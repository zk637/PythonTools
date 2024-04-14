import os
import re
import shutil

import constants
import tools
from fuzzywuzzy import fuzz
from flashtext import KeywordProcessor

# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler


# 复制字幕文件到视频文件下
def find_subtitle():
    # video_path=input("请输入视频路径:")
    # video_path = input("请输入视频路径: ").replace('"', '')
    # subtitles_foldern=input("请输入字幕文件夹路径:")
    # shlex.split(subtitles_foldern)
    print("请输入视频路径")
    video_path = tools.process_intput_strr("请输入视频路径:")
    print("请输入字幕文件夹路径")
    subtitles_folder = tools.process_input_str()
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
    """通过视频路径查找字幕文件列表（支持模糊匹配）   """
    print("请输入视频路径")
    video_path = tools.process_input_str_limit().strip()
    print("请输入字幕文件夹路径")
    subtitles_folder = tools.process_input_str_limit().strip()
    if os.path.isfile(video_path) and os.path.isdir(subtitles_folder):
        # 遍历字幕文件夹获取所有的字幕文件路径
        # subtitle_files = tools.get_file_paths(subtitles_folder)
        SRT_SUFFIX = constants.SRT_SUFFIX
        subtitle_files = tools.get_file_paths_limit(subtitles_folder, *SRT_SUFFIX)

        # 匹配视频关键字获取对应的字幕文件
        video_file = os.path.basename(video_path)
        video_rule = video_file.strip().split('_')
        print(video_rule[0])
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keyword(video_rule[0])

        slur_matching_subtitles = []  # 用于保存模糊匹配的字幕文件路径的列表
        for filename in subtitle_files:
            if keyword_processor.extract_keywords(filename):
                subtitle_path = os.path.join(subtitles_folder, filename)
                slur_matching_subtitles.append(subtitle_path)

        if not slur_matching_subtitles:
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
    else:
        print("参数有误，路径为空？")


def find_matching_subtitles_create():
    """通过视频路径查找字幕文件并创建目录"""
    print("请输入视频路径")
    video_path = tools.process_input_str_limit().strip()
    print("请输入字幕文件夹路径")
    subtitles_folder = tools.process_input_str_limit().strip()
    if not tools.check_is_None(video_path, subtitles_folder):
        # 遍历字幕文件夹获取所有的字幕文件路径
        SRT_SUFFIX = constants.SRT_SUFFIX
        subtitle_files = tools.get_file_paths_limit(subtitles_folder, *SRT_SUFFIX)

        # 匹配视频关键字获取对应的字幕文件
        video_file = os.path.basename(video_path)
        video_rule = video_file.strip().split('_')
        print(video_rule[0])
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keyword(video_rule[0])

        # subtitle_pattern = re.compile(f"^{keyword}.*\.srt$")
        # 遍历字幕文件夹，查找匹配的字幕文件
        subtitle_path = None
        while not subtitle_path:
            for filename in subtitle_files:
                if keyword_processor.extract_keywords(filename):
                    subtitle_path = os.path.join(subtitles_folder, filename)
                    break

            if subtitle_path is None:
                # 没有找到匹配的字幕文件
                print("没有找到匹配的字幕文件。")
                return None
            else:
                # 尝试打开字幕文件，如果文件已被占用，则设置 subtitle_path 为 None 并重试
                try:
                    encode = tools.detect_encoding(subtitle_path)
                    with open(subtitle_path, "r", encoding=encode) as f:
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
        target_subtitle_path = os.path.join(target_folder, os.path.basename(subtitle_path))
        tools.copy_file(subtitle_path, target_subtitle_path)
        print(f"找到匹配的字幕文件：{subtitle_path}")
        # return target_subtitle_path


