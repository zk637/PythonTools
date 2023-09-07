import os
import re
import shutil
import tools
# 复制字幕文件到视频文件下
def find_subtitle():

    # video_path=input("请输入视频路径:")
    # video_path = input("请输入视频路径: ").replace('"', '')
    # subtitles_foldern=input("请输入字幕文件夹路径:")
    # shlex.split(subtitles_foldern)
    print("请输入视频路径")
    video_path=tools.process_intput_strr("请输入视频路径:")
    print("请输入字幕文件夹路径")
    subtitles_folder=tools.process_input_str("请输入字幕文件夹路径:")
    # 提取视频文件名中的关键字
    video_filename = os.path.basename(video_path)
    match = re.search(r"\b\w+\b|\((.*?)\)", video_filename)
    if match:
        keyword = match.group(0)
    else:
        return None

    # 构造字幕文件名的正则表达式
    subtitle_pattern = re.compile(f"^{keyword}.*\.srt$")

    # 遍历字幕文件夹，查找匹配的字幕文件
    for filename in os.listdir(subtitles_folder):
        if subtitle_pattern.match(filename):
            subtitle_path = os.path.join(subtitles_folder, filename)

            # 获取视频文件所在目录和字幕文件名
            video_folder = os.path.dirname(video_path)
            new_subtitle_name = os.path.basename(subtitle_path)
            # print(video_folder)
            # 拼接新的字幕文件路径
            new_subtitle_path = os.path.join(os.path.dirname((video_path)), new_subtitle_name)
            # print(new_subtitle_path)
            # 复制字幕文件到视频文件所在路径的前一级目录
            shutil.copy(subtitle_path, new_subtitle_path)
            if subtitle_path:
                print(f"找到匹配的字幕文件：{subtitle_path}")
            else:
                print("没有找到匹配的字幕文件。")
            return new_subtitle_path

    # 没有找到匹配的字幕文件
    return None


def find_matching_subtitles():
    print("请输入视频路径")
    video_path = tools.process_intput_strr("").strip()
    print("请输入字幕文件夹路径")
    subtitles_folder = tools.process_input_str("").strip()

    # 遍历字幕文件夹获取所有的字幕文件路径
    # subtitle_files = tools.get_file_paths(subtitles_folder)
    subtitle_files = tools.get_file_paths_limit(subtitles_folder,".ts",".srt",".ass",".ssa",".vtt",".sub",".sub",".smi",".mpl",".rt",""
                                ".dfxp",".lrc",".pjs",".usf",".rtf",".sup",".pgs",".sub",".sup")
    # 匹配视频关键字获取对应的字幕文件
    video_file = os.path.basename(video_path)
    match = re.search(r"\b\w+\b|\((.*?)\)", video_file)
    keyword = match.group(0)
    match2 = re.search(r"(.+)(?=\.\w+$)", video_file)
    keyword2 = match2.group(0)
    # 构造字幕文件名的正则表达式
    # subtitle_pattern = re.compile(f".*{keyword}.*\.srt$")
    # subtitle_pattern2 =re.compile(f".*{keyword2}.*\.srt$")
    subtitle_pattern = re.compile(f".*{keyword}.*")
    subtitle_pattern2 = re.compile(f".*{keyword2}.*")
    print(subtitle_pattern)
    # subtitle_pattern = re.compile(f"^{keyword}.*\.srt$")
    # 遍历字幕文件夹，查找匹配的字幕文件
    precise_matching_subtitles = []  # 用于保存精确匹配的字幕文件路径的列表
    slur_matching_subtitles = []  # 用于保存模糊匹配的字幕文件路径的列表
    for filename in subtitle_files:
        if subtitle_pattern2.search(filename):
            subtitle_path = os.path.join(subtitles_folder, filename)
            precise_matching_subtitles.append(subtitle_path)
        elif subtitle_pattern.search(filename):
            subtitle_path = os.path.join(subtitles_folder, filename)
            slur_matching_subtitles.append(subtitle_path)

    if not precise_matching_subtitles and not slur_matching_subtitles:
        # 没有找到匹配的字幕文件
        print("没有找到匹配的字幕文件。")
    else:
        # 打印匹配的字幕文件路径列表，并在每个路径后添加换行符
        if slur_matching_subtitles:
            print("模糊匹配的字幕文件：")
            for subtitle_path in slur_matching_subtitles:
                # print(subtitle_path)
                print(tools.add_quotes_forpath(subtitle_path))
            print()  # 打印空行以实现换行效果
        if precise_matching_subtitles:
            print("精确匹配的字幕文件：")
            for subtitle_path in precise_matching_subtitles:
                # print(subtitle_path)
                print(tools.add_quotes_forpath(subtitle_path))
            print()  # 打印空行以实现换行效果

# 复制字幕文件到新创建的文件夹下
def find_matching_subtitles_create():

    print("请输入视频路径")
    video_path = tools.process_intput_strr("").strip()
    print("请输入字幕文件夹路径")
    subtitles_folder = tools.process_input_str("").strip()

    # 遍历字幕文件夹获取所有的字幕文件路径
    subtitle_files = tools.get_file_paths_limit(subtitles_folder,".ts",".srt",".ass",".ssa",".vtt",".sub",".sub",".smi",".mpl",".rt",""
                                ".dfxp",".lrc",".pjs",".usf",".rtf",".sup",".pgs",".sub",".sup")

    # 匹配视频关键字获取对应的字幕文件
    video_file = os.path.basename(video_path)
    match = re.search(r"\b\w+\b|\((.*?)\)", video_file)
    keyword = match.group(0)

    # 构造字幕文件名的正则表达式

    keyword_escaped = re.escape(keyword)
    # subtitle_pattern = re.compile(f"^{keyword_escaped}.*\\.srt$")
    subtitle_pattern = re.compile(f".*{keyword}.*")
    print(subtitle_pattern)
    # subtitle_pattern = re.compile(f"^{keyword}.*\.srt$")
    # 遍历字幕文件夹，查找匹配的字幕文件
    subtitle_path = None
    while not subtitle_path:
        for filename in subtitle_files:
            if subtitle_pattern.match(filename):
                subtitle_path = os.path.join(subtitles_folder, filename)
                break

        if subtitle_path is None:
            # 没有找到匹配的字幕文件
            print("没有找到匹配的字幕文件。")
            return None
        else:
            # 尝试打开字幕文件，如果文件已被占用，则设置 subtitle_path 为 None 并重试
            try:
                with open(subtitle_path, "r", encoding="utf-8") as f:
                    pass
            except IOError:
                subtitle_path = None

    # 获取视频文件所在路径的前一级路径
    parent_folder = os.path.dirname(video_path)

    # 创建与视频文件同名的文件夹
    video_file_no_ext = os.path.splitext(video_file)[0]
    target_folder = os.path.join(parent_folder, video_file_no_ext)
    os.makedirs(target_folder, exist_ok=True)

    # # 将字幕文件复制到目标文件夹中
    # target_subtitle_path = os.path.join(target_folder, os.path.basename(subtitle_path))
    # shutil.copy(subtitle_path, target_subtitle_path)

    print(f"找到匹配的字幕文件：{subtitle_path}")
    # return target_subtitle_path


