'''
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license

'''
import os
import constants
import tools

# 注册模块对象
from model import tips_m, log_info_m, result_m

# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler


# TODO 兼容UI
def ui_param_decorator(input_func):
    def wrapper(*args, **kwargs):
        use_ui = kwargs.get('use_ui', False)
        if use_ui:
            ui_params = kwargs.get('ui_params', {})

            # 获取文件路径列表
            paths_input = ui_params.get('paths_input', None)
            if paths_input:
                paths = paths_input.toPlainText().split('\n')
                paths = [path.strip() for path in paths if path.strip()]  # 去除空行和前后空格
            else:
                paths = []

            # 获取文件类型索引
            file_type_input = ui_params.get('file_type_input', None)
            if file_type_input:
                file_type_index = int(file_type_input.text().strip())
            else:
                file_type_index = 0

            # 调用原始函数并传递解析后的参数
            kwargs.update({'paths': paths, 'index': file_type_index})
            return input_func(*args, **kwargs)
        else:
            # 调用原始函数并传递原始参数
            return input_func(*args, **kwargs)

    return wrapper


def getfoldercount():
    "获取文件夹列表下的文件数量"
    count = 0
    tips_m.print_message(message="输入文件列表")
    paths = tools.process_input_list()
    for path in paths:
        for root, dirs, files in os.walk(path):
            count += len(files)
    # log_info_m.print_message("test")
    result_m.print_message(message=count)
    return count


def getfoldercount_by_include():
    """获取指定文件类型的文件数量和路径"""
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
        path_list = tools.get_file_paths_list_limit(list, *extensions)
    elif os.path.isdir(dir) and index <= 5:
        path_list = tools.get_file_paths_limit(dir, *extensions)
    else:
        path_list = None
        result_m.print_message("参数有误，不是合法的路径？")

    f_path_list = tools.cont_files_processor(path_list, index)
    return f_path_list


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
        result_m.print_message("参数有误，不是合法的路径？")

    f_path_list = tools.cont_files_processor(path_list, index)

    return f_path_list


def get_file_count_by_underfolder_size():
    """
    获取录入文件夹列表中子文件大于指定大小（MB)且存在3个以上文件的文件夹并输出不符合条件的文件夹
    """
    file_paths_folder_paths = tools.process_input_list()
    tips_m.print_message(message="是否打印每个文件夹下的具体内容？Y/N def:N")
    flag = tools.process_input_str_limit() or 'N'
    tips_m.print_message(message="文件夹下的内容最低应大于？（MB）")
    size = tools.process_input_str_limit()
    if not tools.check_is_None(file_paths_folder_paths):
        result_list = set()
        result_wipe_list = set()
        file_list = set()
        folder_list = set()
        file_list, folder_list = tools.check_file_or_folder(file_paths_folder_paths)

        if folder_list:
            result_list = [folder for folder in folder_list if
                           tools.get_file_count(folder) >= 3 and tools.get_folder_size
                           (folder) >= size * 1024 * 1024]
            result_wipe_list = set(folder_list) - set(result_list)

        if flag.upper() == 'N':
            result_m.print_message(message='录入列表的单个文件\n')
            tools.print_list_structure(file_list)
            result_m.print_message(message='录入列表文件夹不符合大于3GB且至少存在3个文件的文件夹\n')
            tools.print_list_structure(result_wipe_list)
            result_m.print_message(message='录入列表文件夹符合大于3GB且至少存在3个文件的文件夹\n')
            tools.print_list_structure(result_list)
        else:
            result_m.print_message(message='录入列表的单个文件\n')
            tools.print_list_structure(file_list)
            result_m.print_message(message='录入列表文件夹不符合大于3GB且至少存在3个文件的文件夹\n')
            tools.print_list_structure([folder for folder in result_wipe_list if tools.get_file_paths(folder)])
            result_m.print_message(message='录入列表文件夹符合大于3GB且至少存在3个文件的文件夹\n')
            tools.print_list_structure([folder for folder in result_list if tools.get_file_paths(folder)])
        return file_list, result_wipe_list, result_list
