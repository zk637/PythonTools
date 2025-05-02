'''
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license

'''
import os
import sys
import io


def create_log():
    # 获取当前脚本目录，确保 logs 目录存在
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
    log_dir = os.path.join(script_dir, 'logs')  # logs 目录绝对路径
    os.makedirs(log_dir, exist_ok=True)  # 确保 logs 目录存在

    log_prefix = 'output'
    log_count_file = os.path.join(log_dir, 'log_count.txt')  # 计数文件路径

    # 读取 log_count，如果文件不存在则从 1 开始
    if os.path.exists(log_count_file):
        with open(log_count_file, 'r', encoding='UTF-8') as f:
            try:
                log_count = int(f.read().strip())
            except ValueError:
                log_count = 1  # 文件损坏时默认重置为 1
    else:
        log_count = 1

    # 生成日志文件路径
    log_file = os.path.join(log_dir, f'{log_prefix}-{log_count}.log')

    # 如果日志文件已存在且超过 20 MB，则增加计数
    if os.path.exists(log_file) and os.path.getsize(log_file) > 20 * 1024 * 1024:
        log_count += 1
        log_file = os.path.join(log_dir, f'{log_prefix}-{log_count}.log')

    # 更新 log_count 文件
    with open(log_count_file, 'w', encoding='UTF-8') as f:
        f.write(str(log_count))

    return log_file


def check_log_size(out_put):
    if os.path.exists(out_put) and os.path.getsize(out_put) >= 20 * 1024 * 1024:
        out_put = create_log()
        return ConsoleLogger(out_put)
    else:
        return ConsoleLogger(out_put)


class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a', encoding='UTF-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()


def clear_stdin():
    sys.stdin = io.StringIO()


def clear_stdout():
    sys.stdout = io.StringIO()


def clear_stderr():
    sys.stderr = io.StringIO()


class ConsoleLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.log_handle = open(self.log_file, 'a', encoding='UTF-8')
        self.stdin_backup = None
        self.log_cache = io.StringIO()
        self.log_writer = self.LogWriter(self.log_handle, self.log_cache)
        self.log_reader = self.LogReader(self.log_handle, self.log_cache)

    def start_logging(self):
        sys.stdout = self.log_writer
        sys.stderr = self.log_writer
        self.stdin_backup = sys.stdin
        sys.stdin = self.log_reader

    def stop_logging(self):
        sys.stdin = self.stdin_backup
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def close(self):
        self.stop_logging()
        self.log_handle.close()

    class LogWriter:
        def __init__(self, log_handle, log_cache):
            self.log_handle = log_handle
            self.log_cache = log_cache

        def write(self, data):
            sys.__stdout__.write(data)
            sys.__stdout__.flush()
            self.log_cache.write(data)
            self.flush()

        def flush(self):
            sys.__stdout__.flush()
            self.log_handle.write(self.log_cache.getvalue())
            self.log_handle.flush()
            self.log_cache.seek(0)
            self.log_cache.truncate()

    class LogReader:
        def __init__(self, log_handle, log_cache):
            self.log_handle = log_handle
            self.log_cache = log_cache

        def readline(self):
            line = sys.__stdin__.readline()
            if not line:
                return None
            self.log_cache.write(line)
            return line

        def read(self):
            data = sys.__stdin__.read()
            self.log_cache.write(data)
            return data


def exit_handler():
    sys.stderr.write('\n' + '-' * 50 + 'End' + '-' * 52)