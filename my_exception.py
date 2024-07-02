import sys
import traceback
import ffmpeg


class InputLengthExceededException(Exception):
    """自定义输入长度超出异常类"""

    def __init__(self, message="输入长度超过限制！"):
        self.message = message
        super().__init__(self.message)

class ReadFrameException(Exception):
    """自定义输入长度超出异常类"""

    def __init__(self, message="读取帧有误！"):
        self.message = message
        super().__init__(self.message)

def global_exception_handler(exctype, value, tb, *args):
    """
    全局异常处理函数
      Args:
        exctype: 异常类型
        value: 异常值
        tb: 异常的追踪信息
        *args: 任意数量的资源对象，用于在异常处理过程中关闭这些资源

    Returns:
        None
    """
    try:
        # 构建异常字典，键是数字，值是包含异常类型和处理字符串的列表 以便维护和逻辑扩充
        exception_dict = {
            1: [MemoryError, "MemoryError: {value}\n"],
            2: [ArithmeticError, "ArithmeticError: {value}\n"],
            3: [LookupError, "LookupError: {value}\n"],
            4: [OSError, "OSError occurred: {value}\n"],
            5: [(PermissionError, FileNotFoundError),
                "Error:权限不足或文件不存在\nFilename: {value.filename}" if hasattr(value, 'filename') else "Error:权限不足或文件不存在"],
            6: [TimeoutError, "Error:操作超时\n"],
            7: [BlockingIOError, "Error:IO阻塞\n"],
            8: [ConnectionError, "Error:连接错误\n"],
            9: [ValueError, "Error:值不正确\n"],
            10: [InputLengthExceededException, "过长的参数！\n"],
            11: [ReadFrameException, '读取帧有误！\n'],
            12: [BaseException, "BaseException: {value}\n"]
        }

        # 在异常处理过程中关闭传入的资源对象
        if args:
            for arg in args:
                if hasattr(arg, 'release') and callable(getattr(arg, 'release')):
                    arg.release()
                elif hasattr(arg, 'close') and callable(getattr(arg, 'close')):
                    arg.close()

        # 如果异常不是 ffmpeg._probe.Error，则打印堆栈跟踪信息
        if not issubclass(exctype, ffmpeg._probe.Error) and not issubclass(exctype, InputLengthExceededException):
            tb_str = ''.join(traceback.format_tb(tb))
            if tb_str:
                print(tb_str)

        # 如果异常是 ffmpeg._probe.Error 类型，则重新抛出异常
        if issubclass(exctype, ffmpeg._probe.Error):
            # 需要提供 stdout 和 stderr 参数
            stderr_output = value.stderr if hasattr(value, 'stderr') else "ffmpeg stderr output"
            stdout_output = value.stdout if hasattr(value, 'stdout') else "ffmpeg stdout output"
            raise exctype(value, stdout=stdout_output, stderr=stderr_output)

        # 检查异常是否在异常字典中
        if exception_dict:
            # 遍历异常字典，查找对应的处理字符串
            for key, (exc_type, message) in exception_dict.items():
                if issubclass(exctype, exc_type):
                    # 输出处理字符串
                    print(message.format(value=value))
                    # 处理特定类型的异常
                    if key == 1 or key == 2 or key == 3 or key == 10:
                        sys.exit(1)
                    break
        else:
            print(f"An exception of type {exctype} occurred with value {value}")

    except Exception as e:
        print(e)
