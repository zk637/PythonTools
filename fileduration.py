import ctypes
import os
import re
import shutil
import subprocess
import sys
import cProfile
import pstats
import io
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import ffmpeg

import tools

def get_video_duration_sorted():
    """获取文件夹下所有视频文件的时长并排序输出"""
    print("请输入视频文件夹")
    folder = tools.process_input_str("")
    folder_flag=True
    if not os.path.isdir(folder):
        folder_flag=False
        paths = []
        while True:
            path = input("请输入文件路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
            if not path:
                break
            paths.append(path.strip('"'))
    else:
        paths = []  # Define paths here as a fallback if not inside the 'if' branch

    print("是否输出文件时长大小一致的列表？Y/N de:N")
    same_flag=input()
    print("是否纯净输出y/n")
    flag = input()
    if same_flag=='N':
        if folder_flag:
            # paths = tools.get_file_paths_limit(folder,'.mp4','.mkv','.avi')
            paths = tools.get_file_paths_limit(
                folder, '.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
                '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
                '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
                '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
        durations = []
        for path in paths:
            duration = tools.get_video_duration(path)
            if duration is not None:
                durations.append((path, duration))

        sorted_durations = sorted(durations, key=lambda x: x[1], reverse=True)
        for path, duration in sorted_durations:
            if (flag == 'y'.lower()):
                path = tools.add_quotes_forpath(path)
                print(path)
            else:
                print(f"{path}: {duration / 60:.2f} min")

    if same_flag.upper() == 'Y':
        video_extensions = tools.get_file_paths_limit(
            folder, '.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
            '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
            '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv',
            '.mov',
            '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv',
            '.divx',
            '.webm', '.wtv', '.f4v', '.mxf')
        durations = []
        file_sizes = {}  # Dictionary to store file sizes and creation times
    try:
        for path in video_extensions:
            duration = tools.get_video_duration(path)
            if duration is not None:
                file_size = os.path.getsize(path)
                creation_time = os.path.getctime(path)
                if file_size not in file_sizes:
                    file_sizes[file_size] = []
                file_sizes[file_size].append((path, duration, creation_time))

        # Filter out file size groups with only one file
        file_sizes = {k: v for k, v in file_sizes.items() if len(v) > 1}

        # For each file size group, further group files by duration
        for file_size, paths_durations_creation in file_sizes.items():
            # Sort files by creation time (ascending)
            paths_durations_creation.sort(key=lambda x: x[2])

            # Group files by duration
            duration_groups = {}
            for path, duration, _ in paths_durations_creation:
                if duration not in duration_groups:
                    duration_groups[duration] = []
                duration_groups[duration].append(path)

            # Filter out duration groups with only one file
            duration_groups = {k: v for k, v in duration_groups.items() if len(v) > 1}

            # Print paths for each duration group, sorted by duration
            for duration, paths in duration_groups.items():
                if (flag == 'y'.lower()):
                    for path in paths[1:]:
                        path = tools.add_quotes_forpath(path)
                        print(path)
                else:
                    print(f"{duration / 60:.2f} min")
                    for path in paths[1:]:  # Exclude the first (earliest created) file
                            path = tools.add_quotes_forpath(path)
                            print(path)
    except Exception as e:
        print(e)

def get_max_duration(paths, video_extension):
    # Get the maximum duration for a specific video extension and remove it from the list
    max_duration = 0
    max_duration_index = None

    for i, (path, duration) in enumerate(paths):
        if path.endswith(video_extension) and duration > max_duration:
            max_duration = duration
            max_duration_index = i

    if max_duration_index is not None:
        paths.pop(max_duration_index)  # Remove the file with the max duration from the list

    return max_duration



def print_video_info_list():
    # 创建 cProfile 对象
    profiler = cProfile.Profile()
    # 启动性能分析
    profiler.enable()
    """输出视频文件的大小、时长、比特率和分辨率"""
    start = time.time()
    print(start)
    print("选择场景：Y/N 文件路径列表(Y) 文件夹（N）")
    flag=input() or 'n'
    if flag.lower()=='y':
        # 新增方法：获取文件路径列表
        file_paths_list = []

        while True:
            print("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
            path = input()
            # path = input("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
            if not path:
                break
            file_paths_list.append(path.replace('"',''))
        print("是否纯净输出y/n")
        flag = input()
        folder=tools.get_file_paths_list_limit(file_paths_list,'.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
            '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
        '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
        '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
    else:
        print("请输入视频文件夹")
        folder = tools.process_input_str("")
        print("是否纯净输出y/n")
        flag = input()
        folder = tools.get_file_paths_limit(folder,'.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
                '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
            '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
            '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
    if not folder:
        print("文件为空，需检查条件或参数！")
        return
    # pool=ThreadPoolExecutor(1)
    # future =pool.submit(tools.get_video_info_list,folder)
    # future_result=future.result()
    # video_info_list, max_path_len = future_result
    video_info_list, max_path_len = tools.get_video_info_list(folder)
    for video_info in video_info_list:
        path = video_info[0]
        size = "{:.2f}MB".format(video_info[1])
        duration = "{:.2f}min".format(video_info[2] / (60*60))
        bitrate = "{:.2f}kbps".format(video_info[3] / 1024)
        width = video_info[4]
        height = video_info[5]
        if (flag == 'y'.lower()):
            print(path)
        else:
            print("{:<{}}{:<15}{:<15}{:<15}{:<15}".format(path, max_path_len, size, duration, bitrate, f"{width}x{height}"),
              end="")
            print(" " * (max_path_len - len(path) + 1))

    end = time.time()
    print(end)
    print("cost:", end - start, "seconds")
    # 停止性能分析
    profiler.disable()

    # 将分析结果保存到文件或打印出来
    output = io.StringIO()
    stats = pstats.Stats(profiler, stream=output).sort_stats('cumulative')
    stats.print_stats()
    print(output.getvalue())


def generate_video_thumbnail():
    print("请输入视频文件夹")
    folder=tools.process_input_str("")
    video_path = tools.get_file_paths_limit(folder, '.mp4', '.mkv', '.avi')
    thumbnail_path=r"\\video_thumbnail\\"

    return thumbnail_path

def check_files_in_folder(file_list):
    # 提示用户输入目录路径
    print("请输入要检索的目录：")
    folder_path = input()
    print("只输出不匹配的文件？ Y/N def:N")
    flag=input() or "N"
    # 将 file_list 中的双引号去除
    file_list = [file.strip('"') for file in file_list]

    # 获取 file_list 中的文件名和文件夹名
    file_names, folder_names = tools.get_listunder_fileandfolder(file_list)

    matching_paths = []
    non_matching_paths = []

    for root, dirs, files in os.walk(folder_path):
        # 如果需要比较文件夹名，则只保留需要比较的文件夹
        for dir in dirs:
            path = os.path.join(root, dir)  # 初始化 path 变量
            for name in folder_names:
                if (os.path.basename(dir).lower()) == (os.path.basename(name).lower()):
                    matching_paths.append(path)
                else:
                    non_matching_paths.append(path)
    for root, dirs, files in os.walk(folder_path):
        # 如果需要比较文件名，则只保留需要比较的文件名
        for file in files:
            path = os.path.join(root, file)  # 初始化 path 变量
            for name in file_names:
                if (os.path.basename(file).lower()) == (os.path.basename(name).lower()):
                    matching_paths.append(path)
                else:
                    non_matching_paths.append(path)

    if not matching_paths:
        # 如果没有找到匹配的文件，则输出提示信息并返回 None
        print("没有找到匹配的文件。")
        return None

    # 输出不匹配的文件路径
    if non_matching_paths and "Y"==flag.upper():
        print("找到不匹配的文件：")
        for file_path in non_matching_paths:
            print('"' + f"{file_path}" + '"')
    else:
        # 如果找到了匹配的文件，则输出每个匹配的文件的路径
        print("找到匹配的文件：")
        for file_path in matching_paths:
            print('"' + f"{file_path}" + '"')

    return matching_paths, non_matching_paths


def compare_and_move_files():
    excluded_extensions = ['.dll', '.exe', 'png', '.xml', '.html', '.mp3']
    print("请输入需要对比的文件夹")
    folder_path = tools.process_input_str("")
    print("是否保留多个后缀比较【默认保留】")
    model = str(input("") or 'y')
    jpg_files = []
    non_jpg_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1]
            if file_extension == '.jpg':
                jpg_files.append(file_path)
            elif file_extension not in excluded_extensions:
                non_jpg_files.append(file_path)
    for non_jpg_file in non_jpg_files:
        if (model.lower()=='y'):
            file_name = os.path.basename(non_jpg_file)
        else:
            file_name = os.path.splitext(os.path.basename(non_jpg_file))[0]

        same_name_files = []
        for jpg_file in jpg_files:
            jpg_file_base = os.path.splitext(os.path.basename(jpg_file))[0]
            if jpg_file_base not in excluded_extensions and jpg_file != non_jpg_file and jpg_file_base == file_name:
                same_name_files.append(jpg_file)
        print(same_name_files)
        if len(same_name_files) > 0:
            for jpg_file in same_name_files:
                jpg_dir = os.path.dirname(jpg_file)
                if not jpg_dir.endswith('.ts'):
                    jpg_dir = os.path.join(jpg_dir, '.ts')
                elif not jpg_dir.endswith('/'):
                    jpg_dir = jpg_dir + '/'
                ts_dir = os.path.abspath(jpg_dir)
                if not os.path.exists(jpg_dir):
                    os.mkdir(jpg_dir)
                    ts_dir = jpg_dir
                    break
            for file in same_name_files:
                file_extension = os.path.splitext(file)[1]
                if file_extension == '.jpg':
                    try:
                        # shutil.move(file,ts_dir)
                        f_path=shutil.copy(file, ts_dir)
                        jpg_files.remove(file)
                        # non_jpg_files.remove(non_jpg_file)
                        os.remove(file)
                    except Exception as e:
                        print(f'处理发生错误：{file}')
                        print(e)
                    # finally:
                    #     print(f'{f_path}')
                    # finally:
                    #     print(f'{file}n')

def get_file_paths_with_rules():
    """
    获取文件夹下所有文件的路径，并返回文件名符合指定规则的文件路径列表
    :param folder: 文件夹路径
    :return: 符合规则的文件路径列表
    """
    print("请输入需要对比的文件夹")
    folder_path = tools.process_input_str("")
    paths = []
    file_name_rules = tools.read_rules_from_file()
    # print(f"规则列表：{file_name_rules}")
    try:
        for root, dirs, files in os.walk(folder_path,topdown=False):
            for folder_name in dirs:
                folder_full_path = os.path.join(root, folder_name)
                for rule in file_name_rules:
                    regex_pattern = r'^' + re.escape(rule) + r'$'
                    if not rule:
                        continue
                    if re.search(regex_pattern, folder_name):
                        paths.append(folder_full_path)
                        break
            for file_name in files:
                file_full_path = os.path.join(root, file_name)
                file_name_without_ext, file_ext = os.path.splitext(file_name)
                for rule in file_name_rules:
                    regex_pattern = r'^.*' + re.escape(rule) + r'.*$'
                    if not rule:
                        continue
                    # print(regex_pattern)
                    if re.search(regex_pattern, file_name_without_ext):
                        paths.append(file_full_path)
                        break
        # paths=tools.add_quotes_forpath(paths)
        print('\n'.join(paths))
    except Exception as e:
        print(e)

def get_file_paths_with_name():
    # 获取用户输入的文件名列表和路径
    print(r"请输入需要检索的文件夹路径：")
    folderpath = input()
    found_files = []

    filenames_list=[]
    while True:
        print("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
        path=input()
        # path = input("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
        if not path:
            break
        filenames_list.append(path)
    # 获取指定路径下及其子目录下的所有文件路径
    files_in_folder = tools.get_list_files(folderpath)
    # 获取指定路径下的所有子目录路径
    dirs_in_folder = tools.get_list_dirs(folderpath)

    # 对比用户输入的文件名和指定路径下的所有文件中的文件名，找到匹配的文件
    for filename in filenames_list:
        for file in files_in_folder:
            if os.path.splitext(os.path.basename(file))[0] == filename:
                found_files.append(file)
        for subdir in dirs_in_folder:
            if os.path.splitext(os.path.basename(subdir))[0] == filename:
                    found_files.append(subdir)

    # 按找到的文件数量输出文件路径，如果没有找到就输出提示信息
    if len(found_files) > 0:
        print("找到的文件有:")
        for file in found_files:
            file=tools.add_quotes_forpath(file)
            print(file)
    else:
        print("这些文件都不存在！")

# def compare_file_and_folder_names():
#     excluded_extensions = ['.dll', '.exe', '.png', '.xml', '.html', '.mp3','.ts']
#     print("请输入源文件夹路径:")
#     source_folder_path = input("")
#     print("请输入目标文件夹路径:")
#     target_folder_path = input("")
#     source_files_list = []
#     target_folders_list = []
#     same_list = []
#
#     for root, dirs, files in os.walk(source_folder_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             file_name = os.path.splitext(file)[0]
#             file_extension = os.path.splitext(file)[1]
#             if file_extension not in excluded_extensions:
#                 source_files_list.append(file_name)
#
#     for root, dirs, files in os.walk(target_folder_path):
#         for folder in dirs:
#             target_folder_name = os.path.basename(folder)
#             if target_folder_name in source_files_list:
#                 source_file_path = os.path.join(source_folder_path, target_folder_name)
#                 target_folder_path = os.path.join(target_folder_path, target_folder_name)
#                 same_list.append((source_file_path, target_folder_path))
#
#     print("源文件:")
#     for item in same_list:
#         print("文件路径: " + item[0])
#     print("目标文件夹:")
#     for item in same_list:
#         print("文件夹路径: " + item[1])


def create_symbolic_links():
    tools.admin_process()
    excluded_extensions = ['.dll', '.exe', '.png', '.xml', '.html', '.mp3', '.ts']
    print("请输入源文件夹路径:")
    source_folder_path = input("")
    print("请输入目标文件夹路径:")
    target_folder_path = input("")
    source_files_list = []
    same_list = []

    for root, dirs, files in os.walk(source_folder_path):
        for file in files:
            source_files_list.append(os.path.join(root, file))

    for root, dirs, files in os.walk(target_folder_path):
        for folder in dirs:
            target_folder_name = os.path.basename(folder)
            target_folder_path = os.path.join(root, folder)
            file_name = os.path.splitext(target_folder_name)[0]
            same_name_files = []
            for source_file in source_files_list:
                source_file_base = os.path.splitext(os.path.basename(source_file))[0]
                if source_file_base not in excluded_extensions and source_file != target_folder_path and source_file_base == file_name:
                    same_name_files.append(source_file)
            if same_name_files:
                same_list.append((same_name_files, target_folder_path))

    print("为以下目标文件建立符号链接:")
    for item in same_list:
        for source_file in item[0]:
            target_dir = item[1]
            cmd = ['mklink', os.path.join(target_dir, os.path.basename(source_file)), source_file]
            print('\n' + '-' * 50)
            print("\n"+"执行命令: " + ' '.join(cmd)+"\n")
            try:
                # os.system(" ".join(cmd))
                subprocess.check_call(cmd, shell=True)
                # output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
                # print("result: " + output+"\n")
                print("源文件路径: " + source_file)
                print("目标文件夹路径: " + target_dir)
            except Exception as e:
                print("符号链接创建失败: " + str(e))
    print("输入空格结束程序")
    input_str = input("")
    if input_str.isspace():
        sys.exit()
    else:
        print("非空格，程序继续.....")

# for target_folder in target_folders_lists:
#     file_name=os.path.splitext(os.path.basename(target_folder))[0]
#     same_name_files=[]
#     for source_file in source_files_lists:
#         source_file_base = os.path.splitext(os.path.basename(source_file))[0]
#         if source_file_base not in excluded_extensions and source_file != target_folder and source_file_base == file_name:
#             same_name_files.append(source_file)

def same_file_createsymbolic_links():

    tools.admin_process()
    # 定义源路径列表
    source_dirs = []
    while True:
        print("请输入文件路径或文件夹路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
        input_str = input()
        if not input_str.strip():  # 如果用户只输入了空格或者回车符，则结束输入
            break
        input_list = input_str.split('\n')  # 将输入字符串转换为列表，按行分割
        for path in input_list:
            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]  # 去除引号
            source_dirs.append(path)
    # 指定目标目录
    print("请输入要创建的目标目录：")
    target_dir = input().strip()
    # 遍历源路径列表，将文件和文件夹分别添加到不同的列表中
    files, folders = tools.get_listunder_fileandfolder(source_dirs)
    # # 输出结果
    # print('Files:')
    # for file_path in files:
    #     print(file_path)
    # print('Folders:')
    # for folder_path in folders:
    #     print(folder_path)
    # 遍历路径列表，为每个文件或文件夹创建符号链接
    for source_file in files:
        print("文件符号链接")
        # 构建mklink命令行
        # cmd = ['mklink', '"' + os.path.join(target_dir, os.path.basename(source_file)) + '"', '"' + source_file + '"']
        cmd = ['mklink', os.path.join(target_dir, os.path.basename(source_file)).replace('"', ''),
               source_file.replace('"', '')]
        print('\n' + '-' * 50)
        print("\n" + "执行命令: " + ' '.join(cmd) + "\n")
        try:
            subprocess.check_call(cmd, shell=True)
            # output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            # print("result: " + output + "\n")
            print("源文件路径: " + source_file)
            print("目标文件夹路径: " + target_dir)
        except Exception as e:
            print("符号链接创建失败: " + str(e))

    for source_file in folders:
        print("文件夹符号链接")
        # 构建mklink命令行
        # cmd = ['mklink', '"' + os.path.join(target_dir, os.path.basename(source_file)) + '"', '"' + source_file + '"']
        cmd = ['mklink', '/d', os.path.join(target_dir, os.path.basename(source_file)).replace('"', ''),
               source_file.replace('"', '')]
        print('\n' + '-' * 50)
        print("\n" + "执行命令: " + ' '.join(cmd) + "\n")
        try:
            subprocess.check_call(cmd, shell=True)
            # output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            # print("result: " + output + "\n")
            print("源文件路径: " + source_file)
            print("目标文件夹路径: " + target_dir)
        except Exception as e:
            print("符号链接创建失败: " + str(e))

    print("输入空格结束程序")
    input_str = input("")
    if input_str.isspace():
        sys.exit()
    else:
        print("非空格，程序继续.....")


def get_exclude_suffix_list():
    print("参数是否为文件列表 Y/N def:Y")
    flag = input()
    if "N" == flag.upper():
        print("请输入文件夹")
        path_folderdir = input()
        file_paths_list = tools.get_file_paths(path_folderdir)
        print("输入需要排除的后缀 多个参数用空格隔开")
        excluded_extensions = input()
        matching_files = tools.find_matching_files(file_paths_list, *excluded_extensions)
        if matching_files:
            print("Matching files:")
            for file_path in matching_files:
                print(file_path)
        else:
            print("No matching files found")
    else:
        file_paths_list = []
        while True:
            print("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
            path = input()
            # path = input("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
            if not path:
                break
            file_paths_list.append(path)
        print("输入需要排除的后缀")
        excluded_extensions = input()
        matching_files = tools.find_matching_files(file_paths_list, *excluded_extensions)

        if matching_files:
            print("Matching files:")
            for file_path in matching_files:
                print(file_path)
        else:
            print("No matching files found")
        return None


def get_filepathsort():
    rules=[]
    tools.get_sort_list(rules)
    return None


def getfiletypeislegal():
    print("请输入文件夹路径:")
    source_folder_path = input("")
    path=tools.get_file_paths(source_folder_path)
    # print(path)
    tools.check_file_access(path)
    return None


# def getsortsamefiles():
#     # 初始化一个空的字典，用于存储时长相同的文件路径列表
#     same_duration_dict = {}
#     print("输入要对比的文件夹")
#     lists=input()
#     path_list=tools.get_file_paths(lists)
#     # 初始化一个空的字典，用于存储时长相同的文件路径列表
#     same_duration_dict = {}
#     # 遍历文件路径列表并检查每个文件的时长
#     for path in path_list:
#         if path.endswith(".wav") or path.endswith(".flac") or path.endswith(".mp4") or path.endswith(".mp3"):
#             # 如果该文件是音频文件，则使用ffmpeg获取其时长
#             file_path = os.path.join(path).replace("'",'')
#
#             cmd = f"ffprobe -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file_path}"
#             output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
#             duration = float(output.strip())
#
#             # 如果字典中不存在键，则创建一个新的键并将路径添加到列表中
#             if duration not in same_duration_dict:
#                 same_duration_dict[duration] = [file_path]
#             # 如果键已存在，则将路径添加到现有列表
#             else:
#                 same_duration_dict[duration].append(file_path)
#
#     # 输出结果
#     for duration, file_paths in same_duration_dict.items():
#         if len(file_paths) > 1:
#             print(f"这些文件的时长为 {duration}:")
#             for path in file_paths:
#                 print(path)
def update_linked_items():
    # tools.admin_process()
    # source_folder=create_symbolic_links_recursive()
    print("请输入符号链接所在文件夹")
    source_folder = input()
    print("请输入要复制源文件到的所在文件夹")
    destination_folder = input()
    print("是否增量更新？def:N（是：则获取新增的文件。否：只更新索引下修改的文件)")
    flag=input() or 'N'
    # 获取源文件夹中的所有文件路径
    item_paths = tools.get_file_paths(source_folder)

    # 遍历每个文件路径
    for item_path in item_paths:
        # 检查路径是否是符号链接
        if os.path.islink(item_path):
            # 构建目标路径
            destination_path = os.path.join(destination_folder, os.path.basename(item_path))

            # 复制符号链接的源文件或文件夹到目标路径
            copy_source_update_from_symlink(item_path,destination_folder,flag)

def create_linked_items():
    # tools.admin_process()
    # source_folder=create_symbolic_links_recursive()
    print("请输入符号链接所在文件夹")
    source_folder = input()
    print("请输入要复制源文件到的所在文件夹")
    destination_folder = input()
    # 获取源文件夹中的所有文件路径
    item_paths = tools.get_file_paths(source_folder)

    # 遍历每个文件路径
    for item_path in item_paths:
        # 检查路径是否是符号链接
        if os.path.islink(item_path):
            # 构建目标路径
            destination_path = os.path.join(destination_folder, os.path.basename(item_path))

            # 复制符号链接的源文件或文件夹到目标路径
            copy_source_create_from_symlink(item_path,destination_folder)

def common_path(paths,destination_folder):
    # 如果路径为空，返回空
    if not paths:
        return ""

    # 将路径按分隔符分割
    parts_list = [os.path.normpath(path).split(os.path.sep) for path in paths]

    # 反转每个路径的部分，从最后一级开始比较
    reversed_parts_list = [list(reversed(parts)) for parts in parts_list]

    # 使用 zip 函数遍历路径的各级目录
    common_parts = []
    for level_parts in zip(*reversed_parts_list):
        if all(part == level_parts[0] for part in level_parts):
            common_parts.append(level_parts[0])
        else:
            break

    # 如果没有共同路径，返回空字符串
    if not common_parts:
        return ""

    # 反转共同路径，恢复正常顺序
    common_parts = list(reversed(common_parts))

    # 使用 os.path.join 合并共同路径
    common_path = os.path.join(*common_parts)
    # base_path = r"D:\Back\GameSaveBackup\test"
    base_path = destination_folder
    final_path = os.path.join(base_path, common_path)
    final_path = os.path.normpath(final_path)
    return final_path

def copy_source_update_from_symlink(symlink_path,destination_folder,flag):
    try:
        source_path = os.readlink(symlink_path)
        paths_list = [source_path, symlink_path]
        final_path = common_path(paths_list,destination_folder)
        current_date = datetime.now()
        yesterday = current_date - timedelta(days=1)
        try:
            if flag.upper()=='N':
                # 取出 common_path 最后一级前的内容
                common_parent = os.path.dirname(final_path)
                # print(source_path)
                # print(final_path)
                # 如果 final_path 已经存在，则直接复制文件
                # 获取文件修改时间
                file_mtime = os.path.getmtime(source_path)
                file_modified_date = datetime.fromtimestamp(file_mtime)
                # print(yesterday)
                # print(file_modified_date)
                #如果文件比当前日期的前一天晚，则更新
                if file_modified_date >= yesterday:
                    # 创建目录（如果不存在）
                    os.makedirs(os.path.dirname(common_parent), exist_ok=True)
                    if os.path.exists(final_path):
                        shutil.copy2(source_path, final_path)
                        print(f"Source file copied from '{source_path}' to '{final_path}'")
                    else:
                        # 创建目标文件夹
                        os.makedirs(common_parent, exist_ok=True)

                        # 复制文件夹
                        shutil.copy2(source_path, common_parent)
                        print(f"Source folder copied from '{source_path}' to '{final_path}'")
                # print(f"Source folder copied from '{source_path}' to '{common_parent}'")

            if flag.upper()=='Y':
                # 取出 common_path 最后一级前的内容
                common_parent = os.path.dirname(final_path)
                source_path=os.path.dirname(source_path)
                file_mtime = os.path.getmtime(source_path)
                # 获取文件修改时间
                file_modified_date = datetime.fromtimestamp(file_mtime)
                # print(yesterday)
                # print(file_modified_date)
                #如果文件比当前日期的前一天晚，则更新
                if file_modified_date >= yesterday:
                    if os.path.exists(common_parent):
                        shutil.rmtree(common_parent)
                        print(f"Remove folder from '{source_path}' to '{final_path}'")

                    # 确保 common_parent 存在后再进行复制
                    if not os.path.exists(common_parent):
                        # shutil.copytree(source_path, common_parent)
                        tools.copy_folder(source_path, common_parent)
                        print(f"Source folder copied from '{source_path}' to '{final_path}'")
                # print(f"Source folder copied from '{source_path}' to '{common_parent}'")
        except OSError as e:
            print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")

def copy_source_create_from_symlink(symlink_path,destination_folder):
    try:
        source_path = os.readlink(symlink_path)
        paths_list = [source_path, symlink_path]
        final_path = common_path(paths_list, destination_folder)
        try:
                # 取出 common_path 最后一级前的内容
                common_parent = os.path.dirname(final_path)
                # print(source_path)
                # print(final_path)
                # 如果 final_path 已经存在，则直接复制文件
                file_mtime = os.path.getmtime(source_path)
                file_modified_date = datetime.fromtimestamp(file_mtime)
                # 创建目录（如果不存在）
                os.makedirs(os.path.dirname(common_parent), exist_ok=True)
                if os.path.exists(final_path):
                    shutil.copy2(source_path, final_path)
                    print(f"Source file copied from '{source_path}' to '{final_path}'")
                else:
                    # 创建目标文件夹
                    os.makedirs(common_parent, exist_ok=True)

                    # 复制文件夹
                    shutil.copy2(source_path, common_parent)
                    print(f"Source folder copied from '{source_path}' to '{final_path}'")
        except OSError as e:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def check_symbolic_link():
    print("请输入要检查的符号链接所在文件夹")
    destination_folder = input()
    link_paths=tools.get_file_paths(destination_folder)
    relative_links = []
    absolute_links = []
    invalid_links = []
    for link_path in link_paths:
        try:
            # 检查路径是否是符号链接
            if os.path.islink(link_path):
                # print(f"{link_path} is a symbolic link.")

                # 读取符号链接的目标路径
                target_path = os.readlink(link_path)

                # 判断路径是否为绝对路径
                if os.path.isabs(target_path):
                    absolute_links.append(link_path)
                    absolute_links.append("target_path:"+target_path + "\n")
                else:
                    relative_links.append(link_path)
                    relative_links.append("target_path:"+target_path + "\n")

        except OSError as e:
            print(f"Error: {e}")
    # 打印分类结果
    print("\nRelative Symbolic Links:")
    print("-"*70)
    for link in relative_links:
        print(link)

    print("\nAbsolute Symbolic Links:")
    print("-"*70)
    for link in absolute_links:
        print(link)

    print("\nInvalid Symbolic Links:")
    print("-"*70)
    for link in invalid_links:
        print(link)


def create_symbolic_links_recursive():
    tools.admin_process()
    print("请输入符号链接所在文件夹")
    source_folder = input()
    print("请输入要缓存符号链接的文件夹")
    target_folder = input()

    # 遍历源文件夹中的所有文件和子文件夹
    # 遍历源文件夹中的所有文件和子文件夹
    # 遍历源文件夹中的所有文件
    for root, _, files in os.walk(source_folder):
        for file_name in files:
            source_file = os.path.join(root, file_name)

            try:
                # 获取符号链接所指向的源文件路径
                source_file_link = os.readlink(source_file)
                source_dir = os.path.join(root, os.path.dirname(source_file_link))
            except OSError:
                # 不是符号链接的情况，直接使用原路径
                source_dir = os.path.join(root, file_name)
                continue

            # 检查是否在同一文件系统上
            if os.stat(source_dir).st_dev != os.stat(source_folder).st_dev:
                source_dir = os.path.abspath(source_dir)

            # 构建在目标文件夹中对应的子文件夹路径

            # 假设 source_dir 和 source_folder 是两个文件夹的绝对路径
            source_dir = os.path.abspath(source_dir)
            source_folder = os.path.abspath(source_folder)
            path1 = 'C:\\Users\\zk\\AppData\\Roaming\\Cuphead'
            path2 = 'D:\\Back\\test'

            common_base = os.path.commonpath([path1, path2])
            relative_path1 = os.path.relpath(path1, common_base)
            relative_path2 = os.path.relpath(path2, common_base)

            print(relative_path1)
            print(relative_path2)
            # 将 source_dir 转换为相对于根目录的路径
            relative_path = os.path.relpath(source_dir, os.path.commonprefix([source_dir, source_folder]))

            # 构建在目标文件夹中对应的子文件夹路径
            relative_path = os.path.join(target_folder, relative_path)
            # relative_path = os.path.relpath(source_dir, source_folder)
            target_subfolder = os.path.join(target_folder, relative_path)

            # 创建目标子文件夹
            os.makedirs(target_subfolder, exist_ok=True)
            print(f"复制文件夹 {os.path.dirname(source_file_link)} 到 {target_subfolder}")

            # 创建符号链接
            target_file = os.path.join(target_subfolder, os.path.basename(source_file_link))
            cmd = ['mklink', target_file, source_file_link]
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    shell=True
                )
                out, err = process.communicate()
                print(f"为文件 {file_name} 创建了符号链接：{target_file}")
            except Exception as e:
                print(f"创建符号链接时出错：{e}")
    return target_folder







import concurrent.futures
import os
import asyncio
from functools import wraps

# def make_async(sync_func):
#     @wraps(sync_func)
#     async def async_func(*args, **kwargs):
#         loop = asyncio.get_event_loop()
#         return await loop.run_in_executor(None, partial(sync_func, *args, **kwargs))
#
#     return async_func
#
# def execute_async_function(async_func, *args, **kwargs):
#     loop = asyncio.get_event_loop()
#     return loop.create_task(async_func(*args, **kwargs))
#
# def run_async_task(async_func, *args, **kwargs):
#     loop = asyncio.get_event_loop()
#     return loop.run_until_complete(async_func(*args, **kwargs))
#
# def print_video_info_list_asy():
#     """输出视频文件的大小、时长、比特率和分辨率"""
#     print("选择场景：Y/N 文件路径列表(Y) 文件夹（N）")
#     flag=input() or 'n'
#     if flag.lower()=='y':
#         # 新增方法：获取文件路径列表
#         start=time.time()
#         print(start)
#         file_paths_list = []
#
#         while True:
#             print("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
#             path = input()
#             # path = input("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
#             if not path:
#                 break
#             file_paths_list.append(path.replace('"',''))
#         print("是否纯净输出y/n")
#         flag = input()
#         async_get_file_paths_list_limit=make_async(tools.get_file_paths_list_limit)
#         extensions =('.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
#             '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
#         '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
#         '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
#         task_get_file_paths= execute_async_function(async_get_file_paths_list_limit,*extensions)
#         folder=run_async_task(task_get_file_paths,*extensions)
#         # folder=tools.get_file_paths_list_limit(file_paths_list,'.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
#         #     '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
#         # '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
#         # '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
#     else:
#         try:
#             print("请输入视频文件夹")
#             folder = tools.process_input_str("")
#             print("是否纯净输出y/n")
#             flag = input()
#             async_get_file_paths_list_limit=make_async(tools.get_file_paths_list_limit)
#             extensions =('.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
#                 '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
#             '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
#             '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
#             task_get_file_paths= execute_async_function(async_get_file_paths_list_limit,*extensions)
#             folder=asyncio.run(task_get_file_paths)
#             # folder = tools.get_file_paths_limit(folder,'.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
#             #         '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
#             #     '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
#             #     '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
#         except Exception as e:
#             print(e)
#     if not folder:
#         print("文件为空，需检查条件或参数！")
#         return
#     video_info_list, max_path_len = tools.get_video_info_list(folder)
#     video_info_list= asyncio.run(execute_async_function)
#     for video_info in video_info_list:
#         path = video_info[0]
#         size = "{:.2f}MB".format(video_info[1])
#         duration = "{:.2f}min".format(video_info[2] / (60*60))
#         bitrate = "{:.2f}kbps".format(video_info[3] / 1024)
#         width = video_info[4]
#         height = video_info[5]
#         if (flag == 'y'.lower()):
#             print(path)
#         else:
#             print("{:<{}}{:<15}{:<15}{:<15}{:<15}".format(path, max_path_len, size, duration, bitrate, f"{width}x{height}"),
#               end="")
#             print(" " * (max_path_len - len(path) + 1))
#     end=time.time()
#     print(end)
#     print("cost:", end - start, "seconds")

def poolTool():
    pool = ThreadPoolExecutor(5)  #
    pool.submit()

import asyncio
import os
import time
from functools import partial, wraps

async def get_file_paths_limit(folder, *extensions):
    """获取文件夹下指定后缀的所有文件的路径"""
    paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(tuple(extensions)):
                path = os.path.join(root, file)
                paths.append(path)
    if not paths:
        print("未找到任何文件")
    return paths

async def get_video_details(path):
    """获取视频文件的详细信息"""
    if os.path.exists(path):
        probe = ffmpeg.probe(path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        # duration = float(video_stream['duration']) * 60
        duration = float(probe["format"]["duration"]) * 60
        bitrate = int(probe["format"]['bit_rate'])
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        # bitrate = int(video_stream['bit_rate'])
        # width = int(video_stream['width'])
        # height = int(video_stream['height'])
        return duration, bitrate, width, height

async def get_video_info_list(paths):
    # 异步获取视频信息的逻辑
    video_info_list = []
    max_path_len = 0

    for path in paths:
        try:
            duration, bitrate, width, height = await get_video_details(path)
            size = os.path.getsize(path) / (1024*1024)
            video_info_list.append((path, size, duration, bitrate, width, height))
            max_path_len = max(max_path_len, len(path))
            video_info_list.sort(key=lambda x: x[3])  # 按比特率排序
        except Exception as e:
            print(f"处理文件 {path} 时出错：{e}")
            continue

    return video_info_list, max_path_len

async def get_file_paths_list_limit(file_paths_list, *extensions):
    """获取文件列表中指定后缀的所有文件的路径"""
    paths = []
    for file_path in file_paths_list:
        file_ext = os.path.splitext(file_path)[1].lower().replace('"', '')
        if file_ext in extensions:
            paths.append(file_path)
    if not paths:
        print("未找到任何文件")
    return paths


async def main():
    start = time.time()
    print(start)

    print("选择场景：Y/N 文件路径列表(Y) 文件夹（N）")
    flag = input().lower() or 'n'

    if flag == 'y':
        print("请输入文件夹")
        folder = tools.process_input_str("")
        print("是否纯净输出y/n")
        flag = input().lower()

        extensions = ('.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
                      '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
                      '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
                      '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')

        file_paths_list = await get_file_paths_list_limit(folder, *extensions)
    else:
        try:
            print("请输入视频文件夹")
            folder = tools.process_input_str("")
            print("是否纯净输出y/n")
            flag = input().lower()

            extensions = ('.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
                          '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
                          '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
                          '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')

            file_paths_list = await get_file_paths_limit(folder, '.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
                          '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
                          '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
                          '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
        except Exception as e:
            print(e)
            return

    if not file_paths_list:
        print("文件为空，需检查条件或参数！")
        return

    video_info_list, max_path_len = await get_video_info_list(file_paths_list)

    for video_info in video_info_list:
        path, size, duration, bitrate, width, height = video_info
        size_str = "{:.2f}MB".format(size)
        duration_str = "{:.2f}min".format(duration / (60*60))
        bitrate_str = "{:.2f}kbps".format(bitrate / 1024)

        if flag == 'y':
            print(path)
        else:
            print("{:<{}}{:<15}{:<15}{:<15}{:<15}".format(path, max_path_len, size_str, duration_str, bitrate_str, f"{width}x{height}"),
                  end="")
            print(" " * (max_path_len - len(path) + 1))

    end = time.time()
    print(end)
    print("cost:", end - start, "seconds")

def print_video_info_list_asy():
    # 创建 cProfile 对象
    profiler = cProfile.Profile()

    # 启动性能分析
    profiler.enable()

    # 在主程序中运行主协程
    asyncio.run(main())

    # 将分析结果保存到文件或打印出来
    output = io.StringIO()
    stats = pstats.Stats(profiler, stream=output).sort_stats('cumulative')
    stats.print_stats()
    print(output.getvalue())




# 绝对路径
absolute_path = "C:\\Users\\Username\\Documents\\file.txt"
# 起始路径（通常是当前工作目录或另一个相对路径）
base_path = "C:\\Users\\Username\\Documents"

# 将绝对路径转为相对路径
relative_path = os.path.relpath(absolute_path, base_path)


def excel_compare():
    excel_path=input("请输入需要比较的CSV文件: ").replace('"', '')
    encode = tools.detect_encoding(excel_path)
    with open(excel_path, 'r', encoding=encode) as file:
        for _ in range(5):  # 读取前5行
            print(file.readline())
    folder_path=input("请输入需要比较的文件夹路径: ")
    size_threshold =input("请输入比较文件大小限制（def:200): ") or 200
    # excel_path = "Z:\\WizTree_20231209231054.csv"  # 替换为你的 Excel 文件路径
    # folder_path = "H:\\videos\EN_video(H)"  # 替换为你的文件夹路径
    size_threshold = size_threshold * 1024 * 1024  # 设置文件大小的阈值，单位为字节（这里是200MB）
    # flag=input("纠错模式：将会打印读取的关键字的行数 Y/N（无法读取开启 def:N): ") or 'N'
    # if flag.upper()=='Y':
    #     encode = detect_encoding(excel_path)
    #     with open(excel_path, 'r', encoding=encode) as file:
    #         for _ in range(5):  # 读取前5行
    #             print(file.readline())
    # 获取需要比较的列名列表
    compare_columns = input("请输入需要比较的列名，以逗号分隔: ").split(',')
    find_missing_files(excel_path, folder_path, size_threshold,compare_columns)

def find_missing_files(csv_path, folder_path, size_threshold,compare_columns):
    encode=tools.detect_encoding(csv_path)
    # 读取 CSV 文件，指定 encoding 参数为 'gbk'
    df_csv = None  # 将 df_excel 初始化为 None
    for header_row in range(0, 5):
        try:
            df_csv = pd.read_csv(csv_path, usecols=compare_columns, encoding=encode, header=header_row)
            # 如果成功读取，跳出循环
            print(f"成功以第 {header_row} 行作为列名。")
            break
        except ValueError as e:
            print(f"尝试以第 {header_row} 行作为列名时出错：{e}")

    # 如果 df_excel 未成功读取，给出错误信息并退出
    if df_csv is None:
        print("无法读取 Excel 文件。")
        return

    # 获取文件夹下所有文件
    all_files = [f for f in os.listdir(folder_path) if
                 os.path.isfile(os.path.join(folder_path, f)) and os.path.getsize(
                     os.path.join(folder_path, f)) > size_threshold]

    # 将文件名转为集合以便进行差异比较
    # csv_files = set(compare_columns)
    csv_files = set(df_csv[compare_columns])
    folder_files = set(all_files)

    # 查找在文件夹中有但在 CSV 中没有的文件
    extra_files_in_folder = folder_files - csv_files

    # 输出在 CSV 中没有但在文件夹中有的文件名
    if extra_files_in_folder:
        print("以下文件在 CSV 中没有但在文件夹中有:")
        for file_name in extra_files_in_folder:
            full_path = os.path.join(folder_path, file_name)
            print(full_path)
    else:
        print("所有在文件夹中的文件在 CSV 中都找到了。")