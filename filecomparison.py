import sys
import shutil
import pandas as pd
import subprocess
from flashtext import KeywordProcessor
import constants
import tools

# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler


def compare_and_move_files():
    """取传入目录下所有与文件名一致的jpg创建.ts文件夹并移入"""
    excluded_extensions = ['.dll', '.exe', 'png', '.xml', '.html', '.mp3']
    print("请输入需要对比的文件夹")
    folder_path = tools.process_input_str_limit()
    print("是否保留多个后缀比较【默认保留】")
    model = str(tools.process_input_str_limit() or 'y')
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
        if (model.lower() == 'y'):
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
                        f_path = shutil.copy(file, ts_dir)
                        jpg_files.remove(file)
                        # non_jpg_files.remove(non_jpg_file)
                        os.remove(file)
                    except Exception as e:
                        print(f'处理发生错误：{file}')
                        global_exception_handler(type(e), e, e.__traceback__)
                    # finally:
                    #     print(f'{f_path}')
                    # finally:
                    #     print(f'{file}n')


def check_files_in_folder(file_list):
    """获取给定文件夹下在检索路径列表中以相同文件名匹配的列表或获取不匹配相同文件名的列表"""
    # 提示用户输入目录路径
    print("请输入要检索的目录：")
    folder_path = tools.process_input_str_limit()
    print("只输出不匹配的文件？ Y/N def:N")
    flag = tools.process_input_str_limit() or "N"
    # 将 file_list 中的双引号去除
    file_list = [file.strip('"') for file in file_list]

    # 获取 file_list 中的文件名和文件夹名
    file_names, folder_names = tools.get_listunder_fileandfolder(file_list)

    matching_paths = []
    non_matching_paths = []
    if os.path.isdir(folder_path):
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
    else:
        print("输入参数有误！")
    if not matching_paths:
        # 如果没有找到匹配的文件，则输出提示信息并返回 None
        print("没有找到匹配的文件。")
        return None

    # 输出不匹配的文件路径
    if non_matching_paths and "Y" == flag.upper():
        non_matching_paths = set(non_matching_paths)
        print("找到不匹配的文件：")
        for file_path in non_matching_paths:
            print('"' + f"{file_path}" + '"')
    else:
        # 如果找到了匹配的文件，则输出每个匹配的文件的路径
        print("找到匹配的文件：")
        matching_paths = set(matching_paths)
        for file_path in matching_paths:
            print('"' + f"{file_path}" + '"')

    return matching_paths, non_matching_paths


def get_file_paths_with_rules():
    """
    获取文件夹下所有文件的路径，并返回文件名符合指定规则的文件路径列表
    :param folder: 文件夹路径
    :return: 符合规则的文件路径列表
    """
    print("请输入需要对比的文件夹")
    folder_path = tools.process_input_str_limit()
    file_name_rules = tools.read_rules_from_file()
    # 创建 KeywordProcessor 对象
    if not tools.check_is_None(folder_path):

        keyword_processor = KeywordProcessor()

        # 添加要查找的关键词列表
        keyword_processor.add_keywords_from_list(file_name_rules)

        paths = []
        # print(f"规则列表：{file_name_rules}")
        for root, dirs, files in os.walk(folder_path, topdown=False):
            # 处理文件夹名称
            for folder_name in dirs:
                folder_full_path = os.path.join(root, folder_name)
                if keyword_processor.extract_keywords(folder_name):
                    paths.append(folder_full_path)

            # 处理文件名称
            for file_name in files:
                file_full_path = os.path.join(root, file_name)
                file_name_without_ext, file_ext = os.path.splitext(file_name)
                if keyword_processor.extract_keywords(file_name_without_ext):
                    paths.append(file_full_path)

        # 打印匹配的路径
        for path in paths:
            print(path)


