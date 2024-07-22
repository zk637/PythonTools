'''

@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license
'''
import os
from PIL import Image
import cv2
import tools
import constants
from tqdm import tqdm

# 注册模块对象
from model import tips_m, log_info_m, result_m

# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler


def get_low_resolution_media_files():
    """通过视频目录查找符合区间条件分辨率的媒体文件"""

    tips_m.print_message(message="-----------------------请输入第一个分辨率阈值（格式为 宽*高）：--------------------------")
    size_limit1 = str(tools.process_input_str_limit())
    width_limit1, height_limit1 = map(int, size_limit1.split("*"))

    tips_m.print_message(message="-----------------------请输入第二个分辨率阈值（格式为 宽*高）:--------------------------")
    size_limit2 = str(tools.process_input_str_limit())
    width_limit2, height_limit2 = map(int, size_limit2.split("*"))

    if width_limit1 > width_limit2:
        width_limit1, width_limit2 = width_limit2, width_limit1
    if height_limit1 > height_limit2:
        height_limit1, height_limit2 = height_limit2, height_limit1

    log_info_m.print_message(message=f"分辨率区间阈值：{width_limit1}*{height_limit1}~{width_limit2}*{height_limit2}")

    tips_m.print_message(message="请输入视频文件夹：")
    path = tools.process_input_str_limit()
    tips_m.print_message(message="比特率排序Y/N")

    flag = tools.process_input_str_limit()
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

                log_info_m.print_message(message=f"Error occurred while processing file {file_path}: {str(e)}")

                global_exception_handler(type(e), e, e.__traceback__)

    if ('Y' == flag.upper()):
        try:
            files = tools.getbitratesort(files)
            files = tools.add_quotes_forpath_list(files)

            result_m.print_message(message="分辨率符合要求的媒体文件列表（按比特率由大到小排序）：")
            log_info_m.print_message(message="\n".join(files))
        except Exception as e:
            log_info_m.print_message(message=f"Error occurred while sorting files by bitrate: {str(e)}")
            global_exception_handler(type(e), e, e.__traceback__)
    else:
        result_m.print_message(message="分辨率符合要求的媒体文件列表：")
        files = tools.add_quotes_forpath_list(files)
        log_info_m.print_message(message="\n".join(files))


def get_video_duration_sorted():
    """取文件夹或列表下所有视频文件的时长并排序输出或输出时长大小相同的文件"""
    path_list, folder = tools.process_paths_list_or_folder()
    folder_flag = False
    if folder:
        folder_flag = os.path.isdir(folder)

    # 如果输入不是文件夹，则获取文件列表
    if not folder_flag:
        paths = path_list

    tips_m.print_message(message="是否输出文件时长大小一致的列表？Y/N def:N")
    same_flag = tools.process_input_str_limit().upper()
    tips_m.print_message(message="是否纯净输出Y/N")
    flag = tools.process_input_str_limit().upper()
    # 处理用户输入
    tips_m.print_message(message="输出文件创建时间较早的?Y/N def:N")
    user_input = tools.process_input_str_limit().upper()
    # 设置布尔值，根据用户输入和默认值进行判断
    if user_input == "Y":
        date_flag = True
    elif user_input == "N":
        date_flag = False
    else:
        # 默认值
        date_flag = False

    VIDEO_SUFFIX = constants.VIDEO_SUFFIX
    # 如果选择不输出时长相同的列表
    if same_flag == 'N':
        if folder_flag:
            paths = tools.get_file_paths_limit(folder, *VIDEO_SUFFIX)

        if paths:
            durations = []
            for path in paths:
                duration = tools.get_video_duration(path)
                if duration is not None:
                    durations.append((path, duration))

            sorted_durations = sorted(durations, key=lambda x: x[1], reverse=date_flag)
            for path, duration in sorted_durations:
                if flag == 'Y':
                    path = tools.add_quotes_forpath(path)

                    result_m.print_message(message=path)
                else:
                    log_info_m.print_message(message=f"{path}: {duration / 60:.2f} min")

    # 如果选择输出时长相同的列表
    if same_flag == 'Y':
        if folder_flag:
            video_extensions = tools.get_file_paths_limit(folder, *VIDEO_SUFFIX)
        else:
            video_extensions = paths

        if video_extensions:
            file_sizes = {}
            for path in video_extensions:
                duration = tools.get_video_duration(path)
                if duration is not None:
                    file_size = os.path.getsize(path)
                    creation_time = os.path.getctime(path)
                    if file_size not in file_sizes:
                        file_sizes[file_size] = []
                    file_sizes[file_size].append((path, duration, creation_time))

            file_sizes = {k: v for k, v in file_sizes.items() if len(v) > 1}

            for file_size, paths_durations_creation in file_sizes.items():
                paths_durations_creation.sort(key=lambda x: x[2], reverse=True)
                duration_groups = {}
                for path, duration, _ in paths_durations_creation:
                    if duration not in duration_groups:
                        duration_groups[duration] = []
                    duration_groups[duration].append(path)

                duration_groups = {k: v for k, v in duration_groups.items() if len(v) > 1}

                for duration, paths in duration_groups.items():
                    if flag == 'Y':
                        for path in paths[1:]:
                            path = tools.add_quotes_forpath(path)
                            print(path)
                    else:

                        log_info_m.print_message(message=f"{duration / 60:.2f} min")

                        for path in paths[1:]:
                            path = tools.add_quotes_forpath(path)
                            print(path)


