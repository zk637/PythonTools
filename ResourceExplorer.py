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


class ResourceMonitor:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.called_interfaces = []
        self.io_resources = []
        self.trace_spans = []  # ⬅️ 新增：用于记录链路信息

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
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

    def record_trace_span(self, span_info: dict):
        """统一记录 span"""
        self.trace_spans.append(span_info)
        print(f"[Trace] {span_info['name']} trace_id={span_info['trace_id']} span_id={span_info['span_id']} "
              f"duration={span_info['duration_ms']}ms")

    def register_resource(self, resource_type, obj):
        self.io_resources.append((resource_type, obj))

    def release_resources(self):
        for resource_type, obj in self.io_resources:
            try:
                if hasattr(obj, 'close'):
                    obj.close()
                del obj
            except Exception as e:
                logging.error(f"无法释放 {resource_type} 资源: {e}")
        self.io_resources.clear()

    def get_trace_logs(self):
        """可选：导出 trace 日志"""
        return self.trace_spans


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
            import uuid

            def generate_trace_id():
                return uuid.uuid4().hex

            def generate_span_id():
                return uuid.uuid4().hex
            monitor = ResourceMonitor.get_instance()

            # === 链路追踪信息 ===
            trace_id = generate_trace_id()
            span_id = generate_span_id()
            span_info = {
                "trace_id": trace_id,
                "span_id": span_id,
                "name": func.__name__,
                "args": args,
                "kwargs": kwargs,
                "start_time": time.time()
            }

            # === tracemalloc & memory ===
            tracemalloc.start()
            snap_before = tracemalloc.take_snapshot()
            monitor.record_call(func.__name__, args, kwargs)

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
                result = func(*args, **kwargs)
                span_info["result"] = str(result)[:200]  # 简要记录返回值
                return result
            finally:
                stop_flag.set()
                thread.join()

                rss_end = get_memory_usage() / (1024**2)
                if samples:
                    rss_min = min(samples)
                    rss_max = max(samples)
                    released = rss_max - rss_end
                    print('-'*37+'-------Resource_Track-------'+'-'*37)
                    print(f"[SYS TRACE] 最低 RSS: {rss_min:.2f} MB, 最高 RSS: {rss_max:.2f} MB, "
                          f"结束时 RSS: {rss_end:.2f} MB, 释放: {released:.2f} MB")

                snap_after = tracemalloc.take_snapshot()
                diffs = snap_after.compare_to(snap_before, 'lineno')
                print("[PY TRACE] Python 层面内存增量 Top 5：")
                for stat in diffs[:5]:
                    frame = stat.traceback[0]
                    print(f"  {os.path.basename(frame.filename)}:{frame.lineno} +{stat.size_diff / 1024:.1f} KiB")

                monitor.release_resources()
                gc_count = gc.collect()
                print(f"[DEBUG] gc.collect() 回收 {gc_count} 个对象")

                span_info["duration_ms"] = round((time.time() - span_info["start_time"]) * 1000)
                # monitor.record_trace_span(span_info)
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
