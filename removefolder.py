import os
import tools
import send2trash

def remove_small_folders():
    print("请输入文件夹路径:")
    # input_logger = InputLogger('output.txt')
    # input_logger.start_logging()
    folder=tools.process_intput_strr("")
    print("请输入文件大小下限（单位：MB）：")
    min_size_str=tools.process_input_str("")
    min_size = float(min_size_str) * 1024 * 1024
    """删除小于指定大小的文件所在的文件夹"""
    print("是否使用回收站Y/N:")
    flag = tools.process_intput_strr("")
    if 'Y' == flag.upper():
        # input_logger.stop_logging()
        # input_logger.close()
        remaining_files = delete_small_files_re(folder, min_size)
        print("Remaining files:")
        for file in remaining_files:
            print(file)
    else:
        # input_logger.stop_logging()
        # input_logger.close()
        remaining_files = delete_small_files(folder, min_size)
        print("Remaining files:")
        for file in remaining_files:
            print(file)

def delete_small_files(folder, min_size):
    """删除文件夹下小于30MB的文件并输出删除后剩下的文件列表"""
    files = []
    for root, dirs, filenames in os.walk(folder):
        for filename in filenames:
            path = os.path.join(root, filename)
            if os.path.getsize(path) < min_size:
                    os.remove(path)
                    print(f"Deleted file: {path}")
            else:
                files.append(path)
    return files

def delete_small_files_re(folder_path, size_limit):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            if file_size < size_limit:
                send2trash.send2trash(file_path)

    remaining_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            remaining_files.append(file_path)
    return remaining_files