def print_video_info_list():
    """输出视频文件的大小、时长、比特率和分辨率（支持文件列表和文件夹）"""

    file_paths_list, video_dir = tools.process_paths_list_or_folder()

    tips_m.print_message(message="是否纯净输出y/n")

    flag = tools.process_input_str_limit()
    if file_paths_list:
        folder = tools.get_file_paths_list_limit(file_paths_list, *constants.VIDEO_SUFFIX)
    elif os.path.isdir(video_dir):
        folder = tools.get_file_paths_limit(video_dir, *constants.VIDEO_SUFFIX)
    else:

        log_info_m.print_message(message="文件为空，需检查条件或参数！")
        return

    if not folder:
        log_info_m.print_message(message="文件为空，需检查条件或参数！")

        return

    # pool=ThreadPoolExecutor(1)
    # future =pool.submit(tools.get_video_info_list,folder)
    # future_result=future.result()
    # video_info_list, max_path_len = future_result
    video_info_list, max_path_len = tools.get_video_info_list(folder)
    for video_info in video_info_list:
        path = video_info[0]
        size = "{:.2f}MB".format(video_info[1])
        duration = "{:.2f}min".format(video_info[2] / (60 * 60))
        bitrate = "{:.2f}kbps".format(video_info[3] / 1024)
        width = video_info[4]
        height = video_info[5]
        if (flag == 'y'.lower()):

            result_m.print_message(message=path)

        else:
            print("{:<{}}{:<15}{:<15}{:<15}{:<15}".format(path, max_path_len, size, duration, bitrate,
                                                          f"{width}x{height}"),
                  end="")

            result_m.print_message(message=" " * (max_path_len - len(path) + 1))


def get_video_audio():
    """
     提取视频的音频文件（支持文件列表和文件夹）
     """
    file_paths_list, folder = tools.process_paths_list_or_folder()
    if file_paths_list:
        folder = tools.get_file_paths_list_limit(file_paths_list, *constants.VIDEO_SUFFIX)
    elif os.path.isdir(folder):
        folder = tools.get_file_paths_limit(folder, *constants.VIDEO_SUFFIX)
    if not folder:
        log_info_m.print_message(message="文件为空，需检查条件或参数！")
        return
    for path in folder:
        tools.convert_video_to_mp3(path)
    log_info_m.print_message(message="队列执行完成")


def getfiletypeislegal():
    """校验文件是否合法"""

    tips_m.print_message(message="请输入文件夹路径:")

    source_folder_path = tools.process_input_str_limit()
    if not tools.check_is_None(source_folder_path):
        path = tools.get_file_paths(source_folder_path)
        # print(path)
        tools.check_file_access(path)


