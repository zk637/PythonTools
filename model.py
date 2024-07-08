# -*- encoding: utf-8 -*-
'''
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license
 此模块不进行任何计算
'''

class Tips:

    def __init__(self):
        pass

    def print_message(self, message, *args):
        print(message)

    def return_Result(self, result, *args):
        return result, args

class Log_info:
    """
    规则：如果是函数的过程执行的结果或执行流程产生的信息
    """
    def __init__(self):
        pass

    def print_message(self, message, *args):
        print(message)

    def return_Result(self, result, *args):
        return result, args

class Result:
    """
    规则：如果是函数的返回的结果或输入包含True： False：时使用
    """
    def __init__(self):
        pass

    def print_message(self, message, *args):
        print(message)

    def return_Result(self,result,*args):
        return result , args

# 创建一个全局 Tips 实例
tips_m = Tips()
# 创建一个全局 Log_info 实例
log_info_m = Log_info()
# 创建一个全局 Tips 实例
result_m = Result()