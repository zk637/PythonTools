import ctypes
import os
import re
import chardet
from difflib import SequenceMatcher

import ffmpeg
import filetype
import subprocess
import contextlib
import locale
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

def add_quotes_forpath(s):
    str='"'+s+'"'
    return str

def make_dir(s):
    try:
        os.makedirs(s, exist_ok=True)
        if os.path.exists(s):
            print(f"Folder '{s}' created successfully.")
    except Exception as e:
        print(e)

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

def get_file_paths_list_limit(file_paths_list, *extensions):
    """获取文件列表中指定后缀的所有文件的路径"""
    paths = []
    for file_path in file_paths_list:
        file_ext = os.path.splitext(file_path)[1].lower().replace('"', '')
        if file_ext in extensions:
            paths.append(file_path)
    if not paths:
        print("未找到任何文件")
    return paths

def find_matching_files(paths, *extensions):
    """获取指定路径列表下所有与指定后缀不匹配的文件路径"""
    extensions = [e.lower() for e in extensions]  # 将所有后缀名转换为小写
    matching_files = []
    print("是否检索文件夹Y/N（默认不检索）")
    try:
        flag = input() or "n"
    except Exception as e:
        flag = "n"
    try:
        for path in paths:
            if os.path.isfile(path):
                path, ext = os.path.splitext(path)
                if ext.lower() in extensions:
                    continue
                dir_path = os.path.dirname(path)
                for filename in os.listdir(dir_path):
                    if not filename.startswith(os.path.basename(path)) or filename.lower().endswith(tuple(extensions)):
                        continue
                    matching_files.append(os.path.join(dir_path, filename))
            elif os.path.isdir(path):
                if flag.lower()=='y':
                    for root, dirs, files in os.walk(path):
                        for filename in files:
                            path, ext = os.path.splitext(filename)
                            if ext.lower() not in extensions:
                                matching_files.append(os.path.join(root, filename))
            else:
                raise ValueError(f"{path} is not a valid directory or file path")
    except Exception as e:
        print(e)
    return matching_files



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

#检查文件类型是否合法
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
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        encode=result['encoding']
        return check_encoding(encode)
def check_encoding(s):
    lowercase_s = s.lower()
    if lowercase_s.startswith("gb"):
        return "gbk"
    else:
        return s

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

    # Output files with "Cannot determine file type" error
    if results['cannot_determine_type']:
        print("Errors with 'Cannot determine file type':")
        for file_path in results['cannot_determine_type']:
            print(file_path)
        print("_" * 30)  # Print a line to separate categories

    # Output files with successful "File type" determined
    if results['has_file_type']:
        print("Files with 'File type':")
        for file_data in results['has_file_type']:
            print(f"{file_data['file_path']} (File type: {file_data['file_type']})")
        print("_" * 30)  # Print a line to separate categories

    # Output files where no type determined
    if results['no_type_determined']:
        print("Files with no type determined:")
        for file_path in results['no_type_determined']:
            print(file_path)
        print("_" * 30)  # Print a line to separate categories

    # Output files with errors
    if results['error_files']:
        print("Files with errors:")
        for file_data in results['error_files']:
            print(f"{file_data['file_path']}\nError: {file_data['error_message']}")
        print("_" * 30)  # Print a line to separate categories

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

