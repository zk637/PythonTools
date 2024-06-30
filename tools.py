import ctypes
import os
import re
import shutil
from collections import deque

import chardet
import cProfile
import builtins
import time
import pygetwindow as gw
from difflib import SequenceMatcher

import cv2
import ffmpeg
import filetype
import subprocess
import contextlib
import sys

import numpy as np
from tqdm import tqdm

import my_exception

# 注册模块对象
from model import tips_m, log_info_m, result_m
# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler

# 定义一个全局变量，用于记录程序开始时间和用户输入时间
program_start_time = None
last_input_time = None
input_durations = []


def get_program_start_time():
    return program_start_time


def get_input_time():
    return last_input_time


def get_input_duration():
    return input_durations


# 定义一个新的输入函数，用于替换标准的 input 函数
def custom_input(prompt=''):
    global program_start_time
    global last_input_time

    if program_start_time is None:
        program_start_time = time.perf_counter()  # 记录程序开始时间
    start_time = time.perf_counter()  # 记录输入开始时间
    user_input = builtins.original_input(prompt)  # 调用原始的 input 函数
    end_time = time.perf_counter()  # 记录输入结束时间
    current_time = time.perf_counter()  # 获取当前进程的运行时间
    if user_input.strip() != '':
        if last_input_time is not None and current_time >= last_input_time:
            input_duration = end_time - start_time  # 计算实际输入耗时
            input_durations.append(input_duration)  # 将时间差添加到列表中
        last_input_time = current_time  # 更新上次输入时间
    return user_input


# 保存原始的 input 函数
builtins.original_input = builtins.input
# 替换标准的 input 函数为自定义的输入函数
builtins.input = custom_input

from my_profile import profile


@profile(enable=False)
def process_input_str(s=None):
    """输入参数为字符串"""
    str = ""
    str = input().strip()
    return str


temp_input = []


@profile(enable=False)
def process_input_str_limit(ui_param=None):
    """输入参数为字符串，限制总长度不超过195个字符"""
    global temp_input
    temp_input = []

    while True:
        if ui_param is None:
            # 从命令行获取输入
            line = input().strip()
        else:
            # 从UI组件获取输入
            line = ui_param.toPlainText().strip()

        temp_input.append(line)

        if len(' '.join(temp_input)) > 195:
            raise my_exception.InputLengthExceededException()

        return line