def split_video():
    """
     根据限制大小拆分视频为多段（支持文件列表和文件夹）
     """
    input_video_list, input_video_dir = tools.process_paths_list_or_folder()
    if input_video_list:

        tips_m.print_message(message="拆分后每段文件的大小限制 单位：MB")

        max_size_mb = int(tools.process_input_str_limit()) * 1024 * 1024

        # 初始化进度条
        progress_bar = tqdm(total=len(input_video_list), desc="Processing videos")
        output_dir = r'H:\spilt_parts_dir'
        tools.make_dir(output_dir)
        for input_video in input_video_list:
            progress_bar.update()
            if input_video != '':
                part_num = round(os.path.getsize(input_video) / max_size_mb, 2)
                if part_num > 1:
                    part_max_size = os.path.getsize(input_video) / (os.path.getsize(input_video) / max_size_mb)
                    tools.split_video_for_size(part_max_size, part_num, input_video, output_dir)
                else:
                    log_info_m.print_message(message=f"文件无法拆分：{input_video}")

        progress_bar.close()
    elif os.path.isdir(input_video_dir):
        filename, file_extension = os.path.splitext(input_video_dir)

        output_dir = os.path.join(filename, 'spilt_parts_dir')
        tools.make_dir(output_dir)

        tips_m.print_message(message="拆分后每段文件的大小限制 单位：MB")

        max_size_mb = int(tools.process_input_str()) * 1024 * 1024
        input_video_list = tools.get_file_paths_limit(input_video_dir, *constants.VIDEO_SUFFIX)
        if input_video_list is not None:
            # 初始化进度条
            progress_bar = tqdm(total=len(input_video_list), desc="Processing videos")
            for input_video in input_video_list:
                progress_bar.update()
                free_space = tools.get_free_space_cmd(input_video_dir)
                if free_space > os.path.getsize(input_video):
                    part_num = round(os.path.getsize(input_video) / max_size_mb, 2)
                    if part_num > 1:
                        part_max_size = os.path.getsize(input_video) / part_num
                        tools.split_video_for_size(part_max_size, part_num, input_video, output_dir)
                    else:

                        log_info_m.print_message(message=f"文件无法拆分：{input_video}")

            progress_bar.close()
    else:
        log_info_m.print_message(message="参数有误，不是合法的路径？")


def split_audio():
    """
    拆分音频为两段（支持文件列表和文件夹）
    """
    input_video_list, input_video_dir = tools.process_paths_list_or_folder()
    input_video_list = tools.get_file_paths_list_limit(input_video_list, *constants.AUDIO_SUFFIX)

    if input_video_list:
        path_list = [input_video for input_video in input_video_list if os.path.isfile(input_video)]
    elif os.path.isdir(input_video_dir):
        input_video_list = tools.get_file_paths_limit(input_video_dir, *constants.AUDIO_SUFFIX)
        path_list = [input_video for input_video in input_video_list if os.path.isfile(input_video)]
    else:
        return

    for path in path_list:
        duration, bitrate = tools.get_audio_details(path)
        tools.split_audio_for_duration(path, duration)