def getSrt():
    """使用关键词来查找字幕文件和匹配的媒体文件"""
    # 匹配的关键字，这里假设匹配文件名中包含"abc"的视频文件和字幕文件
    # keywords = "Romeo and Juliet"
    print("请输入keyword：")
    keywords = tools.process_input_str_limit()
    print("请输入视频文件夹路径")
    video_folder = tools.process_input_str_limit()
    print("请输入字幕文件夹路径")
    subtitle_folder = tools.process_input_str_limit()
    if keywords and os.path.isdir(video_folder) and os.path.isdir(subtitle_folder):
        # 遍历视频文件夹中的所有文件
        match_list = []
        path_list = []
        VIDEO_SUFFIX = constants.VIDEO_SUFFIX
        video_file_list = tools.get_file_paths_limit(video_folder, *VIDEO_SUFFIX)
        SRT_SUFFIX = constants.SRT_SUFFIX
        subtitle_list = tools.get_file_paths_limit(subtitle_folder, *SRT_SUFFIX)

        keyword_processor = KeywordProcessor()
        regex_pattern = re.escape(keywords)

        for subtitle_path in subtitle_list:
            subtitle_file = os.path.basename(subtitle_path)
            srt_keyword = re.findall(regex_pattern, subtitle_file)
            if srt_keyword:
                srt_keyword = ''.join(srt_keyword)
                for video_file in video_file_list:
                    video_file = os.path.basename(video_file)
                    video_rule = video_file.strip().split('_')
                    # print(video_rule[0])
                    keyword_processor.add_keyword(video_rule[0])
                    if srt_keyword in video_rule:
                        # 如果视频文件也存在，则保存匹配结果
                        video_path = os.path.join(video_folder, video_file)
                        if os.path.exists(video_path):
                            match_list.append(f"Match found: {video_file} <--> {subtitle_file}")
                            path_list.append(subtitle_path)
        if match_list:
            match_list = set(match_list)
            tools.for_in_for_print(match_list)
        print('-' * 150)
        if path_list:
            path_list = set(path_list)
            tools.for_in_for_print(path_list)
    else:
        print("参数有误，路径为空？")


# 匹配文件夹下视频与字幕对应 并输出列表
def getSrtNew():
    """匹配视频目录下对应的字幕文件并返回列表"""
    # video_dir = "/path/to/video/directory"
    # subtitles_dir = "/path/to/subtitles/directory"
    print("请输入视频文件夹路径")
    video_folder = tools.process_input_str_limit()
    print("请输入字幕文件夹路径")
    subtitle_folder = tools.process_input_str_limit()
    # match_files(video_folder, subtitle_folder)
    if os.path.isdir(video_folder) and os.path.isdir(subtitle_folder):
        process_files(video_folder, subtitle_folder)
    else:
        print("参数有误，路径为空？")


def get_file_paths(folder):
    """获取文件夹下所有文件的路径"""
    paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            # paths.append(path)
            paths.append(tools.add_quotes_forpath(path))
    return paths


# TODO
def process_files(video_folder, subtitle_folder):
    # 获取视频文件名列表
    VIDEO_SUFFIX = constants.VIDEO_SUFFIX
    video_files = tools.get_file_paths_limit(video_folder, *VIDEO_SUFFIX)

    # 获取所有字幕文件路径
    SRT_SUFFIX = constants.SRT_SUFFIX
    subtitle_paths = tools.get_file_paths_limit(subtitle_folder, *SRT_SUFFIX)

    match_list = []
    path_list = []
    keyword_processor = KeywordProcessor()

    for video_file in video_files:
        video_file = os.path.basename(video_file)
        video_rule = video_file.strip().split('_')
        # print(video_rule[0])
        keyword_processor.add_keyword(video_rule[0])
        # print(keyword)# 提取第一个关键词
        for subtitle_path in subtitle_paths:
            subtitle_file = os.path.basename(subtitle_path)
            keyword = keyword_processor.extract_keywords(subtitle_file)
            if keyword:
                # 如果视频文件也存在，则保存匹配结果
                video_path = os.path.join(video_folder, video_file)
                if os.path.exists(video_path):
                    match_list.append(f"Match found: {video_file} <--> {subtitle_file}")
                    path_list.append(subtitle_path)

    if match_list:
        match_list = set(match_list)
        # 打印匹配列表
        tools.for_in_for_print(match_list)
    print('-' * 150)
    if path_list:
        path_list = set(path_list)
        # 打印路径列表
        tools.for_in_for_print(path_list)