@profile(enable=False)
def process_input_list(ui_param=None):
    """输入参数为列表"""
    file_paths = []

    # 处理控制台输入
    if ui_param is None:
        tips_m.print_message(message="请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
        while True:
            path = input().strip('"')
            if not path:
                break
            file_paths.append(path.strip('"'))
    # 处理界面输入
    else:
        text = ui_param.toPlainText()
        file_paths = [path.strip('"') for path in text.split('\n') if path.strip('"')]

    return file_paths


# @profile(enable=False)
# def process_input_list(ui_param=None):
#     """输入参数为列表"""
#     list = []
#     tips_m.print_message(message="请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
#     while True:
#         path = input().strip('"')
#         if not path:
#             break
#         list.append(path.strip('"'))
#     return list


def check_str_is_None(args):
    """通用的单纯验空函数，接受字符串
    Returns:
        bool:
        传入参数有一个非空则返回False
    """
    if args == '' and args == None:
        return True
    else:
        return False


def check_is_None(*args, **kwargs):
    """通用的单纯验空函数，接受任何参数
    Returns:
        bool:
        传入参数有一个非空则返回False
    """
    # 检查位置参数
    if args and all(
            arg is not None and arg != '' and arg != [] and arg != {} and args != () and set() != () for arg in args):
        return False
    # 检查关键字参数
    elif kwargs and all(
            v is not None and v != '' and v != [] and v != {} and args != () and set() != () for v in kwargs.values()):
        return False
    log_info_m.print_message(message="参数有误，为空？")
    return True  # 如果存在参数为空，则返回True


def check_file_or_folder(str_list):
    """
    获取用户输入的文件路径列表和文件夹路径。
    Returns:
        Tuple[List[str], str]: 一个包含文件路径列表和文件夹路径列表的元组。
    """
    file_list = set()
    folder_list = set()
    if str_list:
        for str_item in str_list:
            if os.path.isfile(str_item):
                file_list.add(str_item)
            elif os.path.isdir(str_item):
                folder_list.add(str_item)
                folder_files = set(get_file_paths(str_item))  # 获取文件夹中的文件路径
                file_list.update(folder_files)  # 将文件夹中的文件路径添加到文件集合中
    else:
        log_info_m.print_message(message="参数列表为空！")

    # 将集合转换为列表并返回
    return list(file_list), list(folder_list)


@profile(enable=False)
def process_paths_list_or_folder(ui_param=None):
    """
    获取用户输入的文件路径列表或文件夹路径。
    输入参数为路径列表和文件夹路径的通用方法
    Returns:
        Tuple[List[str], str]: 一个包含文件路径列表和文件夹路径的元组。
    """
    video_paths_list = []

    if ui_param is None:
        # 从命令行获取输入
        tips_m.print_message(message="选择场景：Y/N 文件路径列表(Y) 文件夹（N）")
        flag = process_input_str_limit().lower() or 'n'

        if flag == 'y':
            tips_m.print_message(message="请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
            while True:
                path = process_input_str().strip('"')
                if not path:
                    break
                video_paths_list.append(path.strip('"'))
            folder_path = None
        elif flag == 'n':
            tips_m.print_message(message="请输入文件夹路径：")
            folder_path = process_input_str()
    else:
        # 从界面组件获取输入
        flag = ui_param.toPlainText().lower().strip()

        if flag == 'y':
            # 从界面获取文件路径列表
            text = ui_param.toPlainText()
            video_paths_list = text.replace('\n', ' ').split()
            folder_path = None
        elif flag == 'n':
            # 从界面获取文件夹路径
            folder_path = ui_param.toPlainText()

    return video_paths_list, folder_path


def process_paths_list_and_folder(paths: list,
                                  process_list_func: callable = None,
                                  process_folder_func: callable = None,
                                  list_func_args: tuple = (),
                                  list_func_kwargs: dict = {},
                                  folder_func_args: tuple = (),
                                  folder_func_kwargs: dict = {}) -> list:
    """
    处理文件列表和文件夹路径，根据传入的函数处理列表和文件夹的逻辑。

    参数:
    - paths (list): 包含文件路径或文件夹路径的列表，可以混合列表和文件夹。
    - process_list_func (callable, 可选): 处理文件列表的函数。默认为 None。
    - process_folder_func (callable, 可选): 处理文件夹的函数。默认为 None。
    - list_func_args (tuple, 可选): 传递给 `process_list_func` 的位置参数。默认为空元组 ()。
    - list_func_kwargs (dict, 可选): 传递给 `process_list_func` 的关键字参数。默认为空字典 {}。
    - folder_func_args (tuple, 可选): 传递给 `process_folder_func` 的位置参数。默认为空元组 ()。
    - folder_func_kwargs (dict, 可选): 传递给 `process_folder_func` 的关键字参数。默认为空字典 {}。

    返回:
    - list: 处理后的文件路径列表。

    如果 `paths` 是空的，则打印 "参数为空" 并返回空列表。
    如果 `paths` 中的某个元素既不是列表也不是合法的路径，则打印错误信息并继续处理其他元素。
    """

    if not paths:
        log_info_m.print_message(message="参数为空")
        return []
    video_paths_list, video_dir = paths
    all_files = []

    # 处理列表部分
    for item in video_paths_list:
        if process_list_func:
            all_files.extend(process_list_func([item], *list_func_args, **list_func_kwargs))
        else:
            all_files.append(item)

    if video_dir:
        # 处理文件夹部分
        if os.path.isdir(video_dir):
            if process_folder_func:
                all_files.extend(process_folder_func(*folder_func_args, **folder_func_kwargs))
            else:
                all_files.append(video_dir)
        else:
            log_info_m.print_message(message=f"参数有误，不是合法的路径：{video_dir}")

    return all_files


def add_quotes_forpath(s):
    """使用“包裹字符串"""
    str = '"' + s + '"'
    return str


def add_quotes_forpath_list(paths):
    """
    为路径列表中的每个路径添加双引号并返回
    Args:
        paths (list): 路径列表

    Returns:
        list: 添加了双引号的路径列表
    """
    if paths:
        return ['"' + path + '"' for path in paths]


def make_dir(s):
    os.makedirs(s, exist_ok=True)
    if os.path.exists(s):
        result_m.print_message(message=f"Folder '{s}' created successfully.")


def get_file_count(folder):
    """获取文件夹下所有文件的数量"""
    return len(get_file_paths(folder))


def get_folder_size(folder_path):
    """获取文件夹下所有文件的大小（及文件夹大小）"""
    total_size = 0

    # 遍历文件夹中的所有文件和文件夹
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # 如果是文件，累加文件大小
        if os.path.isfile(item_path):
            total_size += os.path.getsize(item_path)
        # 如果是文件夹，递归计算子文件夹的大小
        elif os.path.isdir(item_path):
            total_size += get_folder_size(item_path)

    return total_size


def count_files(file_paths: list) -> int:
    """
    计算文件列表的文件数量。

    Args:
        file_paths (list): 包含文件路径的列表。

    Returns:
        int: 文件数量。
    """
    file_count = 0

    for path in file_paths:
        if os.path.isfile(path):
            file_count += 1

    return file_count


def for_in_for_print(list, flag=False):
    """
    通用的单纯for循环输出结果
        Args:
        list: 包含文件路径的列表。
        flag: 是否使用“”包裹路径
    example：
    ---------------符合条件的内容---------------
    print()
    ---------------不符合条件的内容---------------
    print()
    """
    if list and flag is not True:
        for str in list:
            result_m.print_message(message=str)
    elif list and flag:
        for str in list:
            result_m.print_message(message=add_quotes_forpath(str))
    else:
        log_info_m.print_message(message="参数有误,列表为空？")


def cont_files_processor(path_list, index):
    if path_list:
        count = count_files(path_list)
        log_info_m.print_message(message="index: {}".format(index))
        result_m.print_message(message=count)
        log_info_m.print_message(message="是否输出符合条件的文件路径 Y/N")
        flag = process_input_str_limit()
        if flag.upper() == 'Y':
            for_in_for_print(path_list)
        return path_list


def get_file_paths(folder):
    """获取文件夹下所有文件的路径"""
    paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            paths.append(path)
    return paths


def get_listunder_fileandfolder(source_dirs):
    """分别获取输入列表中的文件路径和文件夹路径"""
    files = []
    folders = []
    for source_dir_path in source_dirs:
        # 获取每个路径的绝对路径
        abs_path = os.path.abspath(source_dir_path)
        if os.path.isfile(abs_path):
            files.append(abs_path)
        else:
            folders.append(abs_path)
    return files, folders


def get_file_extension(file_path):
    """
       获取文件路径的后缀（包括多个扩展名的情况）
       :param file_path: 文件路径
       :return: 转换小写后的文件后缀
       """
    # 规范化文件路径
    file_path = os.path.normpath(file_path)

    # 获取文件名部分
    file_name = os.path.basename(file_path)

    # 初始化扩展名列表
    extensions = []

    iteration_count = 0  # 初始化计数器

    # 迭代多个扩展名最多两次
    while iteration_count < 2:
        base, ext = os.path.splitext(file_name)
        if ext:
            # 将扩展名添加到列表中
            extensions.append(ext)
            # 更新文件名为当前基本文件名
            file_name = base
            iteration_count += 1  # 增加计数器
        else:
            break

    # 反转扩展名列表并连接成字符串
    file_ext = ''.join(reversed(extensions)).lower()

    return file_ext


def check_in_suffix(file_path, *suffixes):
    """
    检查文件路径的后缀是否在给定的后缀元组中
    :param file_path: 文件路径
    :param suffixes: 后缀元组
    :return: 如果文件路径的后缀在给定的后缀元组中，则返回True，否则返回False
    """
    try:
        # 获取文件扩展名并转换为小写
        file_ext = get_file_extension(file_path).lower()
        # 将后缀元组中的每个后缀都转换为小写（或大写）
        suffixes_lower = [suffix.lower() for suffix in suffixes[0]]  # 取第一个元组内的后缀元素
        # print(f"file_ext: {file_ext}")
        # print(f"suffixes_lower: {suffixes_lower}")
        result = file_ext in suffixes_lower
        return result
    except Exception as e:
        log_info_m.print_message(message=f"Error: {e}")
        global_exception_handler(Exception, f"文件：{file_path}无法获取文件后缀", None)
        return False


def check_not_in_suffix(file_path, *suffixes):
    """
    检查文件路径的后缀是否不在给定的后缀元组中
    :param file_path: 文件路径
    :param suffixes: 后缀元组
    :return: 如果文件路径的后缀不在给定的后缀元组中，则返回True，否则返回False
    """
    try:
        # 获取文件名并转为小写
        file_name = os.path.basename(file_path).lower()
        # 获取后缀名
        file_ext = os.path.splitext(file_name)[1].lower()
        # 检查后缀是否在给定的后缀元组中
        suffixes_lower = [suffix.lower() for suffix in suffixes[0]]  # 取第一个元组内的后缀元素
        result = file_ext not in suffixes_lower
        return result

    except Exception as e:
        log_info_m.print_message(message=f"文件：{file_path}无法获取文件后缀，错误：{e}")
        global_exception_handler(Exception)
        return False  # 如果发生异常，返回 False 表示无法判断


def get_file_paths_limit(folder, *extensions):
    """获取文件夹下指定后缀的所有文件的路径"""
    paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(tuple(extensions)):
                path = os.path.join(root, file)
                paths.append(path)
    if not paths:
        log_info_m.print_message(message="未找到任何文件")
    return paths


def get_file_paths_list_limit(file_paths_list, *extensions):
    """获取文件列表中指定后缀的所有文件的路径"""
    paths = []
    for file_path in file_paths_list:
        for extension in extensions:
            if file_path.endswith(extension):
                paths.append(file_path)
                break  # 如果当前文件路径匹配了任一后缀，则立即跳出内层循环
    if not paths:
        log_info_m.print_message(message="未找到任何文件")
    return paths


def find_matching_files_or_folder_exclude(paths=None, *extensions, folder=None, flag=None):
    if folder:
        """获取文件夹下所有与指定后缀不匹配的文件路径"""
        excluded_files = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                if not file.endswith(extensions):
                    excluded_files.append(file_path)
        return excluded_files
    else:
        """获取文件列表下所有与指定后缀不匹配的文件路径"""
        extensions = [e.lower() for e in extensions]  # 将所有后缀名转换为小写
        matching_files = []
        flag = flag
        for path in paths:
            if os.path.isfile(path):
                path, ext = os.path.splitext(path)
                if ext.lower() in extensions:
                    continue
                dir_path = os.path.dirname(path)
                for filename in os.listdir(dir_path):
                    if not filename.startswith(os.path.basename(path)) or filename.lower().endswith(
                            tuple(extensions)):
                        continue
                    matching_files.append(os.path.join(dir_path, filename))
            elif os.path.isdir(path):
                if flag.upper() == 'Y':
                    for root, dirs, files in os.walk(path):
                        for filename in files:
                            path, ext = os.path.splitext(filename)
                            if ext.lower() not in extensions:
                                matching_files.append(os.path.join(root, filename))
            else:
                raise ValueError(f"{path} is not a valid directory or file path")
        return matching_files


def find_matching_folder_with_exclude(folder, *extensions):
    """检查传入文件夹下是否存在指定后缀的文件，存在一个则返回传入文件夹"""
    paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(tuple(extensions)):
                paths.append(folder)
    return paths


def get_file_paths_e(folder, exclude_dirs, exclude_exts):
    """获取文件夹下的文件路径并排除后缀和文件夹"""
    paths = []
    for root, dirs, files in os.walk(folder):
        if exclude_dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if exclude_exts and file.endswith(tuple(exclude_exts)):
                continue
            path = os.path.join(root, file)
            paths.append(path)
    return paths


def get_file_matching_pattern(file_path, reg):
    """通用指定后缀模糊匹配工具
    :param folder_path: 文件路径
    :param reg: 正则表达式
    :return: 如果文件路径匹配给定的正则，则返回匹配到的路径
    """
    matches = re.match(reg, file_path)
    if matches:
        return file_path


def get_files_matching_pattern(folder_path, reg):
    """通用指定后缀模糊匹配工具
    :param folder_path: 文件夹路径
    :param reg: 正则表达式
    :return: 如果文件路径匹配给定的正则，则返回匹配到的路径列表
    """
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if re.search(reg, filename):
                file_path = os.path.join(root, filename)
                files.append(file_path)
    return files

    # 获取用户输入的文件名列表和路径


def get_list_files(path):
    """
    获取指定路径下包括子目录的所有文件路径
    """
    files = []
    # 递归遍历路径下所有文件和文件夹
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def get_list_dirs(path):
    """
    获取指定路径下的所有子目录路径
    """
    dirs = []
    for subdir in os.listdir(path):
        dir_path = os.path.join(path, subdir)
        if os.path.isdir(dir_path):
            dirs.append(dir_path)
            subdirs = get_list_dirs(dir_path)
            if subdirs:
                dirs.extend(subdirs)
    return dirs


def get_sort_list(rules):
    sorted_rules = sorted(rules, key=len)
    for rule in sorted_rules:
        result_m.print_message(message=f'{rule}')


def get_same_namefile(folder_path):
    all_files = []  # 用于保存所有文件路径

    # 获取所有文件路径
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file_name in filenames:
            file_path = os.path.join(dirpath, file_name)
            all_files.append(file_path)

    # 获取至少有两个相同文件名的路径
    same_name_files = []
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        same_name = [path for path in all_files if os.path.basename(path) == file_name]

        if len(same_name) > 1 and same_name not in same_name_files:
            same_name_files.append(same_name)

    # 返回至少有两个相同文件名的路径
    return [path for file_paths in same_name_files for path in file_paths]


# def get_same_namefile(folder_path):
#     all_files = []  # 用于保存所有文件路径
#
#     # 获取所有文件路径
#     for dirpath, dirnames, filenames in os.walk(folder_path):
#         for file_name in filenames:
#             file_path = os.path.join(dirpath, file_name)
#             all_files.append(file_path)
#
#     # 获取至少有两个相同文件名的路径
#     file_name_dict = {}
#     for file_path in all_files:
#         file_name = os.path.basename(file_path)
#         file_name_dict.setdefault(file_name, []).append(file_path)
#
#     same_name_files = [path for name, paths in file_name_dict.items() if len(paths) > 1 for path in paths]
#
#     # 返回至少有两个相同文件名的路径
#     return same_name_files

# 通用去重工具
def DelRepat(data, key):
    new_data = []
    values = []
    for d in data:
        if d[key] not in values:
            new_data.append(d)
            values.append(d[key])
    return new_data


# 检查文件类型是否合法
# def check_file_access(file_paths):
#     for file_path in file_paths:
#         try:
#             kind = filetype.guess(file_path)
#             if kind is None:
#                 print(f"Cannot determine file type: {file_path}")
#             else:
#                 print(f"File type: {kind.mime}")
#         except Exception as e:
#             print(e)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def detect_encoding(file_path):
    """通用的文件编码检测
        输入参数为文件路径
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if encoding:
            return encoding
        else:
            return 'utf-8'  # 默认返回 utf-8 编码


def convert_to_utf8(input_file_path, encoding):
    """将文件转换为 UTF-8 编码"""
    # 如果未指定输出文件路径，并且编码不是 UTF-8
    if input_file_path and encoding.lower() != 'utf-8':
        # 获取输入文件的目录和文件名
        input_dir, input_filename = os.path.split(input_file_path)
        # 构造输出文件路径
        output_file_path = os.path.join(input_dir, os.path.splitext(input_filename)[0] + "_utf8.txt")
    else:
        # 如果输入文件路径不存在或者编码为 UTF-8，则直接返回
        log_info_m.print_message(message="输入文件路径不存在或者编码为 UTF-8，无需转换")
        return input_file_path

    # 打开输入文件，并以指定的编码方式读取内容
    with open(input_file_path, 'r', encoding=encoding) as input_file:
        content = input_file.read()

    # 将内容以 UTF-8 编码方式写入到新文件中
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(content)

    log_info_m.print_message(message=f"文件已成功转换为 UTF-8 编码，并保存为：{output_file_path}")
    return output_file_path


def check_file_access(file_paths):
    results = {
        'cannot_determine_type': [],
        'has_file_type': [],
        'no_type_determined': [],
        'error_files': []
    }

    for file_path in file_paths:
        try:
            kind = filetype.guess(file_path)
            if kind is None:
                results['cannot_determine_type'].append(file_path)
            else:
                results['has_file_type'].append({'file_path': file_path, 'file_type': kind.mime})
        except Exception as e:
            results['error_files'].append({'file_path': file_path, 'error_message': str(e)})
            global_exception_handler(type(e), e, e.__traceback__)

    # Output files with "Cannot determine file type" error
    if results['cannot_determine_type']:
        log_info_m.print_message(message="Errors with 'Cannot determine file type':")
        for file_path in results['cannot_determine_type']:
            result_m.print_message(message=file_path)
        log_info_m.print_message(message="_" * 30)  # Print a line to separate categories

    # Output files with successful "File type" determined
    if results['has_file_type']:
        log_info_m.print_message(message="Files with 'File type':")
        for file_data in results['has_file_type']:
            log_info_m.print_message(message=f"{file_data['file_path']} (File type: {file_data['file_type']})")
        log_info_m.print_message(message="_" * 30)  # Print a line to separate categories

    # Output files where no type determined
    if results['no_type_determined']:
        log_info_m.print_message(message="Files with no type determined:")
        for file_path in results['no_type_determined']:
            log_info_m.print_message(message=file_path)
        log_info_m.print_message(message="_" * 30)  # Print a line to separate categories

    # Output files with errors
    if results['error_files']:
        log_info_m.print_message(message="Files with errors:")
        for file_data in results['error_files']:
            log_info_m.print_message(message=f"{file_data['file_path']}\nError: {file_data['error_message']}")
        log_info_m.print_message(message="_" * 30)  # Print a line to separate categories


def remove_duplicate_files(file_list):
    files_by_name = {}
    for file_path in file_list:
        name, ext = os.path.splitext(file_path)
        parts = name.split(".")
        file_name = parts[0]
        file_dir = ".".join(parts[1:])
        if file_name not in files_by_name:
            files_by_name[file_name] = {"dirs": {file_dir}, "paths": {file_path}}
        else:
            files_by_name[file_name]["dirs"].add(file_dir)
            files_by_name[file_name]["paths"].add(file_path)
    unique_files = []
    for file_data in files_by_name.values():
        if len(file_data["dirs"]) == 1:
            unique_files.append(list(file_data["paths"])[0])
        else:
            for file_path in file_data["paths"]:
                path, file_name = os.path.split(file_path)
                if file_name.endswith(tuple(file_data["dirs"])):
                    unique_files.append(file_path)
                    break
    return unique_files


# 留重工具
def keep_duplicate_files(file_list):
    # A dictionary to store files by their names
    files_by_name = {}
    # Traverse all the files
    for file_path in file_list:
        # Extract the name and extension of the file
        name, ext = os.path.splitext(os.path.basename(file_path))
        # Count the number of times the name appears
        if name not in files_by_name:
            files_by_name[name] = {'count': 0, 'paths': []}
        files_by_name[name]['count'] += 1
        files_by_name[name]['paths'].append(file_path)

    ique_files = []
    # Traverse the dictionary
    for name, info in files_by_name.items():
        # If the name appears more than once
        if info['count'] > 1:
            # Add all the paths to the result list
            ique_files.extend(info['paths'])
    return ique_files


def subprocess_common(command, shell=True, capture_output=True, text=True):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # 输出命令的详细信息
        log_info_m.print_message(message=result.stdout)
        log_info_m.print_message(message=result.stderr)
    except subprocess.CalledProcessError as e:
        log_info_m.print_message(message=f"Error: {e}")


def subprocess_common_bat(bat_file, command, shell=False, capture_output=True, text=True):
    """通用的bat脚本执行工具
       输入参数为bat文件路径和command
    """
    try:
        # 将命令和批处理文件名组合成一个字符串
        command_with_bat = f'{bat_file} {command}'
        log_info_m.print_message(message=command_with_bat)
        # 调用批处理文件并传递命令作为参数
        process = subprocess.Popen(command_with_bat, shell=shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=text)

        # 获取标准输出和标准错误
        stdout, stderr = process.communicate()

        # 输出命令的详细信息
        log_info_m.print_message(message=stdout)
        log_info_m.print_message(message=stderr)
    except subprocess.CalledProcessError as e:
        log_info_m.print_message(message=f"Error: {e}")


def subprocess_with_progress(command, shell=True):
    """通用的子进程工具
       输入参数为command
    """
    # 启动子进程
    log_info_m.print_message(message=command)
    process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)

    log_info_m.print_message(message=process)
    process.communicate()


# -------------------------------


def remove_duplicate_files(file_list):
    files_by_name = {}
    for file_path in file_list:
        name, ext = os.path.splitext(os.path.basename(file_path))
        if name not in files_by_name:
            files_by_name[name] = [file_path]
        else:
            files_by_name[name].append(file_path)
    unique_files = []
    for file_name, file_paths in files_by_name.items():
        if len(file_paths) > 1:
            # 删除重复的路径，只保留其中一个
            unique_files.append(file_paths[0])
        else:
            # 文件名只出现了一次，直接添加路径
            unique_files.extend(file_paths)
    return unique_files


def rm_folder(folder_path):
    """通用的删除工具 静默删除子文件夹下所有文件
       输入参数为文件夹路径。
    """
    try:
        subprocess.run(['rmdir', '/s', '/q', folder_path], check=False)
        result_m.print_message(message=f"Folder {folder_path} deleted successfully.")
    except subprocess.CalledProcessError as e:
        log_info_m.print_message(message=f"Error: {e}")


def copy_folder(source_folder, destination_folder):
    """通用的复制文件工具
       输入参数为源文件地址和目标文件地址。
    """
    try:
        # 使用 robocopy 命令进行文件夹复制
        result = subprocess.run(
            ['robocopy', source_folder, destination_folder, '/E', '/XO', '/COPY:DAT', '/R:3', '/W:5'], check=False,
            capture_output=True, text=True, encoding='latin-1')

        # print(result.stdout)
        # print(result.stderr)
        result_m.print_message(message=f"Folder copied from '{source_folder}' to '{destination_folder}'")
    except subprocess.CalledProcessError as e:
        log_info_m.print_message(message=f"Error: {e}")


def copy_file(source_file, destination_file):
    """通用的复制文件工具
       输入参数为源文件地址和目标文件地址。
    """
    result = shutil.copy(source_file, destination_file)
    result_m.print_message(message=f"File copied from '{source_file}' to '{destination_file}'")


def create_symbolic_link(source, target_dir, is_folder=False):
    """通用的创建符号链接工具
       输入参数为源文件地址和目标文件地址。
    """
    link_type = '/d' if is_folder else ''
    cmd = ['mklink', link_type, os.path.join(target_dir, os.path.basename(source)), source]
    log_info_m.print_message(message='\n' + '-' * 50)
    log_info_m.print_message(message="\n" + "执行命令: " + ' '.join(cmd) + "\n")
    try:
        subprocess.check_call(cmd, shell=True)
        result_m.print_message(message="源文件路径: " + source)
        result_m.print_message(message="目标文件夹路径: " + target_dir)
    except Exception as e:
        log_info_m.print_message(message="符号链接创建失败: " + str(e))
        global_exception_handler(type(e), e, e.__traceback__)


def read_rules_from_file():
    filename = "file_name_rules.txt"
    if not os.path.exists(filename):
        with open(filename, "w", encoding='UTF-8') as f:
            result_m.print_message(message="规则文件不存在，已创建空文件 file_name_rules.txt")
        return []
    encode = detect_encoding(filename)
    with open(filename, encoding=encode) as f:
        content = f.read().strip()

    if not content:
        log_info_m.print_message(message="file_name_rules规则文件为空")
        return []

    rules = [rule.strip() for rule in content.split(",")]
    return rules


def get_video_details(path):
    """获取视频文件的详细信息"""
    if os.path.exists(path):
        try:
            probe = ffmpeg.probe(path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

            duration = float(probe["format"].get("duration", 0)) * 60
            bitrate = int(probe["format"].get('bit_rate', 0))
            width = int(video_stream['width']) if video_stream and 'width' in video_stream else 0
            height = int(video_stream['height']) if video_stream and 'height' in video_stream else 0

            return duration, bitrate, width, height
        except Exception as e:
            log_info_m.print_message(message=f"处理文件 {path} 时出错：{e}")
            global_exception_handler(type(e), e, e.__traceback__)
            return 0, 0, 0, 0
    else:
        log_info_m.print_message(message=f"文件路径 {path} 不存在")
        return 0, 0, 0, 0


def get_audio_details(path):
    """获取音频文件的常见参数"""
    if os.path.exists(path):
        probe = ffmpeg.probe(path)
        format_info = probe.get("format", {})

        duration = float(format_info.get("duration", 0)) * 60
        bitrate = int(format_info.get("bit_rate", 0))

        return duration, bitrate
    else:
        return 0, 0


def get_video_info_list(paths):
    video_info_list = []
    max_path_len = 0
    attribute_map = {
        1: 'size',
        2: 'duration',
        3: 'bitrate',
    }
    tips_m.print_message(message="请输入排序属性的数字（1-size, 2-duration, 3-bitrate），默认为3-bitrate：")
    sort_index = int(process_input_str_limit() or 3)

    # 初始化进度条
    progress_bar = tqdm(total=len(paths), desc="Processing videos")

    # 检查视频完整性
    for path in paths:
        # 更新进度条
        progress_bar.update(1)
        try:
            duration, bitrate, width, height = get_video_details(path)
            if duration == 0 or bitrate == 0 or width == 0 or height == 0:
                continue  # 跳过值为0的文件

            size = os.path.getsize(path) / (1024 * 1024)
            video_info_list.append((path, size, duration, bitrate, width, height))
            max_path_len = max(max_path_len, len(path))
        except Exception as e:
            log_info_m.print_message(message=f"处理文件 {path} 时出错：{e}")
            global_exception_handler(type(e), e, e.__traceback__)
            continue

    # 关闭进度条
    progress_bar.close()
    sort_attribute = attribute_map.get(sort_index, 'bitrate')
    video_info_list.sort(key=lambda x: x[sort_index])

    result_m.print_message(message=sort_attribute)
    return video_info_list, max_path_len

    # print(f'{len(rule)}: {rule}')


def get_video_duration(video_path):
    """获取视频时长"""
    try:
        result = subprocess.check_output(
            ['ffprobe', '-i', video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")])
        duration = float(result)
        return duration
    except:
        log_info_m.print_message(message=f"Error: Failed to get duration of video {video_path}")
        return 0


def check_audio_stream(video_path):
    try:
        # 运行 ffprobe 命令来检查视频文件的音频流
        result = subprocess.run(
            ['ffprobe', '-i', video_path, '-show_streams', '-select_streams', 'a:0', '-loglevel', 'error'],
            capture_output=True)
        # 检查输出中是否包含音频流信息
        if result.stdout.strip():
            return True
        else:
            return False
    except Exception as e:
        log_info_m.print_message(message=f"检查音频流时发生错误：{e}")
        return False


def convert_video_to_mp3(video_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0] + '.mp3'
    video_final_path = os.path.join(os.path.dirname(video_path), video_name)
    # 检查文件是否包含音频流
    if not check_audio_stream(video_path):
        log_info_m.print_message(message=f"警告：文件 '{video_path}' 不包含音频流，无法转换为 MP3。")
        return
    try:
        subprocess.run(
            ['ffmpeg', '-i', video_path, '-f', 'mp3', '-vn', video_final_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        result_m.print_message(message=f"转换成功：{video_name}")
    except subprocess.CalledProcessError as e:
        result_m.print_message(message=f"转换失败：{video_path}")
        log_info_m.print_message(message=f"错误输出：{e.stderr.decode()}")


def getbitratesort(files):
    # 按比特率排序
    files_bitrate = []
    for file_path in files:
        # 检查文件是否存在
        if not os.path.isfile(file_path):
            log_info_m.print_message(message=f"File {file_path} not found, skipping")
            continue
        try:
            command = ['ffprobe', '-show_format', '-show_streams', '-of', 'json', file_path]

            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            if result.returncode != 0:
                log_info_m.print_message(
                    message=f"ffprobe error (see stderr output for detail): {stderr.decode('utf-8')}")
            # fi=os.path.normpath(file_path)
            # print(fi)
            # quoted_file_path = '"' + file_path + '"'
            probe = ffmpeg.probe(file_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream is not None and 'bit_rate' in video_stream:
                bitrate = int(video_stream['bit_rate'])
                files_bitrate.append((file_path, bitrate))
            else:
                log_info_m.print_message(message=f"No video stream or bit rate information found in file {file_path}")
        except Exception as e:
            log_info_m.print_message(message=f"Error occurred while processing file {file_path}: {str(e)}")
            global_exception_handler(type(e), e, e.__traceback__)

    files_bitrate.sort(key=lambda x: x[1], reverse=True)
    sorted_files = [file_path for file_path, _ in files_bitrate]
    return sorted_files


# import wx
#
# class Frame(wx.Frame):
#
#     def __init__(self):  # ,pos=(0,0)
#         wx.Frame.__init__(self, None, title=u"", pos=(10, 10), size=(1340, 670),
#                           style=wx.SIMPLE_BORDER | wx.TRANSPARENT_WINDOW)
#         self.Center(wx.CURSOR_WAIT)
#         self.SetMaxSize((1340, 670))
#         self.SetMinSize((1340, 670))
#         self.panel = wx.Panel(self, size=(1340, 670))
#         self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
#
#         Close_Button = wx.Button(self.panel, label=u"关闭", pos=(1240, 0), size=(100, 45))
#
#         self.Bind(wx.EVT_BUTTON, self.OnClose, Close_Button)
#
#     def OnClose(self, event):
#         self.Destroy()


def create_groups(lists, reg):
    """从给定的文件列表中找出文件名满足指定正则表达式条件并且出现多次的文件
        Return: List-> list
    """
    lists_by_reg = {}
    for list in lists:
        path, temeame = os.path.splitext(list)
        var = os.path.basename(list)
        tempfilename = os.path.basename(list).split('.')[0]
        # tempfilename=tempfilename.index(1)
        if path not in lists_by_reg:
            # 构建正则
            regf = re.compile(f"" + tempfilename + reg + "")
            match = re.search(regf, var, flags=0)
        if not match:
            lists_by_reg[tempfilename] = {'count': 0, 'path': [], 'name': []}
        lists_by_reg[tempfilename]['count'] += 1
        lists_by_reg[tempfilename]['path'].append(list)
        lists_by_reg[tempfilename]['name'].append(var)
    ique_files = []
    # Traverse the dictionary
    for name, info in lists_by_reg.items():
        # If the name appears more than once
        if info['count'] > 1:
            # Add all the paths to the result list
            ique_files.extend(info['path'])
    return ique_files


def seconds_to_hhmmss(seconds):
    """将秒数转换为时分秒格式"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def get_video_info(path):
    try:
        if os.path.exists(path):
            probe = ffmpeg.probe(path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)

            duration = float(probe["format"]["duration"]) if "format" in probe else 0
            video_bitrate = int(video_stream['bit_rate']) if video_stream else 0
            audio_bitrate = int(audio_stream['bit_rate']) if audio_stream else 0
            width = int(video_stream['width']) if video_stream else 0
            height = int(video_stream['height']) if video_stream else 0

            return duration, video_bitrate, audio_bitrate, width, height
        else:
            log_info_m.print_message(message="File does not exist.")
            return None
    except ffmpeg.Error as e:
        log_info_m.print_message(message=f"Error probing file: {e}")
        return None


def split_video_for_size(part_max_size, part_num, output_prefix, output_dir):
    video_info = get_video_info(output_prefix)
    if video_info is not None:
        duration, video_bitrate, audio_bitrate, width, height = video_info
        part_max_duration = part_max_size * 8 / (video_bitrate + audio_bitrate)
        # 格式化分段最大时长为 HH:MM:SS 格式
        part_max_duration_formatted = seconds_to_hhmmss(part_max_duration)
        log_info_m.print_message(message=f"格式化后的最大时长: {part_max_duration_formatted}")
        # 添加标志以指示是否存在已存在的文件
        existing_file_found = False

        output_prefix_tmp = output_prefix
        output_prefix_tmp = output_prefix_tmp.replace("'", '-')
        filename, file_extension = os.path.splitext(output_prefix_tmp)
        output_prefix_tmp = filename
        output_prefix_tmp.replace('.mp4', '')

        part_index = output_prefix.rfind('_part')
        if part_index != -1:
            # 截取字符串，保留 '_part' 之前的部分
            output_prefix_tmp = output_prefix[:part_index]
            output_prefix_tmp = output_prefix_tmp.replace('.mp4', '')
            # print("Original Name:", output_prefix_tmp)
            result_m.print_message(message="File name contain '_part'.")
        else:
            # 如果未找到 '_part'，执行其他操作
            output_prefix_tmp = output_prefix.replace('.mp4', '')
            result_m.print_message(message="File name does not contain '_part'.")
        part_index = 0
        for part_index in range(int(part_num)):
            output_prefix_tmp = f"{output_prefix_tmp}_part{part_index + 1}.mp4"
            if os.path.isfile(output_prefix_tmp):
                log_info_m.print_message(message=f"Skipping existing file: {output_prefix_tmp}(找到一个已存在的文件就会跳出循环)")
                existing_file_found = True
                output_prefix_tmp = ''
                break  # 找到一个已存在的文件就跳出循环

        if not existing_file_found:
            # 构建拆分命令
            processed_output_prefix = output_prefix.replace('.mp4', '').replace("'", '-')
            split_command = [
                'ffmpeg',
                '-i', output_prefix,
                '-c', 'copy',
                '-map', '0',
                '-f', 'segment',
                '-segment_time', str(part_max_duration),
                '-reset_timestamps', '1',
                '-y',
                # output_prefix.replace('.mp4','').replace("'",'-') + '_part%d.mp4'
                processed_output_prefix + '_part%d.mp4'
            ]
            print(split_command)
            # 使用 subprocess.run 运行拆分命令
            try:
                subprocess.run(split_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                               encoding='utf-8')
            except Exception as e:
                global_exception_handler(e)


def split_audio_for_duration(path, duration):
    filename, file_extension = os.path.splitext(path)
    video_duration = duration / 2 / 60
    log_info_m.print_message(message=video_duration)
    split_command = ['ffmpeg', '-i', path, '-f', 'segment', '-segment_time', str(video_duration), '-c', 'copy',
                     filename + '_part%d.mp3']
    subprocess.run(split_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                   encoding='utf-8')


# def check_subtitle_stream(video_path):
#     if os.path.exists(video_path):
#         video_path=video_path.replace('\\\\', '\\')
#         command = ['ffmpeg', '-i', video_path]
#         print(command)
#         try:
#             output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
#             print(output)
#             streams = re.findall(r'Stream #\d+:\d+(.*?)\n', output)
#             for stream in streams:
#                 if 'Subtitle' in stream:
#                     print(f"{video_path}: 该视频文件包含字幕流。")
#                     return True
#         except Exception as e:
#             streams = re.findall(r'Stream #\d+:\d+(.*?)\n', output)
#             for stream in streams:
#                 if 'Subtitle' in stream:
#                     print(f"{video_path}: 该视频文件包含字幕流。")
#                     return True
#                 else:
#                     print("Error:", f"文件{video_path}：不包含字幕流")
#         return False

def check_subtitle_stream(video_path):
    if os.path.exists(video_path):
        video_path = video_path.replace('\\\\', '\\')
        # ffprobe -v error -select_streams s -show_entries stream=index,codec_name -of default=noprint_wrappers=1:nokey=1 "H:\videos\test.mp4"
        command = ['ffprobe', '-v', 'error', '-select_streams', 's', '-show_entries', 'stream=index,codec_name', '-of',
                   'default=noprint_wrappers=1:nokey=1', video_path]
        # print(command)
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            if output:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            log_info_m.print_message("Error:", f"文件{video_path}：无法获取视频信息")
            log_info_m.print_message(message=e.output)
            return False


def check_mp4(filePath):
    """
    :param filePath:
    :return: total_MB 理论值
    realSize_MB实际值
    """
    total = 0
    try:
        with open(filePath, "rb") as f:
            realSize_bytes = os.path.getsize(filePath)  # 获取文件大小（字节）
            readLarge = False
            while True:
                size = 0
                buff = f.read(8)
                if not buff:
                    break
                if len(buff) < 8:
                    break
                if readLarge:
                    size = int.from_bytes(buff, byteorder='big', signed=False)
                else:
                    size = int.from_bytes(buff[:4], byteorder='big', signed=False)
                if size == 0:
                    break
                if size == 1:
                    # 读取 Large size
                    readLarge = True
                else:
                    total += size
                    skip = size - 8 if not readLarge else size - 16
                    if skip > 0:
                        f.seek(skip, 1)
                        readLarge = False

        # 将理论值、实际值转换成 MB 并输出
        total_MB = total / (1024 * 1024)
        realSize_MB = realSize_bytes / (1024 * 1024)

        return total_MB, realSize_MB
    except FileNotFoundError:
        log_info_m.print_message(message="File not found.")
        return None, None
    except IOError:
        log_info_m.print_message(message="IO error occurred.")
    return None, None


def extract_start_5_minutes(video_path):
    duration = get_video_duration(video_path)
    if duration is not None and duration != 0:
        try:
            command = f'ffmpeg -v error -err_detect explode -ss 300 -i "{video_path}" -t 25 -f null - -xerror'
            log_info_m.print_message(message=command)
            completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               encoding='utf-8')
            if completed_process.returncode == 0 \
                    and 'Context scratch buffers could not be allocated due to unknown size' not in completed_process.stderr \
                    and 'warning: first frame is no keyframe' not in completed_process.stderr \
                    and 'ff asf bad header' not in completed_process.stderr \
                    and 'Header missing' not in completed_process.stderr \
                    and 'co located POCs unavailable' not in completed_process.stderr \
                    and 'Packet mismatch' not in completed_process.stderr \
                    and 'missing picture in access unit' not in completed_process.stderr \
                    and 'Corrupt input packet in stream:' not in completed_process.stderr \
                    and 'Task finished with error code:' not in completed_process.stderr \
                    and 'Terminating thread with return code:' not in completed_process.stderr:
                # print(completed_process.stdout)
                # 现在可以在这里处理提取的视频部分，而不必将其写入文件
                return True, 300
            else:
                log_info_m.print_message(message="Failed to extract start 5 minutes.")
                # print(completed_process.stderr)
                return False, 300
        except Exception as e:
            # 如果有全局异常处理函数，调用它
            global_exception_handler(Exception, f"文件：{video_path}无法获取视频信息", None)
            return False, 0
    else:
        log_info_m.print_message(message="Failed to extract last 5 minutes. Video duration not available.")
        return False, 0


def extract_last_5_minutes(video_path):
    duration = get_video_duration(video_path)
    if duration is not None and duration != 0:
        try:
            start_time = max(duration - 300, 0)
            formatted_start_time = f"{start_time:.6f}"
            command = f'ffmpeg -v error -err_detect explode -ss {formatted_start_time} -i "{video_path}" -t 50 -f null - -xerror'
            log_info_m.print_message(message=command)
            completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               encoding='utf-8')
            if completed_process.returncode == 0 \
                    and 'Context scratch buffers could not be allocated due to unknown size' not in completed_process.stderr \
                    and 'warning: first frame is no keyframe' not in completed_process.stderr \
                    and 'ff asf bad header' not in completed_process.stderr \
                    and 'Header missing' not in completed_process.stderr \
                    and 'co located POCs unavailable' not in completed_process.stderr \
                    and 'Packet mismatch' not in completed_process.stderr \
                    and 'missing picture in access unit' not in completed_process.stderr \
                    and 'Corrupt input packet in stream:' not in completed_process.stderr \
                    and 'Task finished with error code:' not in completed_process.stderr \
                    and 'Terminating thread with return code:' not in completed_process.stderr:

                # print(completed_process.stdout)
                # 现在可以在这里处理提取的视频部分，而不必将其写入文件
                return True, formatted_start_time
            else:
                log_info_m.print_message(message="Failed to extract last 5 minutes.")
                # print(completed_process.stderr)
                return False, formatted_start_time
        except Exception as e:
            # 如果有全局异常处理函数，调用它
            global_exception_handler(Exception, f"文件：{video_path}无法获取视频信息", None)
            return False, 0
    else:
        log_info_m.print_message(message="Failed to extract last 5 minutes. Video duration not available.")
        return False, 0


