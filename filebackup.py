'''
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license

'''
import os
import sys
import tools
import shutil
import subprocess
from datetime import datetime, time, timedelta

# 注册模块对象
from model import tips_m, log_info_m, result_m

# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler


def same_file_createsymbolic_links():
    """获取两个目录下所有路径，源文件的文件名和目标文件的文件夹名一致则建立符号链接（需管理员权限）"""
    tools.admin_process()
    excluded_extensions = ['.dll', '.exe', '.png', '.xml', '.html', '.mp3', '.ts']
    tips_m.print_message(message="请输入源文件夹路径:")
    source_folder_path = tools.process_input_str_limit()
    tips_m.print_message(message="请输入目标文件夹路径:")
    target_folder_path = tools.process_input_str_limit()
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

    log_info_m.print_message(message="为以下目标文件建立符号链接:")
    for item in same_list:
        for source_file in item[0]:
            target_dir = item[1]
            cmd = ['mklink', os.path.join(target_dir, os.path.basename(source_file)), source_file]
            log_info_m.print_message(message='\n' + '-' * 50)
            log_info_m.print_message(message="\n" + "执行命令: " + ' '.join(cmd) + "\n")
            try:
                # os.system(" ".join(cmd))
                subprocess.check_call(cmd, shell=True)
                # output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
                # print("result: " + output+"\n")
                result_m.print_message(message="源文件路径: " + source_file)
                result_m.print_message(message="目标文件夹路径: " + target_dir)
            except Exception as e:
                print("符号链接创建失败: " + str(e))
                global_exception_handler(type(e), e, e.__traceback__)
    tips_m.print_message(message="输入空格结束程序")
    input_str = tools.process_input_str_limit()
    if input_str.isspace():
        sys.exit()
    else:
        log_info_m.print_message(message="非空格，程序继续.....")


def create_symbolic_links():
    """为指定的文件列表在指定目录下创建符号链接（需管理员权限）支持文件和文件夹混合"""
    tools.admin_process()
    # 定义源路径列表
    source_dirs = []
    tips_m.print_message(message="请输入文件路径或文件夹路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
    while True:
        input_str = tools.process_input_str()
        if not input_str.strip():  # 如果用户只输入了空格或者回车符，则结束输入
            break
        input_list = input_str.split('\n')  # 将输入字符串转换为列表，按行分割
        for path in input_list:
            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]  # 去除引号
            source_dirs.append(path)
    # 指定目标目录
    tips_m.print_message(message="请输入要创建的目标目录：")
    target_dir = tools.process_input_str_limit()
    # 遍历源路径列表，将文件和文件夹分别添加到不同的列表中
    files, folders = tools.get_listunder_fileandfolder(source_dirs)

    # 遍历路径列表，为每个文件和文件夹创建符号链接
    process_files_and_folders(files, folders, target_dir)

    print("输入空格结束程序")
    input_str = input("")
    if input_str.isspace():
        print("手动终止程序\n")
        sys.exit()
    else:
        print("非空格，程序继续.....")


def create_symlink(source, target, is_dir=False):
    link_type = '/d' if is_dir else ''
    log_info_m.print_message(message="文件夹符号链接" if is_dir else "文件符号链接")

    cmd = ['mklink', link_type, os.path.join(target, os.path.basename(source)), source]
    log_info_m.print_message(message='\n' + '-' * 50)
    log_info_m.print_message(message="\n执行命令: " + ' '.join(cmd) + "\n")

    try:
        subprocess.check_call(cmd, shell=True)
        result_m.print_message(message="源文件路径: " + source)
        result_m.print_message(message="目标文件夹路径: " + target)
    except Exception as e:
        result_m.print_message(message="符号链接创建失败: " + str(e))
        global_exception_handler(type(e), e, e.__traceback__)


def process_files_and_folders(files, folders, target_dir):
    for source_file in files:
        create_symlink(source_file, target_dir)

    for source_folder in folders:
        create_symlink(source_folder, target_dir, is_dir=True)