# def process_files(video_folder, subtitle_folder):
#     # 获取视频文件名列表
#     VIDEO_SUFFIX = constants.VIDEO_SUFFIX
#     video_files = tools.get_file_paths_limit(video_folder, *VIDEO_SUFFIX)
#
#     # 获取所有字幕文件路径
#     SRT_SUFFIX = constants.SRT_SUFFIX
#     subtitle_paths = tools.get_file_paths_limit(subtitle_folder, *SRT_SUFFIX)
#
#     match_list = []
#     path_list = []
#
#     for video_file in video_files:
#         # 提取视频文件名中的关键词
#         # match = re.search(r"\b\d{2,3}\b|[\d_]{3,7}\b", video_file, re.UNICODE)
#         # match = re.search(r"[\w\s\-\(\)\.\'\[\]]+", video_file, re.UNICODE)
#         # match =re.search( r"\b\d{1,3}\b|\b\d{3}\b|\b\d{4}\b",video_file, re.UNICODE)
#         match =re.search(r"\b\d+\b|\((.*?)\)|(?<=-)\d+(?=\.)|(?<=\.)\d+(?=\s)",video_file, re.UNICODE)
#         if match:
#             keyword = match.group(0).lower()
#             # 在字幕文件中查找匹配的文件路径
#             for subtitle_path in subtitle_paths:
#                 subtitle_file = os.path.basename(subtitle_path).lower()
#                 if keyword in subtitle_file:
#                     # 如果视频文件也存在，则保存匹配结果
#                     video_path = os.path.join(video_folder, video_file)
#                     if os.path.exists(video_path):
#                         match_list.append(f"Match found: {video_file} <--> {subtitle_file}")
#                         path_list.append(subtitle_path)
#                         break
#
#     if match_list:
#         match_list=set(match_list)
#         for match_tip in match_list:
#             # 打印匹配列表
#             print(match_tip)
#     print('-' * 150)
#     if path_list:
#         path_list=set(path_list)
#         for path in path_list:
#             # 打印路径列表
#             print(path)


# # 加载 spaCy 模型
# nlp = spacy.load("en_core_web_sm")


def preprocess_text(text):
    # 将.、_、-替换为空格
    cleaned_text = re.sub(r'[._-]', ' ', text)
    # 使用正则表达式过滤掉非字母和数字的字符
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_text)
    return cleaned_text


# def create_file_map(files, exclusion_list=None):
#     file_map = {}
#     for file_path in files:
#         # 从文件路径中提取文件名
#         file_name = os.path.basename(file_path)
#
#         # 预处理文本，过滤符号和特殊字符
#         cleaned_file_name = preprocess_text(file_name)
#
#         # 拆分文本为单词
#         words = cleaned_file_name.split()
#
#         # 如果存在不参与分词的词组列表，则排除
#         if exclusion_list:
#             words = [word for word in words if word not in exclusion_list]
#
#         # 使用 spaCy 进行分词
#         doc = nlp(" ".join(words))
#         tokens = [token.text for token in doc]
#         # 使用分词后的文件名作为键，文件路径作为值
#         file_map[tuple(tokens)] = file_path
#
#     return file_map


# 定义一个函数，用于找到与目标字符串最相似的字符串
def find_best_match(target, options):
    # 从字符串列表中找到最相似的字符串
    best_match = max(options, key=lambda option: fuzz.ratio(target, option))
    # 计算相似度
    # similarity = fuzz.ratio(target, best_match)
    similarity = fuzz.token_sort_ratio(target, best_match)
    return best_match, similarity

# TODO 更精确的模糊条件查找过滤