def get_video_integrity(video_path):
    if os.path.isfile(video_path):
        # 定义 FFmpeg 命令
        command = f'ffprobe -v error -i "{video_path}"'
        log_info_m.print_message(message=command)

    try:
        # 执行命令，并捕获异常
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8',
                                universal_newlines=True)

        stderr_lines = result.stderr.splitlines()
        error_detected = False

        for line in stderr_lines:
            # 检查错误消息是否来自 input stream 2
            if 'Unsupported codec with id' in line and 'input stream 2' in line:
                continue  # 忽略 input stream 2 的错误
            elif 'Header missing' in line or 'Packet mismatch' in line or 'Extra data:' in line or \
                    'co located POCs unavailable' in line or 'partial file' in line:
                error_detected = True
                break

        if error_detected:
            raise Exception("Video integrity check failed due to stream errors.")
        else:
            return True

    except Exception as e:
        # 如果有全局异常处理函数，调用它
        global_exception_handler(Exception, f"文件：{video_path}无法获取视频信息", None)
        return False


def check_green_screen(buffer, width, height):
    """检查视频帧的四个角"""
    if buffer is None or width <= 0 or height <= 0:
        return True

    size = 20  # 每个角要检查的像素数
    threshold = 15  # 绿屏像素阈值

    # 检查左上角
    zero_count = 0
    for j in range(size):
        for i in range(size):
            if (buffer[j, i] == [0, 255, 0]).all():
                zero_count += 1
                if zero_count > threshold:
                    return True

    # 检查右上角
    zero_count = 0
    for j in range(size):
        for i in range(width - size, width):
            if (buffer[j, i] == [0, 255, 0]).all():
                zero_count += 1
                if zero_count > threshold:
                    return True

    # 检查左下角
    zero_count = 0
    for j in range(height - size, height):
        for i in range(size):
            if (buffer[j, i] == [0, 255, 0]).all():
                zero_count += 1
                if zero_count > threshold:
                    return True

    # 检查右下角
    zero_count = 0
    for j in range(height - size, height):
        for i in range(width - size, width):
            if (buffer[j, i] == [0, 255, 0]).all():
                zero_count += 1
                if zero_count > threshold:
                    return True

    return False


