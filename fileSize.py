import os
# 相同子目录下
import tools


def get_total_file_size(file_paths):
    total_size = 0
    for file_path in file_paths:
        if os.path.exists(file_path):
            total_size += os.path.getsize(file_path)
    print(f"Total size: {total_size / (1024 ** 3):.2f} GB")
    return total_size / (1024 ** 3)


def def_get_total_size(file_paths):
    total_size = 0
    for file_path in file_paths:
        if os.path.isfile(file_path):
            total_size += os.path.getsize(file_path)

        elif os.path.isdir(file_path):
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
    print(f"Total size: {total_size / (1024 ** 3):.2f} GB")
    return total_size / (1024 ** 3)

def filter_files_by_size():
    exclude_dirs = [".ts", "WarmSnow"]
    exclude_extensions = [".ass", ".srt", ".sub", ".assets", ".dll", ".wem", ".xml", ".ts", ".clpi", ".nfo", ".torrent",
                            ".ssa", ".vtt"]  # 修改为你需要排除的后缀列表
    print("请输入文件夹路径")
    # input_logger = InputLogger('output.txt')
    # input_logger.start_logging()
    paths = tools.process_input_str("")
    paths = tools.get_file_paths_e(paths,exclude_dirs, exclude_extensions)
    print("请输入最小值（MB）")
    min_size = float(tools.process_input_str("")) * 1024*1024
    print("请输入最大值（MB）")
    max_size = float(tools.process_input_str("")) * 1024*1024
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