# TODO 10bit视频嵌入硬字幕
def add_srt():
    """为视频文件添加字幕"""

    tips_m.print_message(message="输入视频文件路径")
    video_path = tools.process_input_str_limit().replace('"', '')
    tips_m.print_message(message="输入字幕文件路径")
    srt_path = tools.process_input_str_limit().replace('"', '')
    tips_m.print_message(message="硬字幕还是软字幕 Y/N def:N（硬字幕：Y,软字幕：N")

    flag = tools.process_input_str_limit() or 'N'
    if not tools.check_is_None(video_path, srt_path):
        if os.path.isfile(video_path):
            dir_path = os.path.dirname(video_path)
            # base_name = os.path.basename(video_path).split('.')[0]
            base_name, extension = os.path.splitext(video_path.split('\\')[-1])

            log_info_m.print_message(message=base_name)

            # 构建输出文件名
            video_out_name = f"{base_name}_CN.mp4"
            video_out_name = os.path.join(dir_path, video_out_name)
            bat_file = ''
            encode = tools.detect_encoding(srt_path)
            srt_path_utf8 = tools.convert_to_utf8(srt_path, encode)
            if srt_path_utf8 == None:
                print(f"Error：字幕文件无法转换{srt_path}为UTF-8！任务结束")
                return 0
        if flag.upper() == 'Y':
            preset_map = {
                1: 'fast',
                2: 'medium',
                3: 'slow',
            }

            # 提示用户是否使用质量控制
            tips_m.print_message(message="是否使用质量控制？ Y/N def:N")
            flag = tools.process_input_str_limit().replace('"', '').upper() or 'N'

            if flag == 'Y':
                media_info = tools.get_media_info(video_path)
                total_bitrate = media_info.get('General', {}).get('overall_bit_rate', 'Unknown')
                # 如果无法获取到比特率信息，则终止程序
                if total_bitrate == 'Unknown':
                    print(f"Error：无法获取原视频{video_path}的总比特率信息！任务终止")
                    return 0

                # 提示总比特率大小
                tips_m.print_message(
                    message=f"总比特率大小的值 单位：Kbps def:原视频的总比特率大小{total_bitrate / 1000}")

                # 获取用户输入的比特率
                user_input = tools.process_input_str_limit().strip()  # 去除首尾空格

                # 如果用户没有输入有效值，会使用默认值
                if user_input:
                    try:
                        total_bitrate = float(user_input)
                    except ValueError:
                        print("请输入有效的比特率值！如原视频可获取总比特率将默认使用")
                else:
                    total_bitrate = total_bitrate / 1000  # 使用默认值

                # 提示用户选择质量效率平衡因子
                tips_m.print_message(
                    message="质量效率平衡因子 def:2 （1-fast：在速度和质量之间取得较好的平衡, 2-medium：默认预设，在速度和质量之间取得平衡, 3-slow：编码速度较慢，但质量显著提升）")
                index = int(tools.process_input_str_limit()) or 2
                preset = preset_map.get(index)

                # 构建 FFmpeg 命令
                srt_path_utf8 = srt_path_utf8.replace('\\', r'\\').replace(':', r'\:')
                srt_path_utf8 = "'" + srt_path_utf8 + "'"
                if media_info.get('Video', {}).get('bit_depth', 'Unknown') != 10:
                    # 可用格式 ffmpeg -i "H:\videos\test\Dracula _1080p.mp4" -vf subtitles="'H\:\\videos\\test\\Dracula.zh.utf8.srt'" "Dracula_1080p_CN.mp4"
                    # 'ffmpeg -i H:\\videos\\test\\Dracula _1080p.mp4 -c:v h264_nvenc -vf subtitle=H\\:\\videos\\test\\Dracula.zh.utf8.srt H:\\videos\\test\\Dracula _1080p_CN.mp4'
                    command = f'ffmpeg -i "{video_path}" -c:v h264_nvenc -b:v {total_bitrate}k -maxrate {total_bitrate}k -bufsize {total_bitrate * 2}k -preset {preset} -vf subtitles="{srt_path_utf8}" "{video_out_name}"'
                else:
                    command = f'ffmpeg -i "{video_path}" -c:v libx265 -pix_fmt yuv420p10le -profile:v main10 -b:v {total_bitrate}k -maxrate {total_bitrate}k -bufsize {total_bitrate * 2}k ' \
                                f'-preset {preset} -vf subtitles="{srt_path_utf8}" "{video_out_name}"'
            else:
                # 构建不使用质量控制的 FFmpeg 命令
                command = f'ffmpeg -i "{video_path}" -i "{srt_path_utf8}" -map 0:v -map 0:a -map 1:s:0 -c:v copy -c:a copy -c:s mov_text -disposition:s:0 forced "{video_out_name}"'

            # 打印和执行命令
            log_info_m.print_message(message=command)
            bat_file = tools.generate_bat_script("run_addSrt.bat", command)
            result = tools.subprocess_common_bat(bat_file, command)

            result_m.print_message(message=result)
        else:
            # 定义 FFmpeg 命令
            command = f'ffmpeg -i "{video_path}" -i "{srt_path_utf8}" -map 0:v -map 0:a -map 1:s:0 -c:v copy -c:a copy -c:s mov_text -disposition:s:0 forced "{video_out_name}"'
            bat_file = tools.generate_bat_script("run_addSrt.bat", command)
            result = tools.subprocess_common_bat(bat_file, command)

            result_m.print_message(message=result)


def check_files_subtitle_stream():
    """
     检查视频是否存在字幕流（支持文件列表和文件夹）
     """
    video_paths_list, video_dir = tools.process_paths_list_or_folder()
    video_files = []
    if video_paths_list:
        video_files.extend(video_paths_list)
    elif os.path.isdir(video_dir):
        video_files = tools.find_matching_files_or_folder_exclude(folder=video_dir, *constants.EXTENSIONS)
    else:

        log_info_m.print_message(message="参数有误，不是合法的路径？")

        return
    videos_with_subtitle_stream = []
    videos_without_subtitle_stream = []
    # 初始化进度条
    progress_bar = tqdm(total=len(video_files), desc="Processing videos")

    # 检查视频完整性
    for video_path in video_files:
        # 更新进度条
        progress_bar.update(1)
        result = tools.check_subtitle_stream(video_path)
        if result:
            videos_with_subtitle_stream.append(video_path)
        else:
            videos_without_subtitle_stream.append(video_path)

    # 关闭进度条
    progress_bar.close()

    result_m.print_message(message="True：存在字幕流的文件：" + '_' * 80)
    tools.for_in_for_print(videos_with_subtitle_stream)
    result_m.print_message(message="False：不存在字幕流的文件：" + '_' * 80)

    tools.for_in_for_print(videos_without_subtitle_stream)


