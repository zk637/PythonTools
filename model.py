# -*- encoding: utf-8 -*-
'''
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license
 此模块不进行任何计算
'''

LOG_LEVEL = "INFO"


class Tips:
    def __init__(self):
        pass

    def print_message(self, message, *args):
        if LOG_LEVEL == "INFO" or LOG_LEVEL == "DEBUG":
            print(message)

    def return_Result(self, result, *args):
        return result, args

class Log_info:
    def __init__(self):
        pass

    def print_message(self, message, *args):
        if LOG_LEVEL == "DEBUG":
            print(message)

    def return_Result(self, result, *args):
        return result, args

class Result:
    def __init__(self):
        pass

    def print_message(self, message, *args):
        if LOG_LEVEL == "INFO" or LOG_LEVEL == "DEBUG":
            print(message)

    def return_Result(self, result, *args):
        return result, args


# 创建一个全局 Tips 实例
tips_m = Tips()
# 创建一个全局 Log_info 实例
log_info_m = Log_info()
# 创建一个全局 Tips 实例
result_m = Result()