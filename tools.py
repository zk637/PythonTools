import ctypes
import os
import ffmpeg
import subprocess
import contextlib
import sys


def process_input_list():
    file_paths = []
    while True:
        path = input("请输入文件路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
        if not path:
            break
        file_paths.append(path.strip('"'))
    return file_paths

def process_input_str(s):
    str =""
    str=input()
    return str

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