def subprocess_common(command, shell=True, capture_output=True, text=True):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # 输出命令的详细信息
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def subprocess_common_bat(bat_file, command, shell=False, capture_output=True, text=True):
    try:
        # 将命令和批处理文件名组合成一个字符串
        command_with_bat = f'{bat_file} {command}'
        print(command_with_bat)
        # 调用批处理文件并传递命令作为参数
        process = subprocess.Popen(command_with_bat, shell=shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=text)

        # 获取标准输出和标准错误
        stdout, stderr = process.communicate()

        # 输出命令的详细信息
        print(stdout)
        print(stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def subprocess_with_progress(command, shell=True):
    # 启动子进程
    print(command)
    process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    print(process)
    process.communicate()

#TODO 更加多样的参数逻辑支持
def generate_bat_script(bat_file, command):
    # 检查批处理文件是否已存在
    if os.path.exists(bat_file):
        return bat_file

    # 打开批处理文件以写入模式
    with open(bat_file, 'w') as f:
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
    try:
        subprocess.run(['rmdir', '/s', '/q', folder_path], check=False)
        print(f"Folder {folder_path} deleted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def copy_folder(source_folder, destination_folder):
    try:
        # 使用 robocopy 命令进行文件夹复制
        result = subprocess.run(['robocopy', source_folder, destination_folder, '/E', '/XO', '/COPY:DAT', '/R:3', '/W:5'], check=False, capture_output=True, text=True, encoding='latin-1')

        # print(result.stdout)
        # print(result.stderr)
        print(f"Folder copied from '{source_folder}' to '{destination_folder}'")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

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
    # print("Debug: Paths before processing:", paths)
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
        print(f'{rule}')
        # print(f'{len(rule)}: {rule}')

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

def convert_video_to_mp3(video_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]+'.mp3'
    video_final_path=os.path.join(os.path.dirname(video_path),video_name)
    try:
        subprocess.run(
            ['ffmpeg', '-i', video_path, '-f', 'mp3', '-vn', video_final_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        print(f"转换成功：{video_name}.mp3")
    except subprocess.CalledProcessError as e:
        print(f"转换失败：{video_path}")
        print(f"错误输出：{e.stderr.decode()}")

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

def seconds_to_hhmmss(seconds):
    # 将秒数转换为时分秒格式
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
            print("File does not exist.")
            return None
    except ffmpeg.Error as e:
        print(f"Error probing file: {e}")
        return None

def split_video_for_size(part_max_size,part_num,output_prefix,output_dir):
    video_info = get_video_info(output_prefix)
    if video_info is not None:
        duration, video_bitrate, audio_bitrate, width, height = video_info
        part_max_duration = part_max_size * 8 / (video_bitrate + audio_bitrate)
        # 格式化分段最大时长为 HH:MM:SS 格式
        part_max_duration_formatted = seconds_to_hhmmss(part_max_duration)
        print(f"格式化后的最大时长: {part_max_duration_formatted}")
        # 添加标志以指示是否存在已存在的文件
        existing_file_found = False

        output_prefix_tmp = output_prefix
        output_prefix_tmp=output_prefix_tmp.replace("'",'-')
        filename, file_extension = os.path.splitext(output_prefix_tmp)
        output_prefix_tmp=filename
        output_prefix_tmp.replace('.mp4','')

        part_index = output_prefix.rfind('_part')
        if part_index != -1:
            # 截取字符串，保留 '_part' 之前的部分
            output_prefix_tmp = output_prefix[:part_index]
            output_prefix_tmp=output_prefix_tmp.replace('.mp4','')
            # print("Original Name:", output_prefix_tmp)
        else:
            print("File name doesn't contain '_part'.")
        part_index=0
        for part_index in range(int(part_num)):
            output_prefix_tmp = f"{output_prefix_tmp}_part{part_index + 1}.mp4"
            if os.path.isfile(output_prefix_tmp):
                print(f"Skipping existing file: {output_prefix_tmp}(找到一个已存在的文件就会跳出循环)")
                existing_file_found = True
                output_prefix_tmp=''
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
                processed_output_prefix+ '_part%d.mp4'
            ]

            # 使用 subprocess.run 运行拆分命令
            subprocess.run(split_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,encoding='utf-8')


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
        #ffprobe -v error -select_streams s -show_entries stream=index,codec_name -of default=noprint_wrappers=1:nokey=1 "H:\videos\test.mp4"
        command = ['ffprobe', '-v', 'error', '-select_streams', 's', '-show_entries', 'stream=index,codec_name', '-of',
                   'default=noprint_wrappers=1:nokey=1', video_path]
        # print(command)
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            if output:
                print("True:", f"true=文件{video_path}：存在字幕流")
            else:
                print("False:", f"文件{video_path}：不存在字幕流")
        except subprocess.CalledProcessError as e:
            print("Error:", f"文件{video_path}：无法获取视频信息")
            print(e.output)
            return False

#----------------------------------------------------------
def register_findone(lists, reg):
    lists_by_reg = {}
    # Traverse all the files
    final_name=os.path.basename(lists[0]).split('.')[0]
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
def get_free_space_cmd(folder_path):
    # 提取文件夹所在磁盘的根目录
    #TODO 多语言环境兼容
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
            print("未找到剩余空间信息")
            return 1/0

