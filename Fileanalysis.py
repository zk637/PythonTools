import io
import os
import cProfile
import pstats
import time

from PIL import Image
import cv2
import tools
import constants
from datetime import datetime



def get_low_resolution_media_files():
    """通过视频目录查找符合区间条件分辨率的媒体文件"""
    print("-----------------------请输入第一个分辨率阈值（格式为 宽*高）：--------------------------")
    size_limit1 = input("")
    width_limit1, height_limit1 = map(int, size_limit1.split("*"))

    print("-----------------------请输入第二个分辨率阈值（格式为 宽*高）:--------------------------")
    size_limit2 = input("")
    width_limit2, height_limit2 = map(int, size_limit2.split("*"))

    if width_limit1 > width_limit2:
        width_limit1, width_limit2 = width_limit2, width_limit1
    if height_limit1 > height_limit2:
        height_limit1, height_limit2 = height_limit2, height_limit1

    print(f"分辨率区间阈值：{width_limit1}*{height_limit1}~{width_limit2}*{height_limit2}")

    print("请输入视频文件夹：")
    path = tools.process_input_str("")
    print("比特率排序Y/N")
    flag = input()
    files = []
    for file_path in tools.get_file_paths(path):
        _, ext = os.path.splitext(file_path)
        if ext.lower() in ('.mp4', '.avi', '.mkv', '.jpg', '.jpeg', '.png', '.gif'):
            try:
                if ext.lower() in ('.mp4', '.avi', '.mkv'):
                    cap = cv2.VideoCapture(file_path)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cap.release()
                    if width * height >= width_limit1 * height_limit1 and width * height <= width_limit2 * height_limit2:
                        files.append(file_path)
                elif ext.lower() in ('.jpg', '.jpeg', '.png', '.gif'):
                    width, height = Image.open(file_path).size
                    if width >= width_limit1 and height >= height_limit1 and width <= width_limit2 and height <= height_limit2:
                        files.append(file_path)
            except Exception as e:
                print(f"Error occurred while processing file {file_path}: {str(e)}")
    if ('Y' == flag.upper()):
        try:
            files = tools.getbitratesort(files)
            files=tools.add_quotes_forpath(files)
            print("分辨率符合要求的媒体文件列表（按比特率由大到小排序）：")
            print("\n".join(files))
        except Exception as e:
            print(f"Error occurred while sorting files by bitrate: {str(e)}")
    else:
        print("分辨率符合要求的媒体文件列表：")
        files = tools.add_quotes_forpath(files)
        print("\n".join(files))

def get_video_duration_sorted():
    """获取文件夹下所有视频文件的时长并排序输出"""
    print("请输入视频文件夹")
    folder = tools.process_input_str("")
    folder_flag=True
    if not os.path.isdir(folder):
        folder_flag=False
        paths = tools.process_input_list()
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
                folder, *constants.VIDEO_SUFFIX)
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
            folder, *constants.VIDEO_SUFFIX)
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

def print_video_info_list():
    # 创建 cProfile 对象
    profiler = cProfile.Profile()
    # 启动性能分析
    profiler.enable()
    """输出视频文件的大小、时长、比特率和分辨率（支持文件列表和文件夹）"""

    file_paths_list,video_dir=tools.process_paths_list_or_folder()
    if file_paths_list:
        print("是否纯净输出y/n")
        flag = input()
        start = time.time()
        print(start)
        folder = tools.get_file_paths_list_limit(file_paths_list, *constants.VIDEO_SUFFIX)
    elif os.path.isdir(video_dir):
        print("是否纯净输出y/n")
        flag = input()
        start = time.time()
        print(start)
        folder = tools.get_file_paths_limit(video_dir,*constants.VIDEO_SUFFIX)
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


def get_video_audio():
    """
     获取给定文件夹或文件的音频文件（支持文件列表和文件夹）
     """
    file_paths_list,folder=tools.process_paths_list_or_folder()
    if file_paths_list:
        folder = tools.get_file_paths_list_limit(file_paths_list, *constants.VIDEO_SUFFIX)
    elif os.path.isdir(folder):
        folder = tools.get_file_paths_limit(folder, *constants.VIDEO_SUFFIX)
    if not folder:
        print("文件为空，需检查条件或参数！")
        return
    for path in folder:
        tools.convert_video_to_mp3(path)
    print("队列执行完成")

def getfiletypeislegal():
    """校验文件是否合法"""
    print("请输入文件夹路径:")
    source_folder_path = input("")
    path=tools.get_file_paths(source_folder_path)
    # print(path)
    tools.check_file_access(path)
    return None

