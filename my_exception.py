'''
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license

'''
import sys
import tkinter
import traceback
from threading import BrokenBarrierError, ThreadError

import ffmpeg

import cv2
import PIL
import pandas
import subprocess
import chardet
import cProfile
import builtins
import pygetwindow
from difflib import SequenceMatcher

import cv2
import ffmpeg
import filetype
import subprocess
import contextlib
import fuzz
import flashtext
import send2trash
import numpy
import pypinyin
import tqdm
import zipfile
import py7zr
import rarfile


class InputLengthExceededException(Exception):
    """自定义输入长度超出异常类"""

    def __init__(self, message="输入长度超过限制！"):
        self.message = message
        super().__init__(self.message)


class ReadFrameException(Exception):
    """自定义读取帧异常类"""

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
            1: [MemoryError, f"MemoryError: {value}\n"],
            2: [ArithmeticError, f"ArithmeticError: {value}\n"],
            3: [LookupError, f"LookupError: {value}\n"],
            4: [OSError, f"OSError occurred: {value}\n"],
            5: [(PermissionError, FileNotFoundError),
                f"Error:权限不足或文件不存在\nFilename: {value.filename}" if hasattr(value, 'filename') else "Error:权限不足或文件不存在"],
            6: [TimeoutError, "Error:操作超时\n"],
            7: [BlockingIOError, "Error:IO阻塞\n"],
            8: [ConnectionError, "Error:连接错误\n"],
            9: [ValueError, "Error:值不正确\n"],
            10: [InputLengthExceededException, "过长的参数！\n"],
            11: [ReadFrameException, '读取帧有误！\n'],
            12: [BaseException, f"BaseException: {value}\n"]
        }

        # 构建第三方模块异常字典，键是数字，值是包含异常类型和处理字符串的列表 以便维护和逻辑扩充
        three_exception_dict = {
            1: [cv2.error, f"cv2.error: {value}\n"],
            2: [ffmpeg._probe.Error, f"ffmpeg._probe.Error: {value}\n"],
            3: [ffmpeg._run.Error, f"ffmpeg._run.Error: {value}\n"],
            4: [numpy.AxisError, f"numpy.AxisError: {value}\n"],
            5: [numpy.ComplexWarning, f"numpy.ComplexWarning: {value}\n"],
            6: [numpy.ModuleDeprecationWarning, f"numpy.ModuleDeprecationWarning: {value}\n"],
            7: [numpy.RankWarning, f"numpy.RankWarning: {value}\n"],
            8: [numpy.TooHardError, f"numpy.TooHardError: {value}\n"],
            9: [numpy.VisibleDeprecationWarning, f"numpy.VisibleDeprecationWarning: {value}\n"],
            10: [PIL.UnidentifiedImageError, f"PIL.UnidentifiedImageError: {value}\n"],
            11: [py7zr.Bad7zFile, f"py7zr.Bad7zFile: {value}\n"],
            12: [py7zr.DecompressionError, f"py7zr.DecompressionError: {value}\n"],
            13: [py7zr.PasswordRequired, f"py7zr.PasswordRequired: {value}\n"],
            14: [py7zr.UnsupportedCompressionMethodError, f"py7zr.UnsupportedCompressionMethodError: {value}\n"],
            15: [py7zr.exceptions.ArchiveError, f"py7zr.exceptions.ArchiveError: {value}\n"],
            16: [py7zr.exceptions.Bad7zFile, f"py7zr.exceptions.Bad7zFile: {value}\n"],
            17: [py7zr.exceptions.CrcError, f"py7zr.exceptions.CrcError: {value}\n"],
            18: [py7zr.exceptions.DecompressionError, f"py7zr.exceptions.DecompressionError: {value}\n"],
            19: [py7zr.exceptions.InternalError, f"py7zr.exceptions.InternalError: {value}\n"],
            20: [py7zr.exceptions.PasswordRequired, f"py7zr.exceptions.PasswordRequired: {value}\n"],
            21: [py7zr.exceptions.UnsupportedCompressionMethodError,
                 f"py7zr.exceptions.UnsupportedCompressionMethodError: {value}\n"],
            22: [py7zr.py7zr.Bad7zFile, f"py7zr.py7zr.Bad7zFile: {value}\n"],
            23: [py7zr.py7zr.CrcError, f"py7zr.py7zr.CrcError: {value}\n"],
            24: [py7zr.py7zr.DecompressionError, f"py7zr.py7zr.DecompressionError: {value}\n"],
            25: [py7zr.py7zr.InternalError, f"py7zr.py7zr.InternalError: {value}\n"],
            26: [py7zr.py7zr.UnsupportedCompressionMethodError,
                 f"py7zr.py7zr.UnsupportedCompressionMethodError: {value}\n"],
            27: [pygetwindow.PyGetWindowException, f"pygetwindow.PyGetWindowException: {value}\n"],
            28: [pygetwindow._pygetwindow_win.PyGetWindowException,
                 f"pygetwindow._pygetwindow_win.PyGetWindowException: {value}\n"],
            29: [rarfile.BadRarFile, f"rarfile.BadRarFile: {value}\n"],
            30: [rarfile.BadRarName, f"rarfile.BadRarName: {value}\n"],
            31: [rarfile.Error, f"rarfile.Error: {value}\n"],
            32: [rarfile.NeedFirstVolume, f"rarfile.NeedFirstVolume: {value}\n"],
            33: [rarfile.NoCrypto, f"rarfile.NoCrypto: {value}\n"],
            34: [rarfile.NoRarEntry, f"rarfile.NoRarEntry: {value}\n"],
            35: [rarfile.NotRarFile, f"rarfile.NotRarFile: {value}\n"],
            36: [rarfile.PasswordRequired, f"rarfile.PasswordRequired: {value}\n"],
            37: [rarfile.RarCRCError, f"rarfile.RarCRCError: {value}\n"],
            38: [rarfile.RarCannotExec, f"rarfile.RarCannotExec: {value}\n"],
            39: [rarfile.RarCreateError, f"rarfile.RarCreateError: {value}\n"],
            40: [rarfile.RarExecError, f"rarfile.RarExecError: {value}\n"],
            41: [rarfile.RarFatalError, f"rarfile.RarFatalError: {value}\n"],
            42: [rarfile.RarLockedArchiveError, f"rarfile.RarLockedArchiveError: {value}\n"],
            43: [rarfile.RarMemoryError, f"rarfile.RarMemoryError: {value}\n"],
            44: [rarfile.RarNoFilesError, f"rarfile.RarNoFilesError: {value}\n"],
            45: [rarfile.RarOpenError, f"rarfile.RarOpenError: {value}\n"],
            46: [rarfile.RarSignalExit, f"rarfile.RarSignalExit: {value}\n"],
            47: [rarfile.RarUnknownError, f"rarfile.RarUnknownError: {value}\n"],
            48: [rarfile.RarUserBreak, f"rarfile.RarUserBreak: {value}\n"],
            49: [rarfile.RarUserError, f"rarfile.RarUserError: {value}\n"],
            50: [rarfile.RarWarning, f"rarfile.RarWarning: {value}\n"],
            51: [rarfile.RarWriteError, f"rarfile.RarWriteError: {value}\n"],
            52: [rarfile.RarWrongPassword, f"rarfile.RarWrongPassword: {value}\n"],
            53: [rarfile.UnsupportedWarning, f"rarfile.UnsupportedWarning: {value}\n"],
            54: [send2trash.TrashPermissionError, f"send2trash.TrashPermissionError: {value}\n"],
            55: [send2trash.exceptions.TrashPermissionError, f"send2trash.exceptions.TrashPermissionError: {value}\n"],
            56: [tqdm.TqdmDeprecationWarning, f"tqdm.TqdmDeprecationWarning: {value}\n"],
            57: [tqdm.TqdmExperimentalWarning, f"tqdm.TqdmExperimentalWarning: {value}\n"],
            58: [tqdm.TqdmKeyError, f"tqdm.TqdmKeyError: {value}\n"],
            59: [tqdm.TqdmMonitorWarning, f"tqdm.TqdmMonitorWarning: {value}\n"],
            60: [tqdm.TqdmSynchronisationWarning, f"tqdm.TqdmSynchronisationWarning: {value}\n"],
            61: [tqdm.TqdmTypeError, f"tqdm.TqdmTypeError: {value}\n"],
            62: [tqdm.TqdmWarning, f"tqdm.TqdmWarning: {value}\n"],
            63: [tkinter.dialog.TclError, f"tkinter.dialog.TclError: {value}\n"],
            64: [tkinter.simpledialog.TclError, f"ttkinter.simpledialog.TclError: {value}\n"],
            65: [BrokenBarrierError, f"threading.BrokenBarrierError: {value}\n"],
            66: [ThreadError, f"ThreadError: {value}\n"]
        }

        # 在异常处理过程中关闭传入的资源对象
        if args:
            for arg in args:
                if hasattr(arg, 'release') and callable(getattr(arg, 'release')):
                    arg.release()
                elif hasattr(arg, 'close') and callable(getattr(arg, 'close')):
                    arg.close()
        else:
            pass

        # 如果异常不是 ffmpeg._probe.Error，则打印堆栈跟踪信息
        if not issubclass(exctype, ffmpeg._probe.Error) and not issubclass(exctype, InputLengthExceededException):
            if tb is not None and hasattr(tb, 'tb_frame'):
                tb_str = ''.join(traceback.format_tb(tb))
                if tb_str:
                    print(tb_str)
            else:
                print(f"异常 {exctype} 没有 traceback 信息。")

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
                    if key == 1 or key == 2 or key == 3:
                        sys.exit(1)
                    break
        else:
            print(f"An exception of type {exctype} occurred with value {value}")

        # 检查异常是否在第三方异常字典中
        if three_exception_dict:
            # 遍历异常字典，查找对应的处理字符串
            for key, (exc_type, message) in three_exception_dict.items():
                if issubclass(exctype, exc_type):
                    # 输出处理字符串
                    print(message.format(value=value))
                    break
                    # # 处理特定类型的异常
                    # if key == 1 or key == 2 or key == 3 or key == 10:
                    #     sys.exit(1)
                    # break
        else:
            print(f"An exception of type {exctype} occurred with value {value}")

    except Exception as e:
        print(e)