def check_video_for_green_screen(video_path, check_frames=60):
    """取视频的前120和后120帧抽样检查是否绿屏 绿屏则返回True"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error Unable to open video file: {video_path}")
            return True

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        corrupted_frames = 0

        # 检查前120帧
        for frame_idx in range(check_frames):
            try:
                ret, frame = cap.read()
                if not ret or frame is None:
                    print(f"Error 无法读取帧 {frame_idx + 1}")
                    return True
                else:
                    height, width, _ = frame.shape
                    if check_green_screen(frame, width, height):
                        print(f"Green screen detected in frame {frame_idx + 1}")
                        corrupted_frames += 1
            except cv2.error as e:
                return True

        # 检查后120帧

        if not cap.set(cv2.CAP_PROP_POS_FRAMES, max(total_frames - check_frames, 0)):
            raise my_exception.ReadFrameException()
        else:
            for frame_idx in range(total_frames - check_frames, total_frames):
                try:
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        print(f"Error 无法读取帧 {frame_idx + 1}")
                        return True
                    else:
                        height, width, _ = frame.shape
                        if check_green_screen(frame, width, height):
                            print(f"Green screen detected in frame {frame_idx + 1}")
                            corrupted_frames += 1
                except cv2.error as e:
                    return True

            cap.release()
            if corrupted_frames > 0:
                print(f"Total corrupted (green screen) frames in {video_path}: {corrupted_frames}")
                return True
            else:
                print(f"All frames in {video_path} are intact")
                return False
    except Exception as e:
        # 如果有全局异常处理函数，调用它
        global_exception_handler(Exception, f"文件：{video_path}无法获取视频信息", None)
        return True


# TODO
def check_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Unable to open video file: {video_path}")
        return False

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    corrupted_frames = 0

    ret, prev_frame = cap.read()  # 读取第一帧

    if not ret or prev_frame is None or prev_frame.size == 0:
        print(f"Error reading the first frame from {video_path}")
        return False

    for i in range(1, frame_count):
        ret, frame = cap.read()
        if not ret or frame is None or frame.size == 0:
            print(f"Error reading frame {i} from {video_path}")
            corrupted_frames += 1
            continue

        if not check_frame_integrity(prev_frame, frame):
            print(f"Corrupted frame detected at frame {i} in {video_path} based on pixel values")
            corrupted_frames += 1
            cap.release()  # 发现损坏帧后立即释放视频对象
            return False

        prev_frame = frame

    cap.release()

    if corrupted_frames > 0:
        print(f"Total corrupted frames in {video_path}: {corrupted_frames}")
        return False
    else:
        print(f"All frames in {video_path} are intact")
        return True


def check_frame_integrity(prev_frame, frame):
    diff = cv2.absdiff(prev_frame, frame)
    non_zero_count = np.count_nonzero(diff)

    # 如果两个帧之间的变化非常大，可以认为帧是损坏的
    if non_zero_count > 0.5 * frame.size:  # 变化超过10%
        return False
    return True

import av
def get_video_resolution(video_path):
    # os.environ['TF_CPP_MIN_LOG_LIVEL'] = '3'
    try:
        container = av.open(video_path)
        for stream in container.streams.video:
            width = stream.codec_context.width
            height = stream.codec_context.height
            return width, height
    except Exception as e:
        print(f"{video_path} 读取分辨率错误: {e}")
        return 0, 0

# def get_video_resolution(video_path):
#     try:
#         cap = cv2.VideoCapture(video_path)
#         if not cap.isOpened():
#             print(f"Cannot open video file: {video_path}")
#             return 0, 0
#
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         cap.release()  # 释放 VideoCapture 资源
#         return width, height
#     except Exception as e:
#         print(f"{video_path}读取分辨率错误")
#         return 0, 0

# def get_video_resolution(video_path):
#     try:
#         cmd = ['ffmpeg', '-i', video_path]
#         result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#         output = result.stderr.decode('utf-8')
#
#         # 提取分辨率信息
#         for line in output.split('\n'):
#             if 'Stream' in line and 'Video' in line:
#                 parts = line.split(',')
#                 for part in parts:
#                     if 'x' in part:
#                         resolution = part.strip().split(' ')[0]
#                         width, height = map(int, resolution.split('x'))
#                         return width, height
#
#         print(f"Cannot get resolution for video file: {video_path}")
#         return 0, 0
#     except Exception as e:
#         print(f"{video_path}读取分辨率错误")
#         return 0, 0
       # global_exception_handler(Exception, f"文件：{video_path}读取分辨率错误", None)

def calculate_scale(width, height):
    if width!=0 and height!=0:
        aspect_ratio = width / height

        if width * height <= 960 * 540:  # 如果是较低的分辨率
            scale_width = width
            scale_height = height
        elif width * height < 3840 * 2160:  # 如果小于4K
            scale_width = width // 2
            scale_height = height // 2
        else:  # 如果大于等于4K
            scale_width = width // 4
            scale_height = height // 4

            # 确保在大于4K的情况下，最大像素量不超过960x540
        max_pixel_area = 960 * 540
        if scale_width * scale_height > max_pixel_area:
            scale_factor = (max_pixel_area / (scale_width * scale_height)) ** 0.5
            scale_width = int(scale_width * scale_factor)
            scale_height = int(scale_height * scale_factor)

        # 保持宽高比
        if aspect_ratio > 1:
            scale_width = int(scale_height * aspect_ratio)
        else:
            scale_height = int(scale_width / aspect_ratio)

        return scale_width, scale_height
    else:
        return 0, 0


def play_tocheck_video_minimized(video_path, last_duration, start_duration):
    """
    使用ffplay播放视频，并将窗口最小化，如果出现错误立即退出
    """
    duration = get_video_duration(video_path)
    width, height = get_video_resolution(video_path)
    scale_width, scale_height = calculate_scale(width, height)
    print(f"Original resolution: {width}x{height}")
    print(f"Scaled resolution: {scale_width}x{scale_height}")

    if width == 0 or height == 0 or scale_height == 0 or scale_width == 0:
        print(f"Error detected in {video_path}: Resolution unavailable")
        return video_path
    if duration < 600:
        magnification = 80
    else:
        magnification = 160
    # 构建ffplay命令
    command = [
        'ffplay',
        '-autoexit',
        # '-nodisp',  # 禁止显示窗口
        '-an',  # 禁止音频输出
        '-vcodec', 'h264_cuvid',  # 使用硬件加速
        '-vf', f'scale={scale_width}:{scale_height},setpts=PTS/{magnification}',
        '-framedrop', '-infbuf',
        video_path
    ]
    if last_duration is not None and float(last_duration) > 0:
        # 查找 -an 参数的位置
        input_index = command.index('-an')
        # 在 -an 参数之前插入 -ss {last_duration} 和 -t 50
        command.insert(input_index, '-ss')
        command.insert(input_index + 1, str(last_duration))
        command.insert(input_index + 2, '-t')
        command.insert(input_index + 3, '50')
    # elif start_duration is not None and float(start_duration) > 0:
    #     # 查找 -an 参数的位置
    #     input_index = command.index('-an')
    #     # 在 -an  参数之前插入 -ss {last_duration} 和 -t 50
    #     command.insert(input_index, '-ss')
    #     command.insert(input_index + 1, '300')
    #     command.insert(input_index + 2, '-t')
    #     command.insert(input_index + 3, '25')
    process = None  # 提前声明process变量
    try:
        print(str(command))
        # 启动ffplay进程
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

        # 等待ffplay窗口出现
        time.sleep(2)

        # 获取ffplay窗口并最小化
        windows = gw.getWindowsWithTitle('ffplay')
        if windows:
            window = windows[0]
            window.minimize()

        # 实时监控ffplay的输出 创建队列用于回溯错误信息
        output_deque = deque(maxlen=5)
        video_time = None
        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output_deque.append(output)

                # 过滤和打印重要的错误信息
                if 'error' in output.lower() or 'invalid' in output.lower() or 'failed' in output.lower() or 'packet mismatch' \
                        in output.lower() or 'partial file' in output.lower():
                    error_message = output.strip()
                    for line in reversed(output_deque):
                        time_match = re.search(r"M-V:\s+(\d+\.\d+)", line)
                        if time_match:
                            video_time = float(time_match.group(1)) * 20
                            break
                    if video_time is not None:
                        print(f"Error detected in {video_path} at {video_time:.2f} seconds: {error_message}")
                    else:
                        print(f"Error detected in {video_path}: {error_message}")
                    process.terminate()
                    break

        # 等待进程结束
        process.wait()

        return video_path
    except Exception as e:
        print(f"Exception occurred: {e}")
        process.kill()
        # 如果有全局异常处理函数，调用它
        global_exception_handler(Exception, f"文件：{video_path}无法获取视频信息", None)
        return video_path


# TODO 已废弃,该命令执行效率低资源占用高
def get_video_integrity_old(video_path):
    if os.path.isfile(video_path):
        # 定义 FFmpeg 命令
        command = f'ffmpeg -v  error -err_detect explode -i "{video_path}" -f null - -xerror'
        log_info_m.print_message(message=command)
    try:
        # 执行命令，并捕获异常
        result = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
        # 如果返回码不为0，说明命令执行出错
        if result.returncode != 0:
            raise False
        # 如果输出为空，则文件完整
        else:
            return True
    except Exception as e:
        # 如果有全局异常处理函数，调用它
        global_exception_handler(Exception, f"文件：{video_path}无法获取视频信息", None)
        return False


def register_findone(lists, reg):
    lists_by_reg = {}  # 用于存储每个文件名前缀对应的信息
    try:
        for file_path in lists:
            tempfilename = os.path.basename(file_path).split('.')[0]

            # 如果文件名前缀已经存在于字典中，则更新字典中的信息
            if tempfilename in lists_by_reg:
                lists_by_reg[tempfilename]['count'] += 1
                lists_by_reg[tempfilename]['path'].append(file_path)
                lists_by_reg[tempfilename]['name'].append(os.path.basename(file_path))
            else:
                lists_by_reg[tempfilename] = {  # 创建一个新的字典来存储每个文件名前缀对应的信息
                    'count': 1,
                    'path': [file_path],
                    'name': [os.path.basename(file_path)]
                }

        grouped_results = []  # 用于存储分组结果
        for tempfilename, info in lists_by_reg.items():
            regf = re.compile(tempfilename + reg)
            matched_paths = []
            for file_path in info['path']:
                match = regf.search(os.path.basename(file_path))
                if match:
                    matched_paths.append(file_path)
            # 只有至少有两个文件路径匹配正则表达式时才将它们添加到结果列表中
            if len(matched_paths) > 1:
                grouped_results.append(matched_paths)

        return grouped_results
    except re.error as e:
        pass


# --------------------------------------------------------------
# TODO
def register_find(lists, reg):
    lists_by_reg = {}
    for file_path in lists:
        tempfilename = os.path.basename(file_path).split('.')[0]
        # Create an entry in the dictionary if it does not exist
        if tempfilename not in lists_by_reg:
            lists_by_reg[tempfilename] = {
                'count': 0,
                'path': [],
                'name': []
            }
        regf = re.compile(tempfilename + reg)
        match = regf.search(os.path.basename(file_path))
        if match:
            lists_by_reg[tempfilename]['count'] += 1
            lists_by_reg[tempfilename]['path'].append(file_path)
            lists_by_reg[tempfilename]['name'].append(os.path.basename(file_path))

    # Traverse the dictionary
    ique_files = []
    for tempfilename, info in lists_by_reg.items():
        # If the name appears more than once
        if info['count'] > 1:
            # Add all the paths to the result list
            ique_files.extend(info['path'])

    # Group the results by each distinct file prefix
    grouped_results = []
    for tempfilename, info in lists_by_reg.items():
        if len(info['path']) > 1:
            grouped_results.append(info['path'])

    return grouped_results


# def get_free_space_cmd(path="."):
# # 使用命令行获取磁盘剩余空间
# command = f"dir /-C {path} | findstr bytes free"
# result = subprocess.run(command, capture_output=True, text=True, shell=True)
#
# # 提取剩余空间信息
# lines = result.stdout.splitlines()
# if len(lines) >= 2:
#     free_space_line = lines[1].strip()
#     free_space_gb = int(free_space_line.split()[0]) / (1024 ** 3)  # 转换为GB
#     return free_space_gb
# else:
#     return None
# 使用命令行获取磁盘剩余空间
# 获取当前语言环境
# current_locale, _ = locale.getdefaultlocale()
#
# # 根据语言环境选择关键词
# if current_locale.startswith("en"):
#     keywords = "/C:\"bytes free\""
# elif current_locale.startswith("zh"):
#     keywords = "/C:\"字节 可用\""
# else:
#     # 默认选择英文关键词
#     keywords = "/C:\"bytes free\""
#
# # 使用命令行获取磁盘剩余空间
# command = f"dir {path} | findstr {keywords}"
# result = subprocess.run(command, capture_output=True, text=True, shell=True)
#
# # 提取剩余空间信息
# lines = result.stdout.splitlines()
# if len(lines) >= 2:
#     free_space_line = lines[1].strip()
#     free_space_gb = int(free_space_line.split()[0]) / (1024 ** 3)  # 转换为GB
#     return free_space_gb
# else:
#     return None


class Profiler:
    def __init__(self):
        self.profiler = None
        self.start_time = None

    def start(self):
        self.profiler = cProfile.Profile()
        self.profiler.enable()
        self.start_time = time.time()

    def stop(self):
        self.profiler.disable()
        end_time = time.time()
        log_info_m.print_message("Elapsed time:", end_time - self.start_time, "seconds")
        return self.profiler


from functools import wraps


def profile_all_functions(enable=False):
    """
    一个装饰器，用于动态地为函数添加 @profile(enable=True)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if enable:
                return profile(enable=True)(func)(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def apply_profile_to_methods(enable_profile, methods):
    """
    应用 @profile_all_functions() 装饰器到指定方法字典中的所有方法
    """
    if enable_profile:
        for key, value in methods.items():
            methods[key] = profile_all_functions(enable=True)(value)
    return methods


def admin_process():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

        # 检查是否是管理员权限，如果不是则重新运行脚本作为管理员
        # if not is_admin():
        #     print("当前没有管理员权限，将尝试申请管理员权限...")
        #     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        #     ctypes.windll.user32.PostQuitMessage(0)
        #     sys.exit()

    if not is_admin():
        log_info_m.print_message(message="当前没有管理员权限，将尝试申请管理员权限并重新启动程序...")
        # 构建运行命令列表
        set_cmd_title("Tool_User")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        # 在新的进程中运行命令，等待命令执行完毕
        result_m.print_message(message="程序将重新启动...")
        # 重定向
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        # 用当前的可执行文件和命令行参数替代当前进程
        os.execl(sys.executable, *([sys.executable] + sys.argv))
        sys.exit()


def get_free_space_cmd(folder_path):
    """检查磁盘是否有空余空间
        输入文件路径
    """
    # 提取文件夹所在磁盘的根目录
    # TODO 多语言环境兼容
    drive_letter = os.path.splitdrive(os.path.abspath(folder_path))[0]
    # drive_letter=drive_letter+r'\\'
    # 使用命令行获取磁盘剩余空间
    command = f'dir {drive_letter} |  findstr /C:"字节" | findstr /C:"可用"'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    # 提取剩余空间信息G:\Videos\short\test
    lines = result.stdout.splitlines()
    # 遍历每行输出，提取目录到可用字节之间的内容
    for line in lines:
        match = re.search(r'目录\s+(.*?)\s+可用字节', line)
        if match:
            free_space = match.group(1).strip()
            # print("剩余空间:", free_space)
            return int(free_space.replace(',', ''))
        else:
            log_info_m.print_message(message="未找到剩余空间信息")
            return 1 / 0


# 设置 cmd 窗口的标题
def set_cmd_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)


