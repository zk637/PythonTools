# -*- encoding: utf-8 -*-
'''
@File    :   mytools_py_test.py
@Contact :
@License :   (C)Copyright 2018-2021
My_Tools的Testcase
'''
import os
import pytest
import tools
import fileSize

from functools import wraps, partial
from itertools import cycle

import pytest
import atexit
import os

import fileSize
import loggerconifg
import tools
import translate
import filecount
import filebackup
import zippackage
import fileanalysis
import filecomparison
import removefolder

import datetime

from loggerconifg import Logger
from loggerconifg import createog
from loggerconifg import exit_handler
import sys

from unittest.mock import patch, MagicMock

# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler

methods = {
    0: tools.profile_all_functions,
    1: fileSize.get_total_file_size,
    2: fileSize.get_total_size,
    3: translate.getSrt,
    4: translate.getSrtNew,
    5: translate.find_matching_subtitles,
    6: translate.find_matching_subtitles_create,
    7: fileanalysis.get_low_resolution_media_files,
    8: removefolder.remove_small_folders,
    9: filecount.getfoldercount,
    10: fileSize.filter_files_by_sizeordate,
    11: fileanalysis.get_video_duration_sorted,
    12: fileanalysis.print_video_info_list,
    13: filecomparison.check_files_in_folder,
    14: filecomparison.compare_and_move_files,
    15: filecomparison.get_file_paths_with_rules,
    16: filebackup.create_symbolic_links,
    17: filebackup.same_file_createsymbolic_links,
    18: zippackage.check_zip_password,
    19: zippackage.extract_archive,
    20: filecomparison.get_file_paths_with_name,
    21: filecomparison.get_exclude_suffix_list,
    22: filecomparison.get_file_rule_sort,
    23: fileanalysis.getfiletypeislegal,
    24: filecomparison.check_symbolic_link,
    25: filebackup.update_linked_items,
    26: filebackup.create_linked_items,
    27: filecomparison.excel_compare,
    28: fileanalysis.get_video_audio,
    29: filecomparison.rename_with_dir,
    30: fileanalysis.split_video,
    31: fileanalysis.add_srt,
    32: fileanalysis.check_files_subtitle_stream,
    # 31: translate.matching_subtitles_after_rename,
    33: filecomparison.get_directories_and_copy_tree,
    34: fileanalysis.check_video_integrity,
    35: filecount.getfoldercount_by_include,
    36: filecount.getfoldercount_by_exclude,
    37: filecount.get_file_count_by_underfolder_size,
    # 35: filecomparison.print_video_info_list_asy,
    # 26:fileduration.create_symbolic_links_recursive
    # 17: fileduration.compare_file_and_folder_names
}


def run_test_scase():
    # 设置多线程数量
    pytest.config.args = ['-n', '6', '-vs']

    # 设置输出编码为 UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    # 运行测试
    pytest.main([__file__])


# 定义测试用例

def test_profile_all_functions():
    result = tools.profile_all_functions(True)
    assert result is not None


def test_get_total_file_size():
    file_paths = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\index.html",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\it-IT.json"
    ]

    # 调用被测试的方法
    result = fileSize.get_total_file_size(file_paths)

    # 断言结果是否符合预期
    assert isinstance(result, float)
    assert result > 0  # 确保返回的大小大于0


def test_get_total_size():
    file_paths = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\index.html",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\it-IT.json"
    ]
    # 调用被测试的方法
    result = fileSize.get_total_size(file_paths)

    # 断言结果是否符合预期
    assert isinstance(result, float)
    assert result > 0  # 确保返回的大小大于0


import sys


def test_getSrt(monkeypatch):
    inputs = [r'SPYxFAMILY', r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video',
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    # 调用函数
    translate.getSrt()


def test_getSrtNew(monkeypatch):
    srt_inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video',
                  r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: srt_inputs.pop(0))

    # 调用函数
    translate.getSrtNew()