def create_symbolic_links():
    tools.admin_process()
    excluded_extensions = ['.dll', '.exe', '.png', '.xml', '.html', '.mp3', '.ts']
    print("请输入源文件夹路径:")
    source_folder_path = input("").strip()
    print("请输入目标文件夹路径:")
    target_folder_path = input("").strip()
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
            print("\n" + "执行命令: " + ' '.join(cmd) + "\n")
            # os.system(" ".join(cmd))
            subprocess.check_call(cmd, shell=True)
            # output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            # print("result: " + output+"\n")
            print("源文件路径: " + source_file)
            print("目标文件夹路径: " + target_dir)
    print("输入空格结束程序")
    input_str = input("")
    if input_str.isspace():
        sys.exit()
    else:
        print("非空格，程序继续.....")


def same_file_createsymbolic_links():
    tools.admin_process()
    # 定义源路径列表
    source_dirs = []
    print("请输入文件路径或文件夹路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
    while True:
        input_str = tools.process_input_str().strip('"')
        if not input_str.strip():  # 如果用户只输入了空格或者回车符，则结束输入
            break
        input_list = input_str.split('\n')  # 将输入字符串转换为列表，按行分割
        for path in input_list:
            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]  # 去除引号
            source_dirs.append(path)
    # 指定目标目录
    print("请输入要创建的目标目录：")
    target_dir = tools.process_input_str()
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
    files = [file for file in files if os.path.isfile(file)]
    folders = [folder for folder in files if os.path.isdir(folder)]

    for source_file in files:
        print("文件符号链接")
        tools.create_symbolic_link(source_file, target_dir)

    for source_folder in folders:
        print("文件夹符号链接")
        tools.create_symbolic_link(source_folder, target_dir, is_folder=True)

    print("输入空格结束程序")
    input_str = input("")
    if input_str.isspace():
        sys.exit()
    else:
        print("非空格，程序继续.....")


def get_file_paths_with_name():
    """获取检索文件夹下和检索文件名相同的路径列表"""
    # 获取用户输入的文件名列表和路径
    print(r"请输入需要检索的文件夹路径：")
    folderpath = tools.process_input_str_limit()
    found_files = []
    print(r"请输入需要检索的文件列表：")
    filenames_list = tools.process_input_list()
    # 获取指定路径下及其子目录下的所有文件路径
    if filenames_list and os.path.isdir(folderpath):
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
                file = tools.add_quotes_forpath(file)
                print(file)
        else:
            print("这些文件都不存在！")
    else:
        print("文件为空，需检查条件或参数！")
        return


def get_exclude_suffix_list():
    """获取不在指定后缀的文件路径（输入为路径列表或文件夹）"""
    path_list, dir = tools.process_paths_list_or_folder()
    print("是否检索子文件夹Y/N（默认不检索）")
    sub_folder_flag = tools.process_input_str_limit() or "N"
    file_list = []
    if path_list:
        file_list.extend(path_list)
    elif dir:
        file_list = tools.get_file_paths(dir)
    else:
        print("参数有误，不是合法的路径？")
        return
    print("输入需要排除的后缀 多个参数用空格隔开")
    excluded_extensions = input()
    matching_files = tools.find_matching_files_or_folder_exclude(file_list,
                                                                 flag=sub_folder_flag, *excluded_extensions)
    if matching_files:
        print("Matching files:")
        for file_path in matching_files:
            print(file_path)
    else:
        print("No matching files found")


def get_file_rule_sort():
    """过滤规则格式化"""
    rules, folder = tools.process_paths_list_or_folder()
    if folder:
        rules = tools.read_rules_from_file()
        tools.get_sort_list(rules)
    elif rules:
        tools.get_sort_list(rules)
    else:
        print("参数有误！")
        return None