def update_linked_items():
    """文件自动备份（更新-需提前创建符号链接）"""
    # tools.admin_process()
    # source_folder=create_symbolic_links_recursive()
    tips_m.print_message(message="请输入符号链接所在文件夹")
    source_folder = input()
    tips_m.print_message(message="请输入要复制源文件到的所在文件夹")
    destination_folder = input()
    tips_m.print_message(message="是否增量更新？def:N（是：则获取新增的文件。否：只更新索引下修改的文件)")
    flag = input() or 'N'
    # 获取源文件夹中的所有文件路径
    item_paths = tools.get_file_paths(source_folder)

    # 遍历每个文件路径
    for item_path in item_paths:
        # 检查路径是否是符号链接
        if os.path.islink(item_path):
            # 构建目标路径
            destination_path = os.path.join(destination_folder, os.path.basename(item_path))

            # 复制符号链接的源文件或文件夹到目标路径
            copy_source_update_from_symlink(item_path, destination_folder, flag)


def create_linked_items():
    """文件自动备份（创建-需提前创建符号链接）"""
    # tools.admin_process()
    # source_folder=create_symbolic_links_recursive()
    tips_m.print_message(message="请输入符号链接所在文件夹")
    source_folder = tools.process_input_str_limit()
    tips_m.print_message(message="请输入要复制源文件到的所在文件夹")
    destination_folder = tools.process_input_str_limit()
    # 获取源文件夹中的所有文件路径
    item_paths = tools.get_file_paths(source_folder)

    # 遍历每个文件路径
    for item_path in item_paths:
        # 检查路径是否是符号链接
        if os.path.islink(item_path):
            # 构建目标路径
            destination_path = os.path.join(destination_folder, os.path.basename(item_path))

            # 复制符号链接的源文件或文件夹到目标路径
            copy_source_create_from_symlink(item_path, destination_folder)


def common_path(paths, destination_folder):
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


def copy_source_update_from_symlink(symlink_path, destination_folder, flag):
    try:
        source_path = os.readlink(symlink_path)
        paths_list = [source_path, symlink_path]
        final_path = common_path(paths_list, destination_folder)
        current_date = datetime.now()
        yesterday = current_date - timedelta(days=1)
        try:
            if flag.upper() == 'N':
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
                # 如果文件比当前日期的前一天晚，则更新
                if file_modified_date >= yesterday:
                    # 创建目录（如果不存在）
                    os.makedirs(os.path.dirname(common_parent), exist_ok=True)
                    if os.path.exists(final_path):
                        shutil.copy2(source_path, final_path)
                        result_m.print_message(message=f"Source file copied from '{source_path}' to '{final_path}'")
                    else:
                        # 创建目标文件夹
                        os.makedirs(common_parent, exist_ok=True)

                        # 复制文件夹
                        shutil.copy2(source_path, common_parent)
                        result_m.print_message(message=f"Source folder copied from '{source_path}' to '{final_path}'")
                # print(f"Source folder copied from '{source_path}' to '{common_parent}'")

            if flag.upper() == 'Y':
                # 取出 common_path 最后一级前的内容
                common_parent = os.path.dirname(final_path)
                source_path = os.path.dirname(source_path)
                file_mtime = os.path.getmtime(source_path)
                # 获取文件修改时间
                file_modified_date = datetime.fromtimestamp(file_mtime)
                # print(yesterday)
                # print(file_modified_date)
                # 如果文件比当前日期的前一天晚，则更新
                if file_modified_date >= yesterday and common_parent != destination_folder:
                    if os.path.exists(common_parent):
                        shutil.rmtree(common_parent)
                        result_m.print_message(message=f"Remove folder from '{source_path}' to '{final_path}'")

                    # 确保 common_parent 存在后再进行复制
                    if not os.path.exists(common_parent):
                        # shutil.copytree(source_path, common_parent)
                        tools.copy_folder(source_path, common_parent)
                        result_m.print_message(message=f"Source folder copied from '{source_path}' to '{final_path}'")
                # print(f"Source folder copied from '{source_path}' to '{common_parent}'")
        except OSError as e:
            log_info_m.print_message(message=f"Error: {e}")

    except Exception as e:
        global_exception_handler(type(e), e, e.__traceback__)


def copy_source_create_from_symlink(symlink_path, destination_folder):
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
                result_m.print_message(message=f"Source file copied from '{source_path}' to '{final_path}'")
            else:
                # 创建目标文件夹
                os.makedirs(common_parent, exist_ok=True)

                # 复制文件夹
                shutil.copy2(source_path, common_parent)
                result_m.print_message(message=f"Source folder copied from '{source_path}' to '{final_path}'")
        except OSError as e:
            log_info_m.print_message(message=f"Error: {e}")
    except Exception as e:
        global_exception_handler(type(e), e, e.__traceback__)