def test_find_matching_subtitles(monkeypatch):
    inputs = [r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY_EN.webm",
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
    # 调用函数
    translate.find_matching_subtitles()


def test_find_matching_subtitles_create(monkeypatch):
    inputs = [r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY_EN.webm",
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
    # 调用函数
    translate.find_matching_subtitles_create()


def test_get_low_resolution_media_files(monkeypatch):
    inputs = ['1280*720', '2280*3000', r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail", f'Y']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    # 调用函数
    fileanalysis.get_low_resolution_media_files()


def test_remove_small_folders(monkeypatch):
    inputs = [r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_small", f'0.01', f'Y']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    # 调用函数
    removefolder.remove_small_folders()


def test_getfoldercount(monkeypatch):
    inputs = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\新建文件夹 (2)",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\新建文件夹 (3)",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\新建文件夹",
        '""'  # 空行，用于结束输入
    ]

    # 创建一个 MagicMock 对象来模拟 input 函数
    mocked_input = MagicMock(side_effect=inputs)

    # 使用 monkeypatch 将 input 函数替换为 MagicMock 对象
    monkeypatch.setattr('builtins.input', mocked_input)

    result = filecount.getfoldercount()

    # assert isinstance(result, float)


def test_filter_files_by_sizeordate_yes(monkeypatch):
    print(10)
    # 定义模拟的输入和输出值
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\3",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\4",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\5",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\1",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\2",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\批量提取文件名.bat",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4",
                   '""'  # 空行，用于结束输入
                   ]
    inputs = [3, 'Y', 0.01, 3]

    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    # 使用 patch 模拟 process_paths_list_or_folder 函数的返回值
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        # 调用函数
        fileSize.filter_files_by_sizeordate()


def test_filter_files_by_sizeordate_no(monkeypatch):
    print(10)
    # 定义模拟的输入和输出值
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count",
                   '""'  # 空行，用于结束输入
                   ]
    inputs = [3, 'Y', 0.001, 10]

    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    # 使用 patch 模拟 process_paths_list_or_folder 函数的返回值
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        # 调用函数
        fileSize.filter_files_by_sizeordate()


def test_filter_files_by_sizeordate_modifiedate(monkeypatch):
    print(11)
    # 定义模拟的输入和输出值
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\3",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\4",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\5",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\1",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\2",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\批量提取文件名.bat",
                   '""'  # 空行，用于结束输入
                   ]
    inputs = [3, 'N', 'Y', 'Y', 20240307, 20240413]

    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    # 使用 patch 模拟 process_paths_list_or_folder 函数的返回值
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        # 调用函数
        fileSize.filter_files_by_sizeordate()


def test_get_video_duration_sorted_yes(monkeypatch):
    print(11)
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
        , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = ['Y', 'Y']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

        fileanalysis.get_video_duration_sorted()


def test_get_video_duration_sorted_no(monkeypatch):
    print(11)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail",
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    inputs = ['N', 'N']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

        fileanalysis.get_video_duration_sorted()


def test_print_video_info_list_yes(monkeypatch):
    print(12)
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
        , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = ['Y', 3]

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

        fileanalysis.print_video_info_list()


def test_print_video_info_list_no(monkeypatch):
    print(12)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    inputs = ['N', 3]

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

        fileanalysis.print_video_info_list()


def test_check_files_in_folder(monkeypatch):
    inputs_list = ['Y'
        , r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
        , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
                   ]
    inputs = [r"H:\videos\test\test_video_detail", 'N']
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    filecomparison.check_files_in_folder(inputs_list)