def check_symbolic_link():
    """检查录入文件夹下的符号链接是否可用"""
    print("请输入要检查的符号链接所在文件夹")
    destination_folder = tools.process_input_str()
    link_paths = tools.get_file_paths(destination_folder)
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
                    absolute_links.append("target_path:" + target_path + "\n")
                else:
                    relative_links.append(link_path)
                    relative_links.append("target_path:" + target_path + "\n")

        except OSError as e:
            print(f"Error: {e}")
    # 打印分类结果
    print("\nRelative Symbolic Links:")
    print("-" * 70)
    tools.for_in_for_print(relative_links)

    print("\nAbsolute Symbolic Links:")
    print("-" * 70)
    tools.for_in_for_print(absolute_links)

    print("\nInvalid Symbolic Links:")
    print("-" * 70)
    tools.for_in_for_print(invalid_links)


def excel_compare():
    """文件夹内容与csv对比"""
    print("请输入需要比较的CSV文件: ")
    excel_path = tools.process_input_str_limit().replace('"', '')
    if not tools.check_is_None(excel_path):
        encode = tools.detect_encoding(excel_path)
        with open(excel_path, 'r', encoding=encode) as file:
            for _ in range(5):  # 读取前5行
                print(file.readline().strip())
        print("请输入需要比较的文件夹路径: ")
        folder_path = tools.process_input_str_limit()
        print("请输入比较文件大小限制（def:200): ")
        size_threshold = int(tools.process_input_str_limit() or 200)
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
        print("请输入需要比较的列名，以逗号分隔: ")
        compare_columns = tools.process_input_str_limit().split(',')
        print("是否输出CSV和文件夹都有的内容 Y/N (def:N) :")
        flag = tools.process_input_str_limit() or 'N'
        find_missing_files(excel_path, folder_path, size_threshold, compare_columns, flag)


def get_file_paths(folder, size_threshold):
    """获取文件夹下满足大小阈值的所有文件的路径"""
    paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            if os.path.getsize(path) > size_threshold:
                paths.append(path)
    return paths


def find_missing_files(csv_path, folder_path, size_threshold, compare_columns, flag):
    if csv_path and folder_path and size_threshold and compare_columns:
        encode = tools.detect_encoding(csv_path)
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
        # all_files = [f for f in os.listdir(folder_path) ifG:\Videos\3d
        #              os.path.isfile(os.path.join(folder_path, f)) and os.path.getsize(
        #                  os.path.join(folder_path, f)) > size_threshold]
        all_files = get_file_paths(folder_path, size_threshold)
        csv_files = set(df_csv[compare_columns].values.flatten())

        # 遍历目标列的值
        matche_lists = []
        no_matche_lists = []

        # 提取csv_files中每个元素的文件名，存入新的集合
        csv_files_names = set(csv_file.split('\\')[-1] for csv_file in csv_files)

        # 遍历文件列表，逐个与目标字符串比较
        for file in all_files:
            file_base_name = os.path.basename(file)

            # 获取文件名的集合
            file_name_set = {file_base_name}

            # 取两个集合的差集
            unmatched_set = file_name_set - csv_files_names
            # 如果差集不为空，表示找到了CSV中没有的内容
            if unmatched_set:
                matche_lists.append(file)
            if flag.upper() == 'Y':
                # 取两个集合的并集
                matched_set = file_name_set.intersection(csv_files_names)
                if matched_set:
                    no_matche_lists.append(file)

        # 输出匹配结果
        if matche_lists:
            print("以下内容文件夹中有但CSV文件中没有：")
            tools.for_in_for_print(matche_lists)
        else:
            print("没有任何匹配的结果")

        if flag.upper() == 'Y':
            if no_matche_lists:
                print('\n' + '-' * 100)
                print("以下内容文件夹中和CSV中都存在：")
                tools.for_in_for_print(no_matche_lists)
        else:
            print("没有任何匹配的结果")


def rename_with_dir():
    """文件夹下视频命名规范化"""
    print("请输入要重命名的文件夹： ")
    path = tools.process_input_str_limit()
    if not tools.check_is_None(path):
        files = tools.get_file_paths_limit(path, *constants.VIDEO_SUFFIX)
        for file in files:
            rename_file(file)


