import cProfile
import pstats
from io import StringIO
import time
import tools


def profile(enable=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            global input_time  # 使用全局变量

            if enable:
                # 创建一个性能分析器
                # 记录开始时间
                start_time = time.time()
                profiler = cProfile.Profile()
                profiler.enable()

            # 调用原始函数
            result = func(*args, **kwargs)
            input_time = tools.get_input_time()
            if enable and input_time is not None:
                # 如果启用了性能分析，并且记录了输入时间，则输出用户输入时间
                input_elapsed_time = input_time
                # print(f"用户输入时间: {input_elapsed_time} 秒")

            if enable:
                # 停止性能分析
                profiler.disable()
                # 记录结束时间
                end_time = time.time()
                # 创建 StringIO 对象来保存性能分析结果
                stream = StringIO()
                stats = pstats.Stats(profiler, stream=stream)
                stats.sort_stats('cumulative')  # 按累计时间排序
                stats.print_stats()  # 打印性能分析结果
                # 输出性能分析结果
                print("性能分析结果:")
                print(stream.getvalue())  # 输出到控制台
                # 如果输入时间作为参数传递进来了，则输出用户输入时间
                if input_elapsed_time is not None:
                    print(f"用户输入时间: {input_elapsed_time} 秒")
                    print("去除用户输入后的时间：",end_time -start_time -input_elapsed_time, "seconds")
                # get_program_start_time = tools.get_program_start_time()
                # input_time = tools.get_input_time()
                # get_program_start_time =None
                # input_time = None
            return result

        return wrapper

    return decorator