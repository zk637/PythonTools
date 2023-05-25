import ctypes
import os
import re

import ffmpeg
import subprocess
import contextlib
import sys

#输入参数为列表
def process_input_list():
    file_paths = []
    while True:
        path = input("请输入文件路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
        if not path:
            break
        file_paths.append(path.strip('"'))
    return file_paths

#输入参数为字符串
def process_input_str(s):
    str =""
    str=input()
    return str

#输入字符串且有“”包裹
def process_intput_strr(s):
    str=""
    str=input().replace('"', '')
    return str

def get_file_paths(folder):
    """获取文件夹下所有文件的路径"""
    paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            paths.append(path)
    return paths

def get_file_paths_limit(folder, *extensions):
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

# 通用指定后缀模糊匹配工具
def get_files_matching_pattern(folder_path,reg):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if re.search(reg, filename):
                file_path = os.path.join(root, filename)
                files.append(file_path)
    return files

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

def get_same_namefile(folder_path):
    all_files = []  # 用于保存所有文件路径

    # 获取所有文件路径
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file_name in filenames:
            file_path = os.path.join(dirpath, file_name)
            all_files.append(file_path)

    # 获取至少有两个相同文件名的路径
    file_name_dict = {}
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        file_name_dict.setdefault(file_name, []).append(file_path)

    same_name_files = [path for name, paths in file_name_dict.items() if len(paths) > 1 for path in paths]

    # 返回至少有两个相同文件名的路径
    return same_name_files

#通用去重工具
def DelRepat(data,key):
    new_data= []
    values =[]
    for d in data:
        if d[key] not in values:
            new_data.append(d)
            values.append(d[key])
    return new_data



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
    for file_name, file_data in files_by_name.items():
        if len(file_data["dirs"]) == 1:
            unique_files.extend(list(file_data["paths"]))
        else:
            all_paths = list(file_data["paths"])
            unique_files.extend(all_paths)
    return unique_files
#留重工具
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

#分别获取输入列表中的文件路径和文件夹路径
def get_listunder_fileandfolder(source_dirs):
    files = []
    folders = []
    for source_dir_path in source_dirs:
        # 获取每个路径的绝对路径
        abs_path = os.path.abspath(source_dir_path)
        if os.path.isfile(abs_path):
            files.append(abs_path)
        else:
            folders.append(abs_path)
    return files,folders

def read_rules_from_file():

    filename = "file_name_rules.txt"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            print("规则文件不存在，已创建空文件 file_name_rules.txt")
        return []

    with open(filename, encoding='utf-8') as f:
        try:
            content = f.read().strip()
        except Exception as e:
            print("Exception:", e)

    if not content:
        print("file_name_rules规则文件为空")
        return []

    rules = [rule.strip() for rule in content.split(",")]
    return rules

def get_video_details(path):
    """获取视频文件的详细信息"""

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

def get_video_info_list(paths):
    video_info_list = []
    max_path_len = 0
    # 属性编码字典
    attribute_map = {
        1: 'size',
        2: 'duration',
        3: 'bitrate',
    }
    # 手动录入排序属性的数字
    print("请输入排序属性的数字（1-size, 2-duration, 3-bitrate），默认为3-bitrate：")
    sort_index = int(input("") or 3)

    for path in paths:
        try:
            duration, bitrate, width, height = get_video_details(path)
            size = os.path.getsize(path) / (1024*1024)
            video_info_list.append((path, size, duration, bitrate, width, height))
            max_path_len = max(max_path_len, len(path))
            video_info_list.sort(key=lambda x: x[sort_index])  # 按比特率排序
        except Exception as e:
            print(f"处理文件 {path} 时出错：{e}")
            continue
    sort_attribute = attribute_map.get(sort_index)
    print(sort_attribute)

    return video_info_list, max_path_len

def get_file_count(folder):
    """获取文件夹下所有文件的数量"""
    return len(get_file_paths(folder))

def get_video_duration(video_path):
    """获取视频时长"""
    try:
        result = subprocess.check_output(
            ['ffprobe', '-i', video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")])
        duration = float(result)
        return duration
    except:
        print(f"Error: Failed to get duration of video {video_path}.")
        return 0

def getbitratesort(files):
    # 按比特率排序
    files_bitrate = []
    for file_path in files:
        # 检查文件是否存在
        if not os.path.isfile(file_path):
            print(f"File {file_path} not found, skipping")
            continue
        try:
            command = ['ffprobe', '-show_format', '-show_streams', '-of', 'json', file_path]

            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            if result.returncode != 0:
                print(f"ffprobe error (see stderr output for detail): {stderr.decode('utf-8')}")
            # fi=os.path.normpath(file_path)
            # print(fi)
            # quoted_file_path = '"' + file_path + '"'
            probe = ffmpeg.probe(file_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream is not None and 'bit_rate' in video_stream:
                bitrate = int(video_stream['bit_rate'])
                files_bitrate.append((file_path, bitrate))
            else:
                print(f"No video stream or bit rate information found in file {file_path}")
        except Exception as e:
            print(f"Error occurred while processing file {file_path}: {str(e)}")

    files_bitrate.sort(key=lambda x: x[1], reverse=True)
    sorted_files = [file_path for file_path, _ in files_bitrate]
    return sorted_files

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
        print("当前没有管理员权限，将尝试申请管理员权限并重新启动程序...")
        # 构建运行命令列表
        set_cmd_title("Tool_User")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        # 在新的进程中运行命令，等待命令执行完毕
        print("程序将重新启动...")
        # 重定向
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        # 用当前的可执行文件和命令行参数替代当前进程
        os.execl(sys.executable, *([sys.executable] + sys.argv))
        sys.exit()

def create_groups(lists,reg):
    lists_by_reg ={}
    for list in lists:
        try:
            path,temeame=os.path.splitext(list)
            var=os.path.basename(list)
            tempfilename=os.path.basename(list).split('.')[0]
            # tempfilename=tempfilename.index(1)
        except Exception as e:
            print(e)
        try:
            if path not in lists_by_reg:
                # 构建正则
                regf=re.compile(f""+tempfilename+reg+"")
                match=re.search(regf,var,flags=0)
            if not match:
                lists_by_reg[tempfilename] = {'count': 0, 'path': [], 'name': []}
            lists_by_reg[tempfilename]['count']+=1
            lists_by_reg[tempfilename]['path'].append(list)
            lists_by_reg[tempfilename]['name'].append(var)
        except Exception as e:
            print(e)
    ique_files = []
    # Traverse the dictionary
    for name, info in lists_by_reg.items():
        # If the name appears more than once
        if info['count'] > 1:
            # Add all the paths to the result list
            ique_files.extend(info['path'])
    return ique_files

#----------------------------------------------------------
def register_findone(lists, reg):
    lists_by_reg = {}
    # Traverse all the files
    final_name=os.path.basename(lists[0]).split('.')[0]
    # print(lists[0])
    for file_path in lists:
        try:
            tempfilename = os.path.basename(file_path).split('.')[0]
            if tempfilename not in lists_by_reg:
                lists_by_reg[tempfilename] = {
                    'count': 0,
                    'path': [],
                    'name': []
                }
            regf = re.compile(tempfilename + reg)
            match = regf.search(os.path.basename(file_path))
            if match and not final_name!=tempfilename:
                lists_by_reg[tempfilename]['count'] += 1
                lists_by_reg[tempfilename]['path'].append(file_path)
                lists_by_reg[tempfilename]['name'].append(os.path.basename(file_path))
        except Exception as e:
            print(e)

    # Traverse the dictionary
    ique_files = []
    for tempfilename, info in lists_by_reg.items():
        # If the name appears more than once
        if info['count'] > 1:
            # Add all the paths to the result list
            ique_files.extend(info['path'])
    return ique_files

def register_find(lists, reg):
    lists_by_reg = {}
    for file_path in lists:
        try:
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
            if match :
                lists_by_reg[tempfilename]['count'] += 1
                lists_by_reg[tempfilename]['path'].append(file_path)
                lists_by_reg[tempfilename]['name'].append(os.path.basename(file_path))
        except Exception as e:
            print(e)

    # Traverse the dictionary
    ique_files = []
    for tempfilename, info in lists_by_reg.items():
        # If the name appears more than once
        if info['count'] > 1:
            # Add all the paths to the result list
            ique_files.extend(info['path'])
    return ique_files
