# -*- encoding: utf-8 -*-
'''
@File    :   ResourceExplorer.py
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license

'''
import gc
import sys
import time
import random
import psutil  # 第三方库，用于获取进程内存信息
from functools import wraps
import os
import tracemalloc
import logging # 导入logging模块
import threading
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ResourceMonitor 类：用于记录和释放资源，采用单例模式
class ResourceMonitor:
    _instance = None

    def __init__(self):
        self.called_interfaces = []
        self.io_resources = []  # 正确的属性名称

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def record_call(self, func_name, args, kwargs):
        self.called_interfaces.append({
            'interface': func_name,
            'args': args,
            'kwargs': kwargs,
            'success': True
        })

    def register_resource(self, resource_type, obj):
        self.io_resources.append((resource_type, obj))  # 正确的属性名称

    def release_resources(self):
        for resource_type, obj in self.io_resources: # 正确的属性名称
            try:
                if hasattr(obj, 'close'):
                    obj.close()
                del obj
            except Exception as e:
                logging.error(f"无法释放 {resource_type} 资源: {e}")
        self.io_resources.clear()


# 获取当前进程内存使用信息（单位：字节）
def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def Monitor_All_functions(enable_monitor, methods):
    """
    应用 @profile_all_functions 装饰器到指定方法字典中的所有方法
    enable_profile：布尔值，是否启用监控
    methods：一个字典，key 为方法名，value 为方法对象
    """
    if enable_monitor:
        for key, value in methods.items():
            if callable(value):
                methods[key] = Monitor_functions(enable=True)(value)
    return methods


# 装饰器：记录函数调用及自动释放资源
def Monitor_functions(enable=True, sample_interval=1.0):
    def decorator(func):
        if not enable:
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            monitor = ResourceMonitor.get_instance()
            tracemalloc.start()
            snap_before = tracemalloc.take_snapshot()
            monitor.record_call(func.__name__, args, kwargs)

            # 用于定时采样 RSS 的线程
            stop_flag = threading.Event()
            samples = []

            def sampler():
                while not stop_flag.is_set():
                    rss = get_memory_usage() / (1024**2)
                    samples.append(rss)
                    time.sleep(sample_interval)

            thread = threading.Thread(target=sampler, daemon=True)
            thread.start()

            try:
                return func(*args, **kwargs)
            finally:
                # 停止采样线程
                stop_flag.set()
                thread.join()

                # 结束时的 RSS
                rss_end = get_memory_usage() / (1024**2)

                # 系统级内存报告
                if samples:
                    rss_min = min(samples)
                    rss_max = max(samples)
                    released = rss_max - rss_end  # 峰值减去结束时值
                    print(f"[SYS TRACE] 最低 RSS: {rss_min:.2f} MB, 最高 RSS: {rss_max:.2f} MB, "
                          f"结束时 RSS: {rss_end:.2f} MB, 释放: {released:.2f} MB")

                # tracemalloc 层面快照对比
                snap_after = tracemalloc.take_snapshot()
                diffs = snap_after.compare_to(snap_before, 'lineno')
                print("[PY TRACE] Python 层面内存增量 Top 5：")
                for stat in diffs[:5]:
                    frame = stat.traceback[0]
                    print(f"  {os.path.basename(frame.filename)}:{frame.lineno} +{stat.size_diff / 1024:.1f} KiB")

                monitor.release_resources()
                collected = gc.collect()
                print(f"[DEBUG] gc.collect() 回收 {collected} 个对象")
                tracemalloc.stop()

        return wrapper
    return decorator


# 使用 Monitor_functions 装饰器，无需在业务函数内部插入资源释放逻辑，
# 装饰器会在函数执行后统一调用 release_resources()
@Monitor_functions(enable=True)
def resource_usage(memory_size=1024 * 1024 * 512):  # 添加内存大小参数，默认512MB
    """
    测试函数：
    1. 申请指定大小的内存
    2. 循环打印随机日志一分钟
    """
    print(f"开始测试函数：申请{memory_size / (1024 ** 2):.2f} MB内存，循环打印随机日志一分钟")

    try:
        print("正在申请内存，请稍等...")
        mem = bytearray(memory_size)
        print("内存申请成功!")
    except MemoryError:
        logging.error("内存申请失败，系统内存不足！") # 使用 logging 记录错误
        mem = None

    start_time = time.time()
    while (time.time() - start_time) < 60:
        log_message = f"随机日志: {random.randint(1, 1000000)}"
        logging.info(log_message) # 使用 logging 记录信息
        time.sleep(0.5)

    # 结束测试：解除内存引用（内存回收由垃圾回收机制完成）
    mem = None
    print("测试结束")


def main():
    resource_usage()


if __name__ == '__main__':
    main()