# def matching_subtitles_after_rename():
#     print("请输入视频文件夹所在位置： ")
#     video_dir = input()
#     print("请输入字幕文件夹所在位置： ")
#     srt_dir = input()
#
#     # video_list=get_file_paths(video_dir)
#     # srt_list=get_file_paths(srt_dir)
#     video_dir = tools.get_file_paths_limit(video_dir, '.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg',
#                                              '.mpe', '.m1v', '.m2v',
#                                              '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv',
#                                              '.mp4', '.m4v',
#                                              '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram',
#                                              '.rmvb', '.rpm', '.flv', '.mov',
#                                              '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm',
#                                              '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
#     srt_dir=tools.get_file_paths_limit(srt_dir,'.srt','.ass','.sub','.vtt')
#     # 创建文件名到文件路径的映射字典
#     video_file_map = create_file_map(video_dir)
#     rule_list = ['eng', 'EN', 'ENG', 'cn', 'CN', 'ENGLISH', 'GERMAN', 'zh-CN', 'AAC', '1440p', '4k', '2k','_1080p','1080p', 'BD', 'h264','utf8']
#     srt_file_map = create_file_map(srt_dir,rule_list)
#
#     # 为每个视频文件查找最佳匹配的字幕文件
#     print('\n' + '-' * 100)
#     for video_tokens, video_path in video_file_map.items():
#         best_match_name, best_match_path, best_token_count = "", "", 0
#         best_similarity = 0  # 新增变量用于保存最佳相似度值
#         # l=len(video_tokens)
#         # print(l)
#         for srt_tokens, srt_path in srt_file_map.items():
#             # 取视频文件名的分词列表和字幕文件名的分词列表的共同分词
#             matching_tokens = set(video_tokens) & set(srt_tokens)
#
#             # 计算匹配的分词数量
#             match_count = len(matching_tokens)
#
#             # 如果匹配成功的分词数量大于等于1，则认为匹配成功
#             if match_count >= 1 and match_count > best_token_count:
#                 best_match_name, best_match_path, best_token_count = srt_tokens, srt_path, match_count
#                 if os.path.isfile(video_path) and os.path.isfile(best_match_path):
#                     # 将文件名作为目标字符串，文件名列表作为字符串列表
#                     _, similarity = find_best_match(os.path.basename(video_path), [os.path.basename(best_match_path)])
#                     best_similarity = similarity  # 更新最佳相似度值
#
#         # 只输出匹配成功的结果
#         if best_token_count >= 3 and best_similarity >= 20:
#             print(f"视频文件：{video_path} 最佳匹配的字幕文件：{best_match_path} 匹配成功的分词数量：{best_token_count}")
#             # del srt_file_map[best_match_name]
#         elif best_token_count==1 and best_similarity>=35:
#             print(f"视频文件：{video_path} 最佳匹配的字幕文件：{best_match_path} 匹配成功的分词数量：{best_token_count} :{best_similarity}")
# del srt_file_map[best_match_name]

# def matching_subtitles_after_rename():
#     print("请输入视频文件夹所在位置： ")
#     video_dir = input()
#     print("请输入字幕文件夹所在位置： ")
#     srt_dir = input()
#
#     video_dir = tools.get_file_paths_limit(video_dir, '.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg',
#                                            '.mpe', '.m1v', '.m2v',
#                                            '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv',
#                                            '.mp4', '.m4v',
#                                            '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram',
#                                            '.rmvb', '.rpm', '.flv', '.mov',
#                                            '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm',
#                                            '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
#     srt_dir = tools.get_file_paths_limit(srt_dir, '.srt', '.ass', '.sub', '.vtt')
#
#     # 创建文件名到文件路径的映射字典
#     video_file_map = create_file_map(video_dir)
#     rule_list = ['eng', 'EN', 'ENG', 'cn', 'CN', 'ENGLISH', 'GERMAN', 'zh-CN', 'AAC', '1440p', '4k', '2k', '_1080p',
#                  '1080p', 'BD', 'h264', 'utf8']
#     srt_file_map = create_file_map(srt_dir, rule_list)
#
#     # 为每个视频文件查找最佳匹配的字幕文件
#     print('\n' + '-' * 100)
#     for video_tokens, video_path in video_file_map.items():
#         best_match_name, best_match_path, best_token_count = "", "", 0
#         best_similarity = 0  # 新增变量用于保存最佳相似度值
#         max_match_count = 0
#
#         flag = len(srt_file_map)
#         for srt_tokens, srt_path in srt_file_map.items():
#             flag -= 1
#             # 计算相似度
#             _, similarity = find_best_match(os.path.basename(video_path), [os.path.basename(srt_path)])
#
#             # 如果相似度大于等于预设值，进行分词匹配
#             if similarity >best_similarity:
#                 best_similarity=similarity
#                 # 取视频文件名的分词列表和字幕文件名的分词列表的共同分词
#                 matching_tokens = set(word.lower() for word in video_tokens) & set(word.lower() for word in srt_tokens)
#
#                 # 计算匹配的分词数量
#                 match_count = len(matching_tokens)
#
#                 # 更新最大匹配数量
#                 if max_match_count < match_count:
#                     max_match_count = match_count
#
#             # 如果匹配成功的分词数量大于等于2，则认为匹配成功
#             if flag == 0 and best_similarity >=50 and max_match_count>=1:
#                 best_match_name, best_match_path, best_token_count = srt_tokens, srt_path, max_match_count
#                 best_similarity = best_similarity  # 更新最佳相似度值
#
#         # 输出匹配成功的结果
#         if best_similarity >=30 and max_match_count>=1:
#             print(f"视频文件：{video_path} 最佳匹配的字幕文件：{best_match_path} 匹配成功的分词数量：{max_match_count} :{best_similarity}")
#             if best_match_name and best_similarity >= 40:
#                 del srt_file_map[best_match_name]