def split_video():
    """
     根据限制大小拆分视频为多段（支持文件列表和文件夹）
     """
    input_video_list,input_video_dir=tools.process_paths_list_or_folder()
    if input_video_list:
        print("拆分后每段文件的大小限制 单位：MB")
        max_size_mb = int(input()) * 1024 * 1024

        output_dir = r'H:\spilt_parts_dir'
        tools.make_dir(output_dir)
        for input_video in input_video_list:
            if input_video != '':
                part_num = round(os.path.getsize(input_video) / max_size_mb, 2)
                if part_num > 1:
                    part_max_size = os.path.getsize(input_video) / (os.path.getsize(input_video) / max_size_mb)
                    tools.split_video_for_size(part_max_size, part_num, input_video, output_dir)
                else:
                    print(f"文件无法拆分：{input_video}")
    elif os.path.isdir(input_video_dir):
        filename, file_extension = os.path.splitext(input_video_dir)

        output_dir = os.path.join(filename, 'spilt_parts_dir')
        tools.make_dir(output_dir)

        print("拆分后每段文件的大小限制 单位：MB")
        max_size_mb = int(input()) * 1024 * 1024
        input_video_list = tools.get_file_paths_limit(input_video_dir, *constants.VIDEO_SUFFIX)
        if input_video_list is not None:
            for input_video in input_video_list:
                free_space = tools.get_free_space_cmd(input_video_dir)
                if free_space > os.path.getsize(input_video):
                    part_num = round(os.path.getsize(input_video) / max_size_mb, 2)
                    if part_num > 1:
                        part_max_size = os.path.getsize(input_video) / part_num
                        tools.split_video_for_size(part_max_size, part_num, input_video, output_dir)
                    else:
                        print(f"文件无法拆分：{input_video}")
    else:
        print("参数有误，不是合法的路径？")

def add_srt():
    """为视频文件添加字幕"""
    print("输入视频文件路径")
    video_path=input().replace('"','')
    print("输入字幕文件路径")
    srt_path=input().replace('"','')
    print("硬字幕还是软字幕 Y/N def:N")
    flag=input() or 'N'
    if os.path.isfile(video_path):
        dir_path = os.path.dirname(video_path)
        # base_name = os.path.basename(video_path).split('.')[0]
        base_name, extension = os.path.splitext(video_path.split('\\')[-1])
        print(base_name)
        # 构建输出文件名
        video_out_name = f"{base_name}_CN.mp4"
        video_out_name = os.path.join(dir_path, video_out_name)
        bat_file=''
    if flag.upper()=='Y':
            # 定义 FFmpeg 命令
            #可用格式 ffmpeg -i "H:\videos\test\Dracula _1080p.mp4" -vf subtitles="'H\:\\videos\\test\\Dracula.zh.utf8.srt'" "Dracula_1080p_CN.mp4"
            # 'ffmpeg -i H:\\videos\\test\\Dracula _1080p.mp4 -c:v h264_nvenc -vf subtitle=H\\:\\videos\\test\\Dracula.zh.utf8.srt H:\\videos\\test\\Dracula _1080p_CN.mp4'
            srt_path = srt_path.replace('\\', r'\\').replace(':', r'\:')
            # video_path = video_path.replace('\\','\\\\')
            # print(video_path)
            srt_path="'"+srt_path+"'"
            # print(srt_path)
            command=f'ffmpeg -i "{video_path}" -c:v h264_nvenc -vf subtitles="{srt_path}" "{video_out_name}"'
            print(command)
            bat_file=tools.generate_bat_script("run_addSrt.bat",command)
            tools.subprocess_common_bat(bat_file,command)
    else:
            # 定义 FFmpeg 命令
            command=f'ffmpeg -i "{video_path}" -i "{srt_path}" -map 0:v -map 0:a -map 1:s:0 -c:v copy -c:a copy -c:s mov_text -disposition:s:0 forced "{video_out_name}"'
            bat_file=tools.generate_bat_script("run_addSrt.bat",command)
            result=tools.subprocess_common_bat(bat_file,command)
            print(result)

def check_files_subtitle_stream():
    """
     检查视频是否存在字幕流（支持文件列表和文件夹）
     """
    video_paths_list,video_dir=tools.process_paths_list_or_folder()
    if video_paths_list:
        for video_path in video_paths_list:
            tools.check_subtitle_stream(video_path)
    elif os.path.isdir(video_dir):
        video_lists = tools.find_matching_files_or_folder_exclude(folder=video_dir, *constants.EXTENSIONS)
        for video_path in video_lists:
            tools.check_subtitle_stream(video_path)
    else:
        print("参数有误，不是合法的路径？")


def check_video_integrity():
    """
     获取指定文件列表或文件夹下的视频是否完整（支持文件列表和文件夹）
     """
    video_paths_list,video_dir=tools.process_paths_list_or_folder()
    if video_paths_list:
        for video_path in video_paths_list:
            tools.get_video_integrity(video_path)
    elif os.path.isdir(video_dir):
        video_lists = tools.find_matching_files_or_folder_exclude(folder=video_dir, *constants.EXTENSIONS)
        for video_path in video_lists:
            tools.get_video_integrity(video_path)
    else:
        print("参数有误，不是合法的路径？")
