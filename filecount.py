import os
import constants
import tools

def getfoldercount():
    "获取文件列表下的文件数量"
    count = 0
    print("输入文件列表")
    paths = tools.process_input_list()
    for path in paths:
        for root, dirs, files in os.walk(path):
            count += len(files)
    print(count)

def getfoldercount_by_include():
    """获取指定文件类型的文件数量和路径"""
    list,dir=tools.process_paths_list_or_folder()
    suffix_map ={
        1: constants.ZIP_SUFFIX,
        2: constants.OFFICE_SUFFIX,
        3: constants.VIDEO_SUFFIX,
        4: constants.AUDIO_SUFFIX,
        5: constants.EXTENSIONS,
    }
    print("请输入要包含的文件类型（1-压缩格式, 2-办公软件格式, 3-视频格式，4-音频格式，5-其它格式）")
    index = int(input(""))
    extensions=suffix_map.get(index)
    if list and index<=5:
        path_list=tools.get_file_paths_list_limit(list,*extensions)
    elif os.path.isdir(dir) and index<=5:
        path_list=tools.get_file_paths_limit(dir,*extensions)
    else:
        print("参数有误，不是合法的路径？")
    if path_list is not None:
        count = tools.count_files(path_list)
        print("index: {}".format(index))
        print(count)
        print("是否输出符合条件的文件路径 Y/N")
        flag=input()
        if flag.upper()=='Y':
            for path in path_list:

                print(path)

def getfoldercount_by_exclude():
    """获取指定文件类型外文件的数量和路径"""
    list, dir = tools.process_paths_list_or_folder()
    suffix_map ={
        1: constants.ZIP_SUFFIX,
        2: constants.OFFICE_SUFFIX,
        3: constants.VIDEO_SUFFIX,
        4: constants.AUDIO_SUFFIX,
        5: constants.EXTENSIONS,
    }
    print("请输入要不包含的文件类型（1-压缩格式, 2-办公软件格式, 3-视频格式，4-音频格式，5-其它格式）")
    index = int(input(""))
    extensions=suffix_map.get(index)
    if list:
        print("是否遍历子文件夹  Y/N")
        flag=input()
        path_list=tools.find_matching_files_or_folder_exclude(list,*extensions,folder=dir,flag=flag)
    elif dir:
        path_list=tools.find_matching_files_or_folder_exclude(paths=list,*extensions,folder=dir)
    else:
        print("参数有误，不是合法的路径？")
    if path_list is not None:
        count = tools.count_files(path_list)
        print("index: {}".format(index))
        print(count)
        print("是否输出符合条件的文件路径 Y/N")
        flag=input()
        if flag.upper()=='Y':
            for path in path_list:
                print(path)








