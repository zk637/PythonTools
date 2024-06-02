import os
import constants
import tools

# 注册模块对象
from model import tips_m, log_info_m, result_m

# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler


def ui_param_decorator(func):
    def wrapper(*args, **kwargs):
        if 'ui_enable' in kwargs and kwargs['ui_enable']:
            # 检查ui_enable是否为True
            # 获取函数的参数列表
            parameters = func.__code__.co_varnames
            # 计算关键字参数的数量
            num_keywords = len(parameters) - len(args)
            # 根据参数数量为UI赋值
            if num_keywords > 0:
                for i in range(num_keywords):
                    kwargs[parameters[i]] = args[0].ui.file_input
        return func(*args, **kwargs)
    return wrapper

def getfoldercount(paths=None):
    """
    获取文件夹列表下的文件数量
    Args:
        paths (list of str, optional): 文件夹路径列表。如果未提供，则会提示用户输入。
    """
    if paths is None:
        print("输入文件列表")
        paths = tools.process_input_list()

    count = 0
    for path in paths:
        for root, dirs, files in os.walk(path.strip()):
            count += len(files)

    print(f"Total files count: {count}")
    return count

@ui_param_decorator
def getfoldercount_by_include(paths=None, index=None, ui_enable=False, **kwargs):
    """获取指定文件类型的文件数量和路径"""
    file_list, dir = tools.process_paths_list_or_folder(paths)
    suffix_map = {
        1: constants.ZIP_SUFFIX,
        2: constants.OFFICE_SUFFIX,
        3: constants.VIDEO_SUFFIX,
        4: constants.AUDIO_SUFFIX,
        5: constants.EXTENSIONS,
    }
    tips_m.print_message(message="请输入要包含的文件类型（1-压缩格式, 2-办公软件格式, 3-视频格式，4-音频格式，5-其它格式）")
    index = int(tools.process_input_str_limit(index))
    extensions = suffix_map.get(index)
    if file_list and index <= 5:
        path_list = tools.get_file_paths_list_limit(file_list, *extensions)
    elif os.path.isdir(dir) and index <= 5:
        path_list = tools.get_file_paths_limit(dir, *extensions)
    else:
        path_list = None
        log_info_m.print_message("参数有误，不是合法的路径？")
    result = tools.cont_files_processor(path_list, index)
    return result


def getfoldercount_by_exclude():
    """获取指定文件类型外文件的数量和路径"""
    list, dir = tools.process_paths_list_or_folder()
    suffix_map = {
        1: constants.ZIP_SUFFIX,
        2: constants.OFFICE_SUFFIX,
        3: constants.VIDEO_SUFFIX,
        4: constants.AUDIO_SUFFIX,
        5: constants.EXTENSIONS,
    }
    tips_m.print_message(message="请输入要包含的文件类型（1-压缩格式, 2-办公软件格式, 3-视频格式，4-音频格式，5-其它格式）")
    index = int(tools.process_input_str_limit())
    extensions = suffix_map.get(index)
    if list and index <= 5:
        print("是否遍历子文件夹  Y/N")
        flag = tools.process_input_str_limit()
        path_list = tools.find_matching_files_or_folder_exclude(list, folder=dir, flag=flag, *extensions, )
    elif os.path.isdir(dir) and index <= 5:
        path_list = tools.find_matching_files_or_folder_exclude(folder=dir, *extensions)
    else:
        path_list = None
        log_info_m.print_message("参数有误，不是合法的路径？")
    tools.cont_files_processor(path_list, index)


def get_file_count_by_underfolder_size():
    """
    获取录入文件列表中子文件大于3GB且存在3个以上文件的文件夹并输出不符合条件的文件夹
    """
    file_paths_folder_paths = tools.process_input_list()
    tips_m.print_message(message="是否打印每个文件夹下的具体内容？Y/N def:N")
    flag = tools.process_input_str_limit() or 'N'
    if not tools.check_is_None(file_paths_folder_paths):
        result_list = set()
        result_wipe_list = set()
        file_list = set()
        folder_list = set()
        file_list, folder_list = tools.check_file_or_folder(file_paths_folder_paths)

        if folder_list:
            result_list = [folder for folder in folder_list if
                           tools.get_file_count(folder) >= 3 and tools.get_folder_size
                           (folder) >= 3 * 1024 * 1024 * 1024]
            result_wipe_list = set(folder_list) - set(result_list)

        if flag.upper() == 'N':
            result_m.print_message(message='录入列表的单个文件\n')
            tools.for_in_for_print(file_list)
            result_m.print_message(message='录入列表文件夹不符合大于3GB且至少存在3个文件的文件夹\n')
            tools.for_in_for_print(result_wipe_list)
            result_m.print_message(message='录入列表文件夹符合大于3GB且至少存在3个文件的文件夹\n')
            tools.for_in_for_print(result_list)
        else:
            result_m.print_message(message='录入列表的单个文件\n')
            tools.for_in_for_print(file_list)
            result_m.print_message(message='录入列表文件夹不符合大于3GB且至少存在3个文件的文件夹\n')
            tools.for_in_for_print([folder for folder in result_wipe_list if tools.get_file_paths(folder)])
            result_m.print_message(message='录入列表文件夹符合大于3GB且至少存在3个文件的文件夹\n')
            tools.for_in_for_print([folder for folder in result_list if tools.get_file_paths(folder)])
