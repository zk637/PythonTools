# -*- encoding: utf-8 -*-
'''
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license
 此模块不进行任何计算
'''
from ColoredPrinter import ColoredPrinter
import re

# 假设你有这份配置
ColoredPrinter.load_presets_from_file("log_colors.json")

class Logger:
    def __init__(self, highlight=True, force_preset_only=False, preset="info"):
        self.highlight = highlight
        self.force_preset_only = force_preset_only
        self.preset = preset  # 新增：明确指定 preset
        self.printers = {
            "debug": ColoredPrinter(preset="debug"),
            "info": ColoredPrinter(preset="info"),
            "error": ColoredPrinter(preset="error")
        }

    def print_message(self, message, *args):
        if args:
            message = message.format(*args)

        if self.force_preset_only:
            # 整句使用指定 preset 着色
            self.printers[self.preset].print(message)
        elif self.highlight:
            parts = self._highlight_keywords_only(message)
            for text, preset in parts:
                if preset:
                    self.printers[preset].print(text, end='')
                else:
                    print(text, end='')
            print()
        else:
            print(message)


    @staticmethod
    def _highlight_keywords_only(message):
        keywords = {
            "TRUE": "info",
            "FALSE": "error",
            "ERROR": "error"
        }

        pattern = re.compile(r"(True|False|ERROR)", re.IGNORECASE)
        parts = []
        last_end = 0

        for match in pattern.finditer(message):
            start, end = match.span()
            if start > last_end:
                parts.append((message[last_end:start], None))
            keyword = match.group()
            preset = keywords.get(keyword.upper(), None)  # 这里必须用 upper 统一查找
            parts.append((keyword, preset))
            last_end = end

        if last_end < len(message):
            parts.append((message[last_end:], None))

        return parts

    @staticmethod
    def print_highlighted(message):
        parts = ColoredPrinter._highlight_keywords_only(message)
        for text, preset in parts:
            if preset:
                printer = ColoredPrinter(preset=preset)
                printer.print(text, end='')
            else:
                print(text, end='')
        print()  # 换行

class TipsLogger(Logger):
    def print_message(self, message, *args):
        if args:
            message = message.format(*args)

        # 提取所有关键词
        pattern = re.compile(r"(True|False|ERROR)", re.IGNORECASE)
        matched_keywords=pattern.finditer(message)

        # 如果包含 'true'，则执行部分高亮逻辑
        if matched_keywords:
            parts = self._highlight_true_only(message)
            for text, preset in parts:
                if preset:
                    self.printers[preset].print(text, end='')
                else:
                    print(text, end='')
            print()
        else:
            # 否则整句用 debug 配置打印
            self.printers["debug"].print(message)

    @staticmethod
    def _highlight_true_only(message):
        pattern = re.compile(r"(True)", re.IGNORECASE)
        parts = []
        last_end = 0

        for match in pattern.finditer(message):
            start, end = match.span()
            if start > last_end:
                parts.append((message[last_end:start], "debug"))  # 其余部分也打 debug preset
            keyword = match.group()
            parts.append((keyword, "info"))  # True 高亮 info
            last_end = end

        if last_end < len(message):
            parts.append((message[last_end:], "debug"))  # 收尾补上 debug

        return parts


class Tips:
    def __init__(self):
        self.logger = TipsLogger()

    def print_message(self, message, *args):
        self.logger.print_message(message, *args)


class Log_info:
    def __init__(self):
        self.logger = Logger(highlight=True)  # 强制整句 info 着色

    def print_message(self, message, *args):
        self.logger.print_message(message, *args)

    def return_Result(self, result, *args):
        return self.logger.return_Result(result, *args)


class Result:
    def __init__(self):
        self.logger = Logger(highlight=True)

    def print_message(self, message, *args):
        self.logger.print_message(message, *args)

    def return_Result(self, result, *args):
        return self.logger.return_Result(result, *args)


class Model:
    def __init__(self):
        self.total_uncompressed_size = 0.0



# 创建一个全局 Tips 实例
tips_m = Tips()
# 创建一个全局 Log_info 实例
log_info_m = Log_info()
# 创建一个全局 Tips 实例
result_m = Result()
# 创建一个全局 Model 实例
model = Model()

if __name__ == "__main__":
    # 可选：从文件加载自定义预设


    tips_m.print_message("13413213")
    tips_m.print_message("True1")
    log_info_m.print_message('TRUE313')
    log_info_m.print_message('ERROR313')
    result_m.print_message('ERROR313')
    result_m.print_message('TRUE313')
    log_info_m.print_message('FALSE1313')
    result_m.print_message('FALSE1313')
