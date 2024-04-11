import cProfile
import pstats
from io import StringIO
import time
import tools

# 注册全局异常处理函数
from my_exception import global_exception_handler
global_exception_handler = global_exception_handler


def profile(enable=False):
    """基于cProfile重新实现支持输入窗口记录的性能分析"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            global input_durations
            global last_input_time
            global program_start_time
            if enable:
                # 创建一个性能分析器
                # 记录开始时间
                start_time = time.perf_counter()
                profiler = cProfile.Profile()
                profiler.enable()

            # 调用原始函数
            try:
                result = func(*args, **kwargs)
                if enable:
                    # 停止性能分析
                    profiler.disable()
                    end_time = time.perf_counter()
                    # 创建 StringIO 对象来保存性能分析结果
                    stream = StringIO()
                    stats = pstats.Stats(profiler, stream=stream)
                    stats.sort_stats('cumulative')  # 按累计时间排序
                    stats.print_stats()  # 打印性能分析结果

                    # 输出性能分析结果
                    print("性能分析结果:")
                    print(stream.getvalue())  # 输出到控制台

                    input_durations= tools.get_input_duration()
                    if input_durations is not None and start_time is not None and end_time is not None:
                        print(f"用户输入时间: {sum(input_durations)} 秒") if sum(input_durations) > (end_time - start_time) \
                            else None
                        print("去除用户输入后的时间：", end_time - start_time - sum(input_durations), "seconds") \
                            if end_time - start_time - sum(input_durations) > 0 else None

                    # 重置tools模块中的全局变量
                    tools.program_start_time = None
                    tools.last_input_time = None
                    tools.input_durations = []
                return result
            except Exception as e:
                global_exception_handler(type(e), e, e.__traceback__)

        return wrapper

    return decorator