# def matching_subtitles_after_rename():
#     print("请输入视频文件夹所在位置： ")
#     video_dir = input()
#     print("请输入字幕文件夹所在位置： ")
#     srt_dir = input()
#
#     # video_list=get_file_paths(video_dir)
#     # srt_list=get_file_paths(srt_dir)
#     video_dir = tools.get_file_paths_limit(video_dir, '.avi', '.wmv', '.wmp', '.wm', '.asf', '.mpg', '.mpeg',
#                                              '.mpe', '.m1v', '.m2v',
#                                              '.mpv2', '.mp2v', '.tp', '.tpr', '.trp', '.vob', '.ifo', '.ogm', '.ogv',
#                                              '.mp4', '.m4v',
#                                              '.m4p', '.m4b', '.3gp', '.3gpp', '.3g2', '.3gp2', '.mkv', '.rm', '.ram',
#                                              '.rmvb', '.rpm', '.flv', '.mov',
#                                              '.qt', '.nsv', '.dpg', '.m2ts', '.m2t', '.mts', '.dvr-ms', '.k3g', '.skm',
#                                              '.evo', '.nsr', '.amv', '.divx', '.webm', '.wtv', '.f4v', '.mxf')
#     srt_dir=tools.get_file_paths_limit(srt_dir,'.srt','.ass','.sub','.vtt')
#     # 创建文件名到文件路径的映射字典
#     video_file_map = create_file_map(video_dir)
#     rule_list = ['eng', 'EN', 'ENG', 'cn', 'CN', 'ENGLISH', 'GERMAN', 'zh-CN', 'AAC', '1440p', '4k', '2k','_1080p','1080p', 'BD', 'h264','utf8']
#     srt_file_map = create_file_map(srt_dir,rule_list)
#
#     # 为每个视频文件查找最佳匹配的字幕文件
#     print('\n' + '-' * 100)
#     for video_tokens, video_path in video_file_map.items():
#         best_match_name, best_match_path, best_token_count = "", "", 0
#         best_similarity = float('-inf')  # 初始化为负无穷
#         # l=len(video_tokens)
#         # print(l)
#         flag=len(srt_file_map)
#         max_match_count=0
#         for srt_tokens, srt_path in srt_file_map.items():
#             flag -=1
#             # 取视频文件名的分词列表和字幕文件名的分词列表的共同分词
#             matching_tokens = set(video_tokens) & set(srt_tokens)
#
#             # 计算匹配的分词数量
#             match_count = len(matching_tokens)
#             if max_match_count<match_count:
#                 max_match_count=match_count
#             # 如果匹配成功的分词数量大于等于1，则认为匹配成功
#             if  flag==0:
#                 best_match_name, best_match_path, best_token_count = srt_tokens, srt_path, match_count
#                 if os.path.isfile(video_path) and os.path.isfile(best_match_path):
#                     # 将文件名作为目标字符串，文件名列表作为字符串列表
#                     _, similarity = find_best_match(os.path.basename(video_path), [os.path.basename(best_match_path)])
#                     max_match_count = max_match_count  # 更新最佳相似度值
#                     if best_similarity<similarity:
#                         best_similarity=similarity
#
#         # if max_match_count >= 2 and best_similarity>=27:
#         #     print(f"视频文件：{video_path} 最佳匹配的字幕文件：{best_match_path} 匹配成功的分词数量：{max_match_count} :{best_similarity}")
#         if best_similarity >= 27:
#             print(f"视频文件：{video_path} 最佳匹配的字幕文件：{best_match_path} 匹配成功的分词数量：{max_match_count} :{best_similarity}")
# elif  best_similarity >=29:
#     print(f"视频文件：{video_path} 最佳匹配的字幕文件：{best_match_path} 匹配成功的分词数量：{max_match_count} |{best_similarity}")
