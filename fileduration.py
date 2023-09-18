import ctypes
import os
import re
import shutil
import subprocess
import sys


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
    """输出视频文件的大小、时长、比特率和分辨率"""
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
    # 将 file_list 中的双引号去除
    file_list = [file.strip('"') for file in file_list]

    # 获取 file_list 中的文件名和文件夹名
    file_names, folder_names = tools.get_listunder_fileandfolder(file_list)

    paths = []
    for root, dirs, files in os.walk(folder_path):
        # 如果需要比较文件夹名，则只保留需要比较的文件夹
        for dir in dirs:
            for name in folder_names:
                if (os.path.basename(dir).lower()) == (os.path.basename(name).lower()):
                    path = os.path.join(root, dir)
                    paths.append(path)
    for root, dirs, files in os.walk(folder_path):
        # 如果需要比较文件名，则只保留需要比较的文件名
        for file in files:
            for name in file_names:
                if (os.path.basename(file).lower()) == (os.path.basename(name).lower()):
                    path = os.path.join(root, file)
                    paths.append(path)
    if not paths:
        # 如果没有找到匹配的文件，则输出提示信息并返回 None
        print("没有找到匹配的文件。")
        return None

    # 如果找到了匹配的文件，则输出每个文件的路径
    print("找到匹配的文件：")
    for file_path in paths:
        print('"' + f"{file_path}" + '"')
    return paths


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
    file_paths_list=[]
    while True:
        print("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
        path=input()
        # path = input("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
        if not path:
            break
        file_paths_list.append(path)
    print("输入需要排除的后缀")
    excluded_extensions=input()
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
