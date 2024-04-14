import datetime
import os
# 相同子目录下
import constants
import tools

# 注册全局异常处理函数
from my_exception import global_exception_handler
global_exception_handler = global_exception_handler


def get_total_file_size(file_paths):
    """获取相同子目录下的文件大小"""
    total_size = 0
    if not tools.check_is_None(file_paths):
        for file_path in file_paths:
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
        print(f"Total size: {total_size / (1024 ** 3):.2f} GB")
        return total_size / (1024 ** 3)


def get_total_size(file_paths):
    """获取不同子目录下的文件大小"""
    total_size = 0
    if not tools.check_is_None(file_paths):
        file_paths, folder_path = tools.check_file_or_folder(file_paths)
        for file_path in file_paths:
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
        print(f"Total size: {total_size / (1024 ** 3):.2f} GB")
    return total_size / (1024 ** 3)


def filter_files_by_sizeordate():
    """获取文件在大小区间下的列表或在修改时间区间下的列表"""
    exclude_dirs = [".ts", "WarmSnow"]
    # exclude_extensions = [".ass", ".srt", ".sub", ".assets", ".dll", ".wem", ".xml", ".ts", ".clpi", ".nfo", ".torrent",
    #                         ".ssa", ".vtt"]  # 修改为你需要排除的后缀列表
    paths,folder=tools.process_paths_list_or_folder()
    suffix_map = {
        1: constants.ZIP_SUFFIX,
        2: constants.OFFICE_SUFFIX,
        3: constants.VIDEO_SUFFIX,
        4: constants.AUDIO_SUFFIX,
        5: constants.EXTENSIONS,
    }
    print("请输入要不包含的文件类型（1-压缩格式, 2-办公软件格式, 3-视频格式，4-音频格式，5-其它格式）")
    index = int(tools.process_input_str_limit())
    exclude_extensions = suffix_map.get(index)
    if not tools.check_is_None(paths):
        paths = tools.find_matching_files_or_folder_exclude(paths, *exclude_extensions, flag='Y')
    elif not tools.check_is_None(folder):
        paths = tools.get_file_paths_e(folder,exclude_dirs, exclude_extensions)
    if paths:
        paths = set(paths)
        print("要执行的操作：Y按照大小输出 N按照修改时间输出")
        flag=tools.process_input_str_limit()
        if flag.upper()=='Y':
            print("请输入最小值（MB）")
            min_size = float(tools.process_input_str_limit()) * 1024*1024
            print("请输入最大值（MB）")
            max_size = float(tools.process_input_str_limit()) * 1024*1024
            print(f"-------------------------------------end-------------------------------------")
            # input_logger.stop_logging()
            # input_logger.close()
            filtered_paths = []
            for path in paths:
                file_size = os.path.getsize(path)
                if min_size <= file_size <= max_size:
                    filtered_paths.append(path)

            filtered_paths.sort(key=lambda x: os.path.getsize(x), reverse=True)
            for path in filtered_paths:
                filename = os.path.basename(path)
                size = "{:.2f}MB".format(os.path.getsize(path) / 1024 / 1024)
                # print(f"{path} {size}")
            print('\n'.join(filtered_paths))
        else:
            print("纯净输出Y/N?")
            cflag=tools.process_input_str_limit()
            print("打印父路径？Y/N?")
            pflag=tools.process_input_str_limit()
            print("输入开始时间段 示例格式20180302")
            start_date=str(tools.process_input_str_limit())
            print("输入结束时间段 示例格式20180519")
            end_date=str(tools.process_input_str_limit())
            """按文件修改日期倒序排列打印文件路径"""
            file_dates = {}

            start_datetime = datetime.datetime.strptime(start_date, "%Y%m%d")
            end_datetime = datetime.datetime.strptime(end_date, "%Y%m%d")

            for path in paths:
                modification_time = os.path.getmtime(path)
                date = datetime.datetime.fromtimestamp(modification_time)

                if start_datetime <= date <= end_datetime:
                    parent_path = os.path.dirname(path)
                    if parent_path not in file_dates:
                        file_dates[parent_path] = []
                    file_dates[parent_path].append((path, date))

            for parent_path, files in file_dates.items():
                if pflag.upper() =="Y":
                    print(parent_path + "--------")
                    files.sort(key=lambda x: x[1], reverse=True)
                if cflag.upper()!='Y':
                    for file in files:
                        print(f"{file[0]}: {file[1]}")
                else:
                    for file in files:
                        print('"'+f"{file[0]}"+'"')