def capture_output_to_file(func):
    def wrapper(*args, **kwargs):
        with open('output.txt', 'a', encoding='utf-8') as f:
            # f.write(os.linesep.join(output))
            with contextlib.redirect_stdout(f):
                func(*args, **kwargs)

    return wrapper


# TODO 更加多样的参数逻辑支持
def generate_bat_script(bat_file, command):
    """通用的bat文件生成工具
       输入参数为bat文件路径和command
    Returns:
        Tuple[List[str], str]: 一个包含文件路径列表和文件夹路径的元组。
    """
    # 检查批处理文件是否已存在
    if os.path.exists(bat_file):
        return bat_file

    # 打开批处理文件以写入模式
    with open(bat_file, 'w', encoding='UTF-8') as f:
        # 写入批处理文件的内容
        f.write('@echo off\n')
        f.write('REM 获取 Python 传递的命令参数\n')
        f.write('set COMMAND=%*\n')
        f.write('\n')
        f.write('REM 输出传递的命令参数\n')
        f.write('echo COMMAND: %COMMAND%\n')
        f.write('\n')
        f.write('REM 执行传递的命令\n')
        f.write('start cmd /k %COMMAND%\n')
        f.write('\n')
        f.write('REM 检查上一个命令的执行结果，如果失败则输出错误信息\n')
        f.write('if errorlevel 1 (\n')
        f.write('    echo Error: Failed to execute the command.\n')
        f.write('    pause\n')
        f.write('    exit /b 1\n')
        f.write(')\n')
        f.write('\n')
        f.write('echo Command executed successfully.\n')
        f.write('pause\n')

    return bat_file
