'''
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license

'''
import os
import sys
import io

def create_log():
    log_dir = './logs'
    log_prefix = 'output'

    log_count_file = os.path.join(log_dir, 'log_count.txt')
    if os.path.exists(log_count_file):
        with open(log_count_file, 'r', encoding='UTF-8') as f:
            log_count = int(f.read().strip())
    else:
        log_count = 1

    log_file = os.path.join(log_dir, f'{log_prefix}-{log_count}.log')
    if os.path.exists(log_file) and os.path.getsize(log_file) > 20 * 1024 * 1024:
        log_count += 1
        log_file = os.path.join(log_dir, f'{log_prefix}-{log_count}.log')

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
