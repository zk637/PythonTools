import os
import re
import tools
# 关键词匹配字幕

def getSrt():
    # 匹配的关键字，这里假设匹配文件名中包含"abc"的视频文件和字幕文件
    # keywords = "010115_001"
    print(print("-----------------------输入keyword：--------------------------"))
    keywords=input("")
    print("请输入视频文件夹路径")
    video_folder=tools.process_input_str("")
    print("请输入字幕文件夹路径")
    subtitle_folder=tools.process_input_str("")
    # 遍历视频文件夹中的所有文件
    match_list = []
    path_list = []
    for video_file in os.listdir(video_folder):
        # 判断是否为视频文件
        if video_file.endswith(('.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg', '.mpe', '.m1v', '.m2v',
            '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv', '.mp4', '.m4v',
        '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram', '.rmvb', '.rpm', '.flv', '.mov',
        '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm', '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')):
            # 获取视频文件名中包含关键字的部分
            video_name = os.path.splitext(video_file)[0]
            if keywords in video_name:
                # 匹配到关键字，尝试查找匹配的字幕文件
                subtitle_path = get_file_paths(subtitle_folder)
                for subtitle_file in subtitle_path:
                    # 判断是否为字幕文件
                    if subtitle_file.endswith((".ts",".srt",".ass",".ssa",".vtt",".sub",".sub",".smi",".mpl",".rt",""
                                ".dfxp",".lrc",".pjs",".usf",".rtf",".sup",".pgs",".sub",".sup")):
                        # 获取字幕文件名中包含关键字的部分
                        subtitle_name = os.path.splitext(os.path.basename(subtitle_file))[0]
                        if keywords in subtitle_name:
                            # 匹配到关键字，输出匹配的视频和字幕文件路径
                            match_list.append(f"Match found: {video_file} <--> {os.path.basename(subtitle_file)}")
                            path_list.append(subtitle_file)

    # 打印匹配列表
    print('\n'.join(match_list))
    print('-' * 150)
    # # 打印路径列表
    print('\n'.join(path_list))


# 匹配文件夹下视频与字幕对应 并输出列表
def getSrtNew():

    # video_dir = "/path/to/video/directory"
    # subtitles_dir = "/path/to/subtitles/directory"
    print("请输入视频文件夹路径")
    video_folder=tools.process_input_str("")
    print("请输入字幕文件夹路径")
    subtitle_folder=tools.process_input_str("")
    # match_files(video_folder, subtitle_folder)
    process_files(video_folder, subtitle_folder)

def get_file_paths(folder):
    """获取文件夹下所有文件的路径"""
    paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            paths.append(path)
    return paths


def process_files(video_folder, subtitle_folder):
    # 获取视频文件名列表
    video_files = os.listdir(video_folder)

    # 获取所有字幕文件路径
    subtitle_paths = get_file_paths(subtitle_folder)

    match_list = []
    path_list = []

    for video_file in video_files:
        # 提取视频文件名中的关键词
        # match = re.search(r"\b\d{2,3}\b|[\d_]{3,7}\b", video_file, re.UNICODE)
        # match = re.search(r"[\w\s\-\(\)\.\'\[\]]+", video_file, re.UNICODE)
        # match =re.search( r"\b\d{1,3}\b|\b\d{3}\b|\b\d{4}\b",video_file, re.UNICODE)
        match =re.search(r"\b\d+\b|\((.*?)\)|(?<=-)\d+(?=\.)|(?<=\.)\d+(?=\s)",video_file, re.UNICODE)
        if match:
            keyword = match.group(0).lower()
            # 在字幕文件中查找匹配的文件路径
            for subtitle_path in subtitle_paths:
                subtitle_file = os.path.basename(subtitle_path).lower()
                if keyword in subtitle_file:
                    # 如果视频文件也存在，则保存匹配结果
                    video_path = os.path.join(video_folder, video_file)
                    if os.path.exists(video_path):
                        match_list.append(f"Match found: {video_file} <--> {subtitle_file}")
                        path_list.append(subtitle_path)
                        break

    # 打印匹配列表
    print('\n'.join(match_list))
    print('-' * 150)
    # 打印路径列表
    print('\n'.join(path_list))