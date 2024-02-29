import io
import os
import cProfile
import pstats
from PIL import Image
import cv2
import tools
from datetime import datetime,time



def get_low_resolution_media_files():
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
        paths = []
        while True:
            print("请输入文件路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
            path = input()
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

def get_video_audio():
    print("选择场景：Y/N 文件路径列表(Y) 文件夹（N）")
    flag = input() or 'n'
    if flag.lower() == 'y':
        # 新增方法：获取文件路径列表
        file_paths_list = []

        while True:
            print("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
            path = input()
            # path = input("请输入文件名，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
            if not path:
                break
            file_paths_list.append(path.replace('"', ''))
        # print("是否纯净输出y/n")
        # flag = input()
        folder = tools.get_file_paths_list_limit(file_paths_list, '.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg',
                                                 '.mpeg', '.mpe', '.m1v', '.m2v',
                                                 '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm',
                                                 '.ogv', '.mp4', '.m4v',
                                                 '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm',
                                                 '.ram', '.rmvb', '.rpm', '.flv', '.mov',
                                                 '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g',
                                                 '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v',
                                                 '.mxf')
    else:
        print("请输入视频文件夹")
        folder = tools.process_input_str("")
        folder = tools.get_file_paths_limit(folder, '.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe',
                                            '.m1v', '.m2v',
                                            '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv',
                                            '.mp4', '.m4v',
                                            '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram',
                                            '.rmvb', '.rpm', '.flv', '.mov',
                                            '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm',
                                            '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
    if not folder:
        print("文件为空，需检查条件或参数！")
        return
    for path in folder:
        tools.convert_video_to_mp3(path)
    print("队列执行完成")

def getfiletypeislegal():
    print("请输入文件夹路径:")
    source_folder_path = input("")
    path=tools.get_file_paths(source_folder_path)
    # print(path)
    tools.check_file_access(path)
    return None