def rename_file(filepath):
    if os.path.isfile(filepath):
        filename, file_extension = os.path.splitext(os.path.basename(filepath))
        year_part = filename[:4]  # 修改这里以确保获取正确的年份部分
        rest_part = filename[4:]

        # 确保年份是数字
        if year_part.isdigit():
            # 首字母大写
            words = rest_part.split()
            words[0] = words[0].capitalize()
            rest_part = ' '.join(words)

            new_name = f"{rest_part} ({year_part}){file_extension}"
            new_path = os.path.join(os.path.dirname(filepath), new_name)
            os.rename(filepath, new_path)
            print(f"已将文件 {filename} 重命名为 {new_name}")
        else:
            print(f"无法获取有效的年份部分于文件 {filename}")
    else:
        print(f"{filepath} 不是一个有效的文件路径")


# ---------------------------------------------------------------

import io
import os
import time
import ffmpeg
import pstats
import asyncio
import cProfile
from concurrent.futures import ThreadPoolExecutor


def poolTool():
    pool = ThreadPoolExecutor(5)  #
    pool.submit()


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
            size = os.path.getsize(path) / (1024 * 1024)
            video_info_list.append((path, size, duration, bitrate, width, height))
            max_path_len = max(max_path_len, len(path))
            video_info_list.sort(key=lambda x: x[3])  # 按比特率排序
        except Exception as e:
            print(f"处理文件 {path} 时出错：{e}")
            global_exception_handler(type(e), e, e.__traceback__)
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
    flag = tools.process_input_str().lower().strip() or 'n'

    if flag == 'y':
        print("请输入文件夹")
        folder = tools.process_input_str()
        print("是否纯净输出y/n")
        flag = tools.process_input_str().lower()

        file_paths_list = await get_file_paths_list_limit(folder, *constants.VIDEO_SUFFIX)
    else:
        print("请输入视频文件夹")
        folder = tools.process_input_str()
        print("是否纯净输出y/n")
        flag = tools.process_input_str().lower()

        file_paths_list = await get_file_paths_limit(folder, *constants.VIDEO_SUFFIX)

    if not file_paths_list:
        print("文件为空，需检查条件或参数！")
        return

    video_info_list, max_path_len = await get_video_info_list(file_paths_list)

    for video_info in video_info_list:
        path, size, duration, bitrate, width, height = video_info
        size_str = "{:.2f}MB".format(size)
        duration_str = "{:.2f}min".format(duration / (60 * 60))
        bitrate_str = "{:.2f}kbps".format(bitrate / 1024)

        if flag == 'y':
            print(path)
        else:
            print("{:<{}}{:<15}{:<15}{:<15}{:<15}".format(path, max_path_len, size_str, duration_str, bitrate_str,
                                                          f"{width}x{height}"),
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


def get_directories_and_copy_tree():
    """获取指定文件夹下的目录结构"""
    print("请输入需要复制目录结构的文件夹")
    folder = tools.process_input_str_limit()
    print("请输入要复制结构到的文件夹")
    point_folder = tools.process_input_str_limit()
    """
    获取给定文件夹中的所有子文件夹，并将其复制到指定文件夹中。
    """

    if os.path.isdir(folder) and os.path.isdir(point_folder):
        # 构造目标文件夹路径，注意这里需要使用 point_folder 作为根路径
        target_dir = os.path.join(point_folder, os.path.basename(folder))
        # 创建目标文件夹
        os.makedirs(target_dir, exist_ok=True)
        print(f"Directory copied from '{folder}' to '{target_dir}'")

        # 获取除起始文件夹外的所有子文件夹
        directories = []
        for root, dirs, files in os.walk(folder):
            for dir_name in dirs:
                directories.append(os.path.join(root, dir_name))

        if directories:
            for directory in directories:
                # 构造目标文件夹路径，注意这里使用最初的目标文件夹作为基路径
                target_subdir = os.path.join(target_dir, os.path.relpath(directory, folder))
                # 创建目标文件夹
                os.makedirs(target_subdir, exist_ok=True)
                print(f"Directory copied from '{directory}' to '{target_subdir}'")

    else:
        print("目录不存在，或不是目录")
