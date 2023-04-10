import os
import sys
import ffmpeg
import subprocess
import contextlib

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
    """获取视频文件的信息列表"""
    video_info_list = []
    max_path_len = 0
    for path in paths:
        try:
            duration, bitrate, width, height = get_video_details(path)
            size = os.path.getsize(path) / (1024*1024)
            video_info_list.append((path, size, duration, bitrate, width, height))
            max_path_len = max(max_path_len, len(path))
            video_info_list.sort(key=lambda x: x[3])  # 按时长排序
        except Exception as e:
            print(f"处理文件 {path} 时出错：{e}")
            continue
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

def capture_output_to_file(func):
    def wrapper(*args, **kwargs):
        with open('output.txt', 'a', encoding='utf-8') as f:
            # f.write(os.linesep.join(output))
            with contextlib.redirect_stdout(f):
                func(*args, **kwargs)
    return wrapper

