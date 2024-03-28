import os
import sys

def createog():
    # 设置日志文件夹和文件名前缀
    log_dir = './logs'
    log_prefix = 'output'

    # 获取当前日志文件编号
    log_count_file = os.path.join(log_dir, 'log_count.txt')
    if os.path.exists(log_count_file):
        with open(log_count_file, 'r') as f:
            log_count = int(f.read().strip())
    else:
        log_count = 1

    # 检查当前日志文件大小是否超过限制，超过则创建新的日志文件
    log_file = os.path.join(log_dir, f'{log_prefix}-{log_count}.log')
    if os.path.exists(log_file) and os.path.getsize(log_file) > 20 * 1024 * 1024:
        log_count += 1
        log_file = os.path.join(log_dir, f'{log_prefix}-{log_count}.log')

    # 将新的日志文件编号写入文件
    with open(log_count_file, 'w') as f:
        f.write(str(log_count))

    # 创建日志对象
    logger = Logger(log_file, sys.stdout)
    return log_file

def check_log_size(out_put):
    if os.path.exists(out_put) and os.path.getsize(out_put) >= 20 * 1024 * 1024:
        out_put=createog()
        return InputLogger(out_put)
    else:
        return InputLogger(out_put)

class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


class InputLogger:
    def __init__(self, filename):
        # self.logfile = open(filename, 'a')
        self.logfile = open(filename, 'a', encoding='utf-8')
        self.stdin_backup = sys.stdin
        self.input_str = ''

    def write_input(self, input_str):
        self.logfile.write(input_str + '\n')
        self.logfile.flush()
        self.input_str += input_str

    def start_logging(self):
        sys.stdin = self

    def stop_logging(self):
        sys.stdin = self.stdin_backup

    def read(self, size=-1):
        return self.stdin_backup.read(size)

    def readline(self, size=-1):
        input_str = self.stdin_backup.readline(size)
        self.write_input(input_str)
        return input_str

    def close(self):
        self.logfile.close()
        sys.stdin = self.stdin_backup


def exit_handler():
    sys.stderr.write('\n' + '-' * 50 + 'End' + '-' * 52)