def check_video_integrity():
    """
    获取指定文件列表或文件夹下的视频是否完整（支持文件列表和文件夹）
    """
    video_paths_list, video_dir = tools.process_paths_list_or_folder()

    parms = [video_paths_list, video_dir]
    # 获取需要检查完整性的视频文件列表
    video_files = tools.process_paths_list_and_folder(
        parms,
        process_folder_func=tools.find_matching_files_or_folder_exclude,
        folder_func_args=(constants.EXTENSIONS),
        folder_func_kwargs={'folder': video_dir}
    )

    video_integrity = []
    video_unintegrity = {}

    pattern = r"(.*)_thumbs_\[(\d{4}\.\d{2}\.\d{2}_\d{2}\.\d{2}\.\d{2})\]\.jpg\.!qB"
    # 去除不支持的文件格式和缓存
    video_files = [video_path for video_path in video_files if
                   not tools.check_in_suffix(video_path, constants.CACHE_SUFFIX)]

    # 初始化进度条
    progress_bar = tqdm(total=len(video_files), desc="Processing videos")

    for video_path in video_files:
        # 更新进度条
        progress_bar.update(1)
        # 初始化权重
        weight = 0
        # 检查MP4文件的完整性
        total_MB, realSize_MB = tools.check_mp4(video_path)
        if total_MB == realSize_MB and not tools.check_str_is_None(total_MB) and not tools.check_str_is_None(
                realSize_MB) and not tools.check_not_in_suffix(video_path, *constants.VIDEO_SUFFIX):
            log_info_m.print_message(message="check_mp4：" + video_path)
            video_integrity.append(video_path)
            continue  # 视频完整，跳过后续检查
        else:
            weight += 50

        # 检查最后5分钟
        lflag, last_duration = tools.extract_last_5_minutes(video_path)
        if not lflag:
            weight += 100
            video_unintegrity[video_path] = {"last_duration": last_duration, "start_duration": 0}

        if weight < 100 and weight != 100:
            # 检查最初5分钟
            sflag, start_duration = tools.extract_start_5_minutes(video_path)
            if not sflag:
                weight += 100
                video_unintegrity[video_path] = {"last_duration": last_duration, "start_duration": start_duration}

        if weight < 100 and weight != 100:
            # 检查视频完整性
            if not tools.get_video_integrity(video_path):
                weight += 100
                video_unintegrity[video_path] = {"last_duration": last_duration, "start_duration": start_duration}

        if weight < 100 and weight != 100:
            # 检查是否存在绿屏
            if not tools.check_video_for_green_screen(video_path):
                weight += 50

        if weight < 100 and weight != 100:
            video_integrity.append(video_path)
        else:
            if video_path not in video_unintegrity:
                video_unintegrity[video_path] = {"last_duration": last_duration, "start_duration": start_duration}

    # 关闭进度条
    progress_bar.close()

    video_unintegrity_list = list(video_unintegrity.keys())

    # 输出
    result_m.print_message(message="True：视频文件完整的有：" + '_' * 80)
    tools.for_in_for_print(video_integrity)
    result_m.print_message(message="False：视频文件不完整的有：" + '_' * 80)
    tools.for_in_for_print(video_unintegrity_list)

    if video_unintegrity:
        tips_m.print_message("是否查看不完整的视频? Y/N de:N 默认静音")
        flag = tools.process_input_str().upper() or 'N'
        check_video_paths = []
        # flag = 'Y'
        if flag == 'Y':
            # 初始化进度条
            progress_bar = tqdm(total=len(video_unintegrity), desc="Processing videos")
            for video_path, durations in video_unintegrity.items():
                # 更新进度条
                progress_bar.update(1)
                last_duration = durations.get('last_duration', 0)
                start_duration = durations.get('start_duration', 0)
                check_video_path = tools.play_tocheck_video_minimized(video_path, last_duration, start_duration)
                check_video_paths.append(check_video_path)

                # 关闭进度条
            progress_bar.close()
        result_m.print_message(message="False：检查播放后视频文件不完整的有：" + '_' * 80)

        tools.for_in_for_print(check_video_paths)
