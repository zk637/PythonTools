
import json
import os

class ColoredPrinter:
    COLORS = {
        'black': '30', 'red': '31', 'green': '32', 'yellow': '33',
        'blue': '34', 'magenta': '35', 'cyan': '36', 'white': '37',
        'reset': '0', 'bold': '1', 'underline': '4', 'inverse': '7'
    }

    BACKGROUND_COLORS = {
        'black': '40', 'red': '41', 'green': '42', 'yellow': '43',
        'blue': '44', 'magenta': '45', 'cyan': '46', 'white': '47',
        'reset': '49'
    }

    # 可从文件加载，也可以内置默认预设
    PRESETS = {
        'info': {"colors": ["green"], "bg_color": "reset"},
        'debug': {"colors": ["cyan"], "bg_color": "black"},
        'warning': {"colors": ["yellow"], "bg_color": "reset"},
        'error': {"colors": ["red"], "bg_color": "reset"},
    }

    @classmethod
    def load_presets_from_file(cls, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                cls.PRESETS.update(json.load(f))

    def __init__(self, preset=None, text_color='reset', bg_color='reset', colors=None):
        if preset and preset in self.PRESETS:
            preset_conf = self.PRESETS[preset]
            self.colors = preset_conf.get("colors", [text_color])
            self.bg_color = preset_conf.get("bg_color", bg_color)
        else:
            self.colors = colors if colors else [text_color]
            self.bg_color = bg_color

    def print(self, text_parts, end='\n'):
        if isinstance(text_parts, str):
            text_parts = [text_parts]

        colored_text = ""
        color_idx = 0

        for part in text_parts:
            text_color_code = self.COLORS.get(self.colors[color_idx], '37')  # 默认白
            bg_color_code = self.BACKGROUND_COLORS.get(self.bg_color, '49')  # 默认背景

            colored_text += f"\033[1;{bg_color_code};{text_color_code}m{part}\033[0m"
            color_idx = (color_idx + 1) % len(self.colors)

        print(colored_text, end=end)

if __name__ == "__main__":
    # 可选：从文件加载自定义预设
    ColoredPrinter.load_presets_from_file('log_colors.json')

    info_logger = ColoredPrinter(preset='info')
    debug_logger = ColoredPrinter(preset='debug')
    warning_logger = ColoredPrinter(preset='warning')
    error_logger = ColoredPrinter(preset='error')

    info_logger.print("Info message")
    debug_logger.print("Debug message")
    warning_logger.print("Warning message")
    error_logger.print("Error message")