def test_compare_and_move_files(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_ts', 'N']

    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    filecomparison.compare_and_move_files()


def test_get_file_paths_with_rules(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule']

    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    filecomparison.get_file_paths_with_rules()


@pytest.mark.skip(reason="Skipping this test function for now")
def test_create_symbolic_links(monkeypatch):
    inputs_list = [
        r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
        , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
          '"'  # 空行结束输入
    ]
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_symbolic_links\新建文件夹']
    mocked_input = MagicMock(side_effect=inputs_list)
    monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    filebackup.create_symbolic_links()


@pytest.mark.skip(reason="Skipping this test function for now")
def test_same_file_createsymbolic_links(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_symbolic_links',
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_symbolic_links\same_symbolic', 'N']

    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    filebackup.same_file_createsymbolic_links()


def test_check_zip_password(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip', 'Y', 'r']
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    zippackage.check_zip_password()


def test_extract_archive(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip']
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    zippackage.extract_archive()


def test_get_file_paths_with_name(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video']
    inputs_list = [
        r"5_6078060425344189964"
        , r"5_6080421351686931793"
        , r"5_6061903926607741990"
        , r"5_6075682606895072339",
        '""'  # 空行，用于结束输入
    ]
    # 使用 patch 模拟 input 函数的行为
    with patch('builtins.input', side_effect=inputs_list):
        # 调用被测试的函数
        result = tools.process_input_list()
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        with patch('tools.process_input_list', return_value=result):
            filecomparison.get_file_paths_with_name()


def test_get_exclude_suffix_list_yes(monkeypatch):
    print(21)
    inputs_list = ['Y'
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\pyvenv.cfg"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\test_CN.mp4"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\testDemo.py"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\testRename.py"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\4_5956136083451284611.srt",
                   '""'  # 空行，用于结束输入
                   ]
    inputs = ['N', '.srt .mp4']
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    # 使用 patch 来模拟 process_paths_list_or_folder 函数的行为
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr('builtins.input', lambda: inputs.pop(0))

        # 再次调用测试函数
        filecomparison.get_exclude_suffix_list()


def test_get_exclude_suffix_list_no(monkeypatch):
    print(21)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix"
                   ]
    inputs = ['Y', '.srt .mp4']
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    # 使用 patch 来模拟 process_paths_list_or_folder 函数的行为
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr('builtins.input', lambda: inputs.pop(0))

        # 再次调用测试函数
        filecomparison.get_exclude_suffix_list()


@pytest.mark.skip(reason="Skipping this test function for now")
def test_get_file_rule_sort_yes(monkeypatch):
    print(22)
    inputs_list = ['Y', ',Day', '宣传文本', '文宣'
                                        '""'  # 空行，用于结束输入
                   ]
    # inputs = [
    #     '""'  # 空行，用于结束输入
    #     ]

    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
        # 模拟用户输入
        filecomparison.get_file_rule_sort()


def test_get_file_rule_sort_no(monkeypatch):
    print(22)
    inputs_list = ['N',
                   '""'  # 空行，用于结束输入
                   ]
    inputs_list = ['N', '1111']

    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        filecomparison.get_file_rule_sort()


def test_getfiletypeislegal(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail']
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    fileanalysis.getfiletypeislegal()


def test_excel_compare(monkeypatch):
    inputs = [r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_csv\WizTree_20240419210133.csv",
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail', 200, '文件名称', 'Y']

    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    filecomparison.excel_compare()


def test_get_video_audio_yes(monkeypatch):
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4"
        ,
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4",
                   '""'  # 空行，用于结束输入
                   ]

    # 使用 patch 来模拟 process_paths_list_or_folder 函数的行为
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 调用测试函数
        fileanalysis.get_video_audio()


def test_get_video_audio_no(monkeypatch):
    inputs = ['N',
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail',
              '""'  # 空行，用于结束输入
              ]

    # 使用 patch 来模拟 process_paths_list_or_folder 函数的行为
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 调用测试函数
        fileanalysis.get_video_audio()


def test_rename_with_dir(monkeypatch):
    inputs = [r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_rename"]
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    filecomparison.rename_with_dir()


def test_split_video(monkeypatch):
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4"
        ,
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4",
                   '""'  # 空行，用于结束输入
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = [1.5]
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        fileanalysis.split_video()


def test_add_srt(monkeypatch):
    inputs = [r"H:\videos\test\test_srt\4_5956136083451284611.webm",
              r"H:\videos\test\test_srt\4_5956136083451284611.srt",
              'N']
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    fileanalysis.add_srt()


def test_check_files_subtitle_stream_yes(monkeypatch):
    print(32)
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4"
        ,
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        fileanalysis.check_files_subtitle_stream()


def test_check_files_subtitle_stream_no(monkeypatch):
    print(32)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        fileanalysis.check_files_subtitle_stream()


def test_get_directories_and_copy_tree(monkeypatch):
    inputs = [r'D:\Back\GameSaveBackupsSource\8Doors',
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_folder_tree']
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    filecomparison.get_directories_and_copy_tree()


def test_check_video_integrity_yes(monkeypatch):
    print(34)
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4"
        ,
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4",
                   '""'  # 空行，用于结束输入
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        fileanalysis.check_video_integrity()


def test_check_video_integrity_no(monkeypatch):
    print(34)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        fileanalysis.check_video_integrity()


def test_getfoldercount_by_include_yes(monkeypatch):
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
        , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\index.html"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\it-IT.json",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = [3, 'Y']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        # print(inputs)
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        filecount.getfoldercount_by_include()


def test_getfoldercount_by_include_no(monkeypatch):
    inputs_list = ['N',
                   r"H:\videos\test\test_video_detail",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    inputs = [3, 'Y']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        # print(inputs)
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        filecount.getfoldercount_by_include()


def test_getfoldercount_by_exclude_yes(monkeypatch):
    print(36)
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
        , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\index.html",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\it-IT.json",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = [3, 'Y', 'Y']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        filecount.getfoldercount_by_exclude()


def test_getfoldercount_by_exclude_no(monkeypatch):
    print(36)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail",
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    inputs = [3, 'Y']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        filecount.getfoldercount_by_exclude()


# TODO 合并优化
def test_get_get_file_count_by_underfolder_size_yes(monkeypatch):
    print(37)
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = ['Y']

    with patch('tools.process_input_list', return_value=(path_list)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        filecount.get_file_count_by_underfolder_size()


def test_get_get_file_count_by_underfolder_size_no(monkeypatch):
    print(37)
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = ['N']

    with patch('tools.process_input_list', return_value=(path_list)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        filecount.get_file_count_by_underfolder_size()


def test_split_audio_y(monkeypatch):
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_audio\mixkit-follow-me-home-350.mp3"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_audio\mixkit-christmas-jokes-1021.mp3",
                   '""'  # 空行，用于结束输入
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        # monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        fileanalysis.split_audio()


def test_split_audio_n(monkeypatch):
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_audio"]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        # monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        fileanalysis.split_audio()


def test_flag_y(monkeypatch):
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\3",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\4",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\5",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\1",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\2",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\批量提取文件名.bat",
                   '""'  # 空行，用于结束输入
                   ]
    process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)


def test_flag_n(monkeypatch):
    inputs = ['N', r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_size_10']
    process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs)


def process_paths_list_or_folder(monkeypatch, flag, inputs_list=None, inputs=None):
    """
    :param monkeypatch:
    :param flag:
    :param inputs_list:
    :param inputs:
    :return:
    """
    if flag == 'Y':
        # 模拟用户选择为 'y' 并输入文件路径列表

        # 创建一个 MagicMock 对象来模拟 input 函数
        mocked_input = MagicMock(side_effect=inputs_list)

        # 使用 monkeypatch 将 input 函数替换为 MagicMock 对象
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str', lambda: inputs_list.pop(0))

    elif flag == 'N':
        # 模拟用户选择为 'n' 并输入文件夹路径

        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))

    # 调用函数
    path_list, folder = tools.process_paths_list_or_folder()
    print(path_list)
    print(folder)
    return path_list, folder


def test_convert_to_utf8(monkeypatch):
    encode = tools.detect_encoding(r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\gdk.txt")
    path = tools.convert_to_utf8(r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\gdk.txt", encode)
    return path


def test_parse():
    a = 1
    str(a)
    print(str(a) + '\n')
    b = '1'
    print(int(b))
    c = '1.1'
    print(float(c))
    d = 1.1
    print(str(d))
    # e =d*c
    # print(e)


# 运行测试用例
if __name__ == "__main__":
    run_test_scase()
