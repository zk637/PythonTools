# -*- encoding: utf-8 -*-
'''
@File    :   mytools_py_test.py
@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license
My_Tools的Testcase
'''
import subprocess

import pytest
import os
import fileSize
import my_exception
import tools
import translate
import filecount
import filebackup
import zippackage
import fileanalysis
import filecomparison
import removefolder

from unittest.mock import patch, MagicMock

# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler

# TODO 接口断言
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
    18: zippackage.check_zip_password_old,
    19: zippackage.extract_archive,
    20: filecomparison.get_file_paths_with_name,
    21: filecomparison.get_exclude_suffix_list,
    22: filecomparison.format_rules_and_tag_sort,
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
    38: fileanalysis.split_audio,
    39: filecomparison.get_exclude_suffix_folder_list,
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


def test_getSrt(monkeypatch):
    inputs = [r'SPYxFAMILY', r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video',
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    # 调用函数
    match_list, path_list = translate.getSrt()

    expected_match_list = {
        'Match found: SPYxFAMILY_EN.webm <--> SPYxFAMILY.srt'
    }
    expected_path_list = {
        r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\SPYxFAMILY.srt',
        r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY.srt'
    }

    assert match_list == expected_match_list and path_list == expected_path_list


def test_getSrtNew(monkeypatch):
    srt_inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video',
                  r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: srt_inputs.pop(0))

    # 调用函数
    match_list, path_list = translate.getSrtNew()

    expected_match_list = {
        r"Match found: SPYxFAMILY_EN.webm <--> SPYxFAMILY.srt"
        , r"Match found: SPYxFAMILY_EN.webm <--> Cyberpunk - Edgerunners - 01 [1080p][ Subtitle].srt"
        ,
        r"Match found: Cyberpunk - Edgerunners - 01 [1080p]_CN-split-noaudio.mp4 <--> Cyberpunk - Edgerunners - 01 [1080p][ Subtitle].srt"
    }

    expected_path_list = {
        r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\SPYxFAMILY.srt',
        r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk '
        '- Edgerunners - 01 [1080p][ Subtitle].srt',
        r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY.srt'
    }

    assert match_list == expected_match_list and path_list == expected_path_list


def test_find_matching_subtitles(monkeypatch):
    inputs = [r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY_EN.webm",
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
    # 调用函数
    slur_matching_subtitles = translate.find_matching_subtitles()

    expected_slur_matching_subtitles = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\SPYxFAMILY.srt"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY.srt"
    ]

    assert slur_matching_subtitles == expected_slur_matching_subtitles


def test_find_matching_subtitles_create(monkeypatch):
    inputs = [r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY_EN.webm",
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
    # 调用函数
    subtitle_path = translate.find_matching_subtitles_create()

    expected_subtitle_path = r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\SPYxFAMILY.srt'

    assert subtitle_path == expected_subtitle_path


def test_get_low_resolution_media_files(monkeypatch):
    inputs = ['1280*720', '2280*3000', r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail", f'Y']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    # 调用函数
    files = fileanalysis.get_low_resolution_media_files()

    expected_files = [
        r'"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4"',
        r'"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4"']
    assert files == expected_files


def test_remove_small_folders(monkeypatch):
    inputs = [r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_small", f'0.01', f'Y']

    # 模拟用户输入
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    # 调用函数
    remaining_files = removefolder.remove_small_folders()

    expected_remaining_files = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_small\logging.html"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_small\图B08-28 径向模糊 素材（via破产姐妹）.jpg"
    ]

    assert remaining_files == expected_remaining_files


def test_getfoldercount(monkeypatch):
    inputs = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\新建文件夹 (2)",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\新建文件夹 (3)",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\新建文件夹",
        'end'  # 空行，用于结束输入
    ]

    # 创建一个 MagicMock 对象来模拟 input 函数
    mocked_input = MagicMock(side_effect=inputs)

    # 使用 monkeypatch 将 input 函数替换为 MagicMock 对象
    monkeypatch.setattr('builtins.input', mocked_input)

    result = filecount.getfoldercount()

    assert isinstance(result, int) and result == 5


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
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4"
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
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count"
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
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\批量提取文件名.bat"
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
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = ['Y', 'Y', 'Y']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

        paths = fileanalysis.get_video_duration_sorted()
        expected_paths = [
            r'H:\videos\test\test_video_detail\5_6075682606895072339.webm',
            r'H:\videos\test\test_video_detail\5_6078060425344189964.webm',
            r'H:\videos\test\test_video_detail\5_6080421351686931793.webm',
            r'H:\videos\test\test_video_detail\2_5228729981135230185.webm',
            r'H:\videos\test\test_video_detail\4_5956136083451284611.webm',
            r'H:\videos\test\test_video_detail\5_6061903926607741990.webm'
        ]
        assert paths == expected_paths


def test_get_video_duration_sorted_no(monkeypatch):
    print(11)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail",
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    inputs = ['N', 'N', 'N']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        paths = fileanalysis.get_video_duration_sorted()
        expected_paths = [
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\2_5228729981135230185.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6061903926607741990.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6075682606895072339.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6078060425344189964.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6080421351686931793.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\corrupted_example.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\Thumb.webm'
        ]
        assert paths == expected_paths


def test_print_video_info_list_yes(monkeypatch):
    print(12)
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
        , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = ['Y', 3]

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

        video_info_list = fileanalysis.print_video_info_list()

        expected_video_info_list = [
            (r'H:\videos\test\test_video_detail\2_5228729981135230185.webm', 0.14445877075195312, 174.0, 417864, 512,
             512),
            (r'H:\videos\test\test_video_detail\5_6078060425344189964.webm', 0.20723533630371094, 147.66, 706386,
             512, 436),
            (r'H:\videos\test\test_video_detail\4_5956136083451284611.webm', 0.14863872528076172, 85.98, 870113, 510,
             512),
            (r'H:\videos\test\test_video_detail\5_6061903926607741990.webm', 0.2198772430419922, 120.0, 922232, 512,
             512),
            (r'H:\videos\test\test_video_detail\5_6075682606895072339.webm', 0.21430397033691406, 84.0, 1284080, 445,
             512),
            (r'H:\videos\test\test_video_detail\5_6080421351686931793.webm', 0.20014476776123047, 47.580000000000005,
             2117195, 512, 288)
        ]

        assert video_info_list == expected_video_info_list


def test_print_video_info_list_no(monkeypatch):
    print(12)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    inputs = ['N', 3]

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

        video_info_list = fileanalysis.print_video_info_list()

        expected_video_info_list = [(
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\2_5228729981135230185.webm',
            0.14445877075195312, 174.0, 417864, 512, 512), (
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\corrupted_example.mp4',
            0.14814472198486328, 152.64000000000001, 488493, 180, 100), (
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\Thumb.webm',
            0.14814472198486328, 152.64000000000001, 488493, 180, 100), (
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6078060425344189964.webm',
            0.20723533630371094, 147.66, 706386, 512, 436), (
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6061903926607741990.webm',
            0.2198772430419922, 120.0, 922232, 512, 512), (
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6075682606895072339.webm',
            0.21430397033691406, 84.0, 1284080, 445, 512), (
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6080421351686931793.webm',
            0.20014476776123047, 47.580000000000005, 2117195, 512, 288), (
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4',
            1.8309993743896484, 388.00002, 2375185, 1280, 720), (
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4',
            0.9314775466918945, 172.79999999999998, 2713125, 1280, 720)]

        assert video_info_list == expected_video_info_list


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

    matching_paths, non_matching_paths = filecomparison.check_files_in_folder(inputs_list)

    # print('-' * 50)
    # tools.for_in_for_print(non_matching_paths)
    expected_matching_paths = [
        r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
    ]
    # expected_non_matching_paths = []
    #
    assert set(matching_paths) == set(expected_matching_paths)


def test_compare_and_move_files(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_ts', 'N']

    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    filecomparison.compare_and_move_files()


def test_get_file_paths_with_rules(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule']

    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    paths = filecomparison.get_file_paths_with_rules()

    expected_paths = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule\字幕组宣传文本.txt"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule\文宣.txt"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule\社团宣传文本.txt"
    ]

    assert paths == expected_paths


@pytest.mark.skip(reason="Skipping this test function for now")
def test_create_symbolic_links(monkeypatch):
    inputs_list = [
        r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
        , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
          'end'  # 空行结束输入
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


def test_check_zip_password_old(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip', 'Y', 'r']
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))

    zippackage.check_zip_password_old()


def test_extract_archive(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip']
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    ex_lists, final_lists = zippackage.extract_archive()

    expected_ex_lists = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_1.7z"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_1.part1.rar"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_1.part2.rar"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_2.rar"
    ]
    expected_final_lists = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test2.rar"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test2_zip.z01"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test2_zip.z02"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test2_zip.zip"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test2_zzip.z01"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test2_zzip.z02"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test2_zzip.zip"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_2.7z"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_2.7z.001"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_2.7z.002"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_2.part1.rar"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_2.part2.rar"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\tokenizer.rar"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\新建压缩文件.7z"
    ]

    assert set(ex_lists) == set(expected_ex_lists) and set(final_lists) == set(expected_final_lists)


def test_get_file_paths_with_name(monkeypatch):
    inputs = [r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video']
    inputs_list = [
        r"5_6078060425344189964"
        , r"5_6080421351686931793"
        , r"5_6061903926607741990"
        , r"5_6075682606895072339",
        'end'  # 空行，用于结束输入
    ]
    # 使用 patch 模拟 input 函数的行为
    with patch('builtins.input', side_effect=inputs_list):
        # 调用被测试的函数
        result = tools.process_input_list()
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        with patch('tools.process_input_list', return_value=result):
            found_files = filecomparison.get_file_paths_with_name()

            expected_found_files = [
                r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6078060425344189964.srt"
                , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6078060425344189964.webm"
                , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6080421351686931793.webm"
                , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6061903926607741990.webm"
                , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6075682606895072339.webm"
            ]

            assert found_files == expected_found_files


def test_get_exclude_suffix_list_yes(monkeypatch):
    print(21)
    inputs_list = ['Y'
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\pyvenv.cfg"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\test_CN.mp4"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\testDemo.py"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\testRename.py"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\4_5956136083451284611.srt"
                   ]
    inputs = ['N', '.srt .mp4']
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    # 使用 patch 来模拟 process_paths_list_or_folder 函数的行为
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr('builtins.input', lambda: inputs.pop(0))

        # 再次调用测试函数
        matching_files = filecomparison.get_exclude_suffix_list()

        expected_matching_files = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\pyvenv.cfg"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\testDemo.py"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\testRename.py"
        ]

        assert matching_files == expected_matching_files


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
        matching_files = filecomparison.get_exclude_suffix_list()

        expected_matching_files = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\pyvenv.cfg"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\testDemo.py"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix\testRename.py"
        ]

        assert matching_files == expected_matching_files


def test_format_rules_and_tag_sort_one(monkeypatch):
    print(22)
    inputs = [1]
    inputs_list = ['N', r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule\file_name_rules.txt"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        filecomparison.format_rules_and_tag_sort()


def test_format_rules_and_tag_sort_two(monkeypatch):
    print(22)
    # 预定义输入
    inputs = [r"- E:\Videos\Newqueue 2024-01\2024-01[sort][video].mp4   <20240318-093138 250,307,839>", "END"]
    inputs_iter = iter(inputs)

    # 模拟 input 函数
    monkeypatch.setattr('builtins.input', lambda: next(inputs_iter))

    inputs_list = ['N', r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule\file_name_rules.txt"]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)

    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: 2)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 执行函数
        filecomparison.format_rules_and_tag_sort()


def test_format_rules_and_tag_sort_three(monkeypatch):
    print(22)
    # 预定义输入
    inputs = [r"- E:\Videos\Newqueue 2024-01\2024-01[sort][video].mp4   [sort][video]", "END"]
    inputs_iter = iter(inputs)

    # 模拟 input 函数
    monkeypatch.setattr('builtins.input', lambda: next(inputs_iter))

    inputs_list = ['N', r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule\file_name_rules.txt"]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)

    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: 3)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 执行函数
        filecomparison.format_rules_and_tag_sort()


def test_format_rules_and_tag_sort_four(monkeypatch):
    print(22)
    # 预定义输入
    inputs = [
        "[Rule253]",
        "ID=Replace",
        "Config=TEXTWHAT:Yuuki;TEXTWITH:Yuuki%5B%E7%BB%93%E5%9F%8E%E6%98%8E%E6%97%A5%E5%A5%88%5D;WHICH:1;SKIPEXTENSION:1;CASESENSITIVE:0;USEWILDCARDS:0;WHOLEWORDSONLY:0",
        "Marked=1",
        "Comment=",
        "",
        "[Rule254]",
        "ID=Replace",
        "Config=TEXTWHAT:Zelda;TEXTWITH:Zelda%5B%E5%A1%9E%E5%B0%94%E8%BE%BE%5D;WHICH:1;SKIPEXTENSION:1;CASESENSITIVE:0;USEWILDCARDS:0;WHOLEWORDSONLY:0",
        "Marked=1",
        "Comment=",
        "END"  # 表示输入结束
    ]
    inputs_iter = iter(inputs)

    # 模拟 input 函数
    monkeypatch.setattr('builtins.input', lambda: next(inputs_iter))

    inputs_list = ['N', r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule\file_name_rules.txt"]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)

    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: 4)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 执行函数
        filecomparison.format_rules_and_tag_sort()


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

    matche_lists, no_matche_lists = filecomparison.excel_compare()
    expected_matche_lists = []
    expected_no_matche_lists = []

    assert matche_lists == expected_matche_lists and no_matche_lists == expected_no_matche_lists


def test_get_video_audio_yes(monkeypatch):
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4"
        ,
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4"
                   ]

    # 使用 patch 来模拟 process_paths_list_or_folder 函数的行为
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 调用测试函数
        folder = fileanalysis.get_video_audio()
        expected_folder = [
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4'
        ]
        assert folder == expected_folder


def test_get_video_audio_no(monkeypatch):
    inputs = ['N',
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail'
              ]

    # 使用 patch 来模拟 process_paths_list_or_folder 函数的行为
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 调用测试函数
        folder = fileanalysis.get_video_audio()
        expected_folder = [
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\2_5228729981135230185.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6061903926607741990.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6075682606895072339.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6078060425344189964.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\5_6080421351686931793.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\corrupted_example.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\Thumb.webm'
        ]
        assert folder == expected_folder


def test_rename_with_dir(monkeypatch):
    inputs = [r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_rename"]
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    filecomparison.rename_with_dir()


def test_split_video(monkeypatch):
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4"
        ,
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = [1]
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        fileanalysis.split_video()


def test_add_srt_yes(monkeypatch):
    inputs = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk - Edgerunners - 01 [1080p]_CN-split-noaudio.mp4",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk - Edgerunners - 01 [1080p][ Subtitle].srt",
        'Y', 'Y', '200', 1]
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    fileanalysis.add_srt()


# 注意：此函数传入的字幕参数不可用用例应返回错误
def test_add_srt_no(monkeypatch):
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
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        videos_with_subtitle_stream, videos_without_subtitle_stream = fileanalysis.check_files_subtitle_stream()

        expected_videos_with_subtitle_stream = []
        expected_videos_without_subtitle_stream = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4"
            ,
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4"
        ]

        assert videos_with_subtitle_stream == expected_videos_with_subtitle_stream and \
               videos_without_subtitle_stream == expected_videos_without_subtitle_stream


def test_check_files_subtitle_stream_no(monkeypatch):
    print(32)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        videos_with_subtitle_stream, videos_without_subtitle_stream = fileanalysis.check_files_subtitle_stream()

        expected_videos_with_subtitle_stream = []
        expected_videos_without_subtitle_stream = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\2_5228729981135230185.webm"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6061903926607741990.webm"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6075682606895072339.webm"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6078060425344189964.webm"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6080421351686931793.webm"
            ,
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk - Edgerunners - 01 [1080p]_CN-split-noaudio.mp4"
            ,
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk - Edgerunners - 01 [1080p]_CN-split-noaudio_CN.mp4'
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY_EN.webm"
        ]
        assert videos_with_subtitle_stream == expected_videos_with_subtitle_stream and \
               videos_without_subtitle_stream == expected_videos_without_subtitle_stream


def test_get_directories_and_copy_tree(monkeypatch):
    inputs = [r'D:\Back\GameSaveBackupsSource\8Doors',
              r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_folder_tree']
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
    filecomparison.get_directories_and_copy_tree()


def test_check_video_integrity_yes(monkeypatch):
    print(34)
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\corrupted_example.mp4"
                   ]
    inputs = ['Y']
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
        video_integrity, video_unintegrity_list, check_video_paths = fileanalysis.check_video_integrity()

        expected_video_integrity = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4"
        ]
        expected_video_unintegrity = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\corrupted_example.mp4"
        ]
        expected_check_video_paths = []

        assert video_integrity == expected_video_integrity and video_unintegrity_list == expected_video_unintegrity \
               and check_video_paths == expected_check_video_paths


def test_check_video_integrity_no(monkeypatch):
    print(34)
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split", 'N'
                   ]
    inputs = ['Y']
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))
        video_integrity, video_unintegrity_list, check_video_paths = fileanalysis.check_video_integrity()

        expected_video_integrity = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium.mp4"
        ]
        expected_video_unintegrity = [
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium_part0.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium_part1.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split\mixkit-yellow-northern-lights-in-norway-4036-medium_part2.mp4'
        ]
        expected_check_video_paths = []

        assert video_integrity == expected_video_integrity and video_unintegrity_list == expected_video_unintegrity \
               and check_video_paths == expected_check_video_paths


def test_getfoldercount_by_include_yes(monkeypatch):
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
        , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
        , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
        , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
        , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
        , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\index.html"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\it-IT.json"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = [3, 'Y']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        f_path_list = filecount.getfoldercount_by_include()

        expected_f_path_list = [
            r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
            , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
            , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
            , r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
            , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
            , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
        ]
        assert f_path_list == expected_f_path_list


def test_getfoldercount_by_include_no(monkeypatch):
    inputs_list = ['N',
                   r"H:\videos\test\test_video_detail"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    inputs = [3, 'Y']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        f_path_list = filecount.getfoldercount_by_include()

        expected_f_path_list = [
            r"H:\videos\test\test_video_detail\2_5228729981135230185.webm"
            , r"H:\videos\test\test_video_detail\4_5956136083451284611.webm"
            , r"H:\videos\test\test_video_detail\5_6061903926607741990.webm"
            , r"H:\videos\test\test_video_detail\5_6075682606895072339.webm"
            , r"H:\videos\test\test_video_detail\5_6078060425344189964.webm"
            , r"H:\videos\test\test_video_detail\5_6080421351686931793.webm"
            , r"H:\videos\test\test_video_detail\bandicam 2022-10-09 12-03-37-846 - 副本 - 副本 (2).wmv"
            , r"H:\videos\test\test_video_detail\video_2023-06-16_16-09-25_part2.mp4"
        ]
        assert f_path_list == expected_f_path_list


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
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\it-IT.json"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = [3, 'Y', 'Y']

    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        f_path_list = filecount.getfoldercount_by_exclude()

        expected_f_path_list = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\index.html",
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\it-IT.json"  # 移除多余的空格
        ]
        assert f_path_list == expected_f_path_list


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
        f_path_list = filecount.getfoldercount_by_exclude()

        expected_f_path_list = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\alma-snortum-phelps-Lo8pE-e3AiU-unsplash.jpg"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\License.txt"
            ,
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\manu-schwendener-zFEY4DP4h6c-unsplash.jpg"
            ,
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\matt-hardy-6ArTTluciuA-unsplash.jpg"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\Stock Video Free License.txt"
        ]
        assert f_path_list == expected_f_path_list


# TODO 合并优化
def test_get_get_file_count_by_underfolder_size_yes(monkeypatch):
    print(37)
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = ['Y']

    with patch('tools.process_input_list', return_value=(path_list)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        file_list, result_wipe_list, result_list = filecount.get_file_count_by_underfolder_size()

        expected_file_list = {
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\5_6061903926607741990.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\5_6078060425344189964.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\SPYxFAMILY.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\.ts',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\2_5228729981135230185.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\4_5956136083451284611.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6061903926607741990.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6075682606895072339.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6078060425344189964.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6078060425344189964.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6080421351686931793.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk '
            r'- Edgerunners - 01 [1080p][ Subtitle].srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk '
            r'- Edgerunners - 01 [1080p][ Subtitle]_utf8.txt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk '
            r'- Edgerunners - 01 [1080p]_CN-split-noaudio.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk '
            r'- Edgerunners - 01 [1080p]_CN-split-noaudio_CN.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY_EN.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY_EN\SPYxFAMILY.srt',
            r'H:\videos\test\test_video_detail\2_5228729981135230185.webm',
            r'H:\videos\test\test_video_detail\4_5956136083451284611.webm',
            r'H:\videos\test\test_video_detail\5_6061903926607741990.webm',
            r'H:\videos\test\test_video_detail\5_6075682606895072339.webm',
            r'H:\videos\test\test_video_detail\5_6078060425344189964.webm',
            r'H:\videos\test\test_video_detail\5_6080421351686931793.webm',
            r'H:\videos\test\test_video_detail\bandicam 2022-10-09 12-03-37-846 - 副本 - '
            r'副本 (2).wmv',
            r'H:\videos\test\test_video_detail\video_2023-06-16_16-09-25_part2.mp4'
        }
        expected_result_wipe_list = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt"
            , r"H:\videos\test\test_video_detail"
        ]
        expected_result_list = []

        assert set(file_list) == set(expected_file_list)
        assert set(result_wipe_list) == set(expected_result_wipe_list)
        assert set(result_list) == set(expected_result_list)


def test_get_get_file_count_by_underfolder_size_no(monkeypatch):
    print(37)
    inputs_list = ['Y',
                   r"H:\videos\test\test_video_detail",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = ['N']

    with patch('tools.process_input_list', return_value=(path_list)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs.pop(0))
        file_list, result_wipe_list, result_list = filecount.get_file_count_by_underfolder_size()

        expected_file_list = {
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\5_6061903926607741990.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\5_6078060425344189964.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\CN\SPYxFAMILY.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\.ts',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\2_5228729981135230185.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\4_5956136083451284611.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6061903926607741990.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6075682606895072339.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6078060425344189964.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6078060425344189964.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\5_6080421351686931793.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk '
            r'- Edgerunners - 01 [1080p][ Subtitle].srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk '
            r'- Edgerunners - 01 [1080p][ Subtitle]_utf8.txt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk '
            r'- Edgerunners - 01 [1080p]_CN-split-noaudio.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\Cyberpunk '
            r'- Edgerunners - 01 [1080p]_CN-split-noaudio_CN.mp4',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY.srt',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY_EN.webm',
            r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt\video\SPYxFAMILY_EN\SPYxFAMILY.srt',
            r'H:\videos\test\test_video_detail\2_5228729981135230185.webm',
            r'H:\videos\test\test_video_detail\4_5956136083451284611.webm',
            r'H:\videos\test\test_video_detail\5_6061903926607741990.webm',
            r'H:\videos\test\test_video_detail\5_6075682606895072339.webm',
            r'H:\videos\test\test_video_detail\5_6078060425344189964.webm',
            r'H:\videos\test\test_video_detail\5_6080421351686931793.webm',
            r'H:\videos\test\test_video_detail\bandicam 2022-10-09 12-03-37-846 - 副本 - '
            r'副本 (2).wmv',
            r'H:\videos\test\test_video_detail\video_2023-06-16_16-09-25_part2.mp4'
        }
        expected_result_wipe_list = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt"
            , r"H:\videos\test\test_video_detail"
        ]
        expected_result_list = []

        assert set(file_list) == set(expected_file_list)
        assert set(result_wipe_list) == set(expected_result_wipe_list)
        assert set(result_list) == set(expected_result_list)


def test_split_audio_y(monkeypatch):
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_audio\mixkit-follow-me-home-350.mp3"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_audio\mixkit-christmas-jokes-1021.mp3"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        fileanalysis.split_audio()


def test_split_audio_n(monkeypatch):
    inputs_list = ['N',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_audio"]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs_list)
    with patch('tools.process_paths_list_or_folder', return_value=(path_list, folder)):
        # 模拟用户输入
        monkeypatch.setattr(tools, 'process_input_str_limit', lambda: inputs_list.pop(0))
        fileanalysis.split_audio()


def test_get_exclude_suffix_folder_list(monkeypatch):
    inputs_list = ['Y', r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_csv"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_exclude_suffix"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_rule"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_size_10"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_split"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_srt"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_symbolic_links"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_ts"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_rename"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_audio"
        , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count"
                   ]
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    inputs = ['.mp4' '.srt']
    with patch('tools.process_input_list', return_value=(path_list)):
        # 创建一个 MagicMock 对象来模拟 input 函数
        mocked_input = MagicMock(side_effect=inputs)
        # 使用 monkeypatch 将 input 函数替换为 MagicMock 对象
        monkeypatch.setattr('builtins.input', mocked_input)
        folders_without_extension = filecomparison.get_exclude_suffix_folder_list()

        expected_paths = [
            r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_csv"
            , r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_symbolic_links"
        ]
        assert folders_without_extension == set(expected_paths)


def test_flag_y(monkeypatch):
    inputs_list = ['Y',
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\3",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\4",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\5",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\1",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\2",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\批量提取文件名.bat"
                   ]

    path_list, folder = process_paths_list_or_folder(monkeypatch, 'Y', inputs_list=inputs_list)
    expected_paths = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\3",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\4",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\5",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\1",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\2",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\批量提取文件名.bat"
    ]

    assert path_list == expected_paths
    assert folder is None


def test_flag_n(monkeypatch):
    inputs = ['N', r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_size_10']
    path_list, folder = process_paths_list_or_folder(monkeypatch, 'N', inputs=inputs)

    expected_paths = []
    expected_folder = r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_size_10"

    assert path_list == expected_paths
    assert folder == expected_folder


def test_process_input_str_limit_pass(monkeypatch):
    long_input = 'a' * 195  # 小于195个字符的字符串

    def mock_input(prompt=''):
        return long_input

    def mock_main():
        return None

    monkeypatch.setattr('builtins.input', mock_input)
    monkeypatch.setattr('main.main', mock_main)

    try:
        # 调用需要测试的函数
        line = tools.process_input_str_limit()
    except my_exception.InputLengthExceededException as e:
        # 断言捕获的异常是期望的异常类型
        assert line <= 195
        return  # 测试通过，捕获到预期的异常
    except Exception as e:
        # 如果捕获到其他异常，则测试失败
        pytest.fail(f"Unexpected exception raised: {e}")


def test_process_input_str_limit_failed(monkeypatch):
    long_input = 'a' * 196  # 超过195个字符的字符串

    def mock_input(prompt=''):
        return long_input

    def mock_main():
        return None

    monkeypatch.setattr('builtins.input', mock_input)
    monkeypatch.setattr('main.main', mock_main)

    try:
        # 调用需要测试的函数
        tools.process_input_str_limit()
    except my_exception.InputLengthExceededException as e:
        # 断言捕获的异常是期望的异常类型
        assert isinstance(e, my_exception.InputLengthExceededException)
        return  # 测试通过，捕获到预期的异常
    except Exception as e:
        # 如果捕获到其他异常，则测试失败
        pytest.fail(f"Unexpected exception raised: {e}")

    inputs_list = (
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\3\n"
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\te\n"
        r"st_count\4\n"
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\5\n"
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\1\n"
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\2\n"
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\批量提取文件名.bat\n"
    )

    def mock_input(prompt=''):
        return inputs_list

    def mock_main():
        return None

    monkeypatch.setattr('builtins.input', mock_input)
    monkeypatch.setattr('main.main', mock_main)

    try:
        # 调用需要测试的函数
        tools.process_input_str_limit()
    except my_exception.InputLengthExceededException as e:
        # 断言捕获的异常是期望的异常类型
        assert isinstance(e, my_exception.InputLengthExceededException)
        return  # 测试通过，捕获到预期的异常
    except Exception as e:
        # 如果捕获到其他异常，则测试失败
        pytest.fail(f"Unexpected exception raised: {e}")


def process_paths_list_or_folder(monkeypatch, flag, inputs_list=None, inputs=None):
    """
    模拟不同的输入选项，并调用相应的处理函数。
    :param monkeypatch:
    :param flag:
    :param inputs_list:
    :param inputs:
    :return:
    """
    folder = None
    path_list = None
    if flag == 'Y':
        # 模拟用户选择为 'Y'

        monkeypatch.setattr('builtins.input', lambda prompt='': 'Y')
        # monkeypatch.setattr('builtins.input', lambda prompt='': inputs_list.pop(0))
        # monkeypatch.setattr(tools,'process_input_str', lambda: inputs_list.pop(0))
        path_list = handle_input_with_cmd_option(monkeypatch, inputs_list)
        # # 使用 monkeypatch 替换 get_input_paths_from_cmd


    elif flag == 'N':
        monkeypatch.setattr('tools.process_input_str_limit', lambda: inputs.pop(0))
        monkeypatch.setattr(tools, 'process_input_str', lambda: inputs.pop(0))

    if path_list is None:
        path_list, folder = tools.process_paths_list_or_folder()
    # print(f"path_list: {path_list}")
    # print(f"folder: {folder}")

    return path_list, folder


def test_handle_input_with_cmd_option(monkeypatch):
    inputs_list = ['Y', r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_count\3",
                   r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\te"]

    expected_paths = ['D:\\Develop\\PythonWorkSpace\\PythonTools\\test\\test_Data\\test_count\\3',
                      'D:\\Develop\\PythonWorkSpace\\PythonTools\\test\\test_Data\\te']
    paths = handle_input_with_cmd_option(monkeypatch, inputs_list)

    assert paths == expected_paths


def handle_input_with_cmd_option(monkeypatch, inputs_list):
    # 模拟 get_input_paths_from_cmd 返回一个预定义的文件路径列表
    def mock_get_input_paths_from_cmd():
        return inputs_list

    # 模拟用户选择 'Y' 作为命令行输入选项
    monkeypatch.setattr('builtins.input', lambda prompt='': inputs_list.pop(0))

    monkeypatch.setattr('tools.get_input_paths_from_cmd', mock_get_input_paths_from_cmd)
    # 执行测试
    result = tools.handle_input()
    print(result)
    return result


def test_get_input_paths_from_gui():
    """
    弹出 GUI 文件选择对话框以获取文件路径。
    """
    file_selector = tools.FileSelector()
    return file_selector.get_input_paths_from_gui()


def test_seconds_to_hhmmss():
    parse_time = tools.seconds_to_hhmmss(213131)
    expected_time = '59:12:11'
    print(parse_time)
    assert parse_time == expected_time


def test_get_video_resolution():
    video_path = r'D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail\mixkit-pine-covered-snowy-mountain-range-3295-medium_part1.mp4'
    resolution = tools.get_video_resolution(video_path)
    expected_resolution = (1280, 720)
    print(resolution)
    assert resolution == expected_resolution


def test_print_list_structure():
    list = [
        "这是一些测试数据",
        "这是一些测试数据",
        "19231313",
        '',
        "这是一些测试数据",
        "这是一些测试数据",
    ]
    converter = tools.check_file_or_folder
    tools.print_list_structure(list, converter=converter, prefix='这是前缀[', suffix='这是后缀]')


def test_print_dict_structure():
    key_label = '文件大小：'
    labels = ["文件路径：", "时长：", "创建时间："]
    converters = [None, None, tools.convert_timestamp]
    suffixes = ["字节", "", "秒", ""]
    data = {
        607115366: [
            (r"a:\n\test2.mp4", 857.466667, 1725022442.18),
            (r"t:\test1.mp4", 857.466667, 1724994240.9)
        ]
    }
    tools.print_dict_structure(data=data, key_label=key_label, value_labels=labels, converters=converters,
                               suffixes=suffixes)


def test_get_free_space_cmd():
    folder_path = r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_video_detail"
    space = tools.get_free_space_cmd(folder_path)
    print(f"space: {space}")


def test_copy_folder_and_copy_file():
    source_file = r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\gbk.txt"
    destination_file = r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_small\gbk.txt"
    tools.copy_file(source_file, destination_file)

    source_folder = r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_ts"
    destination_folder = r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_folder_tree"
    tools.copy_folder(source_folder, destination_folder)


def test_detect_encoding_and_convert_to_utf8():
    input_file_path = r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\gbk.txt"
    encoding = tools.detect_encoding(input_file_path)
    output_file_path = tools.convert_to_utf8(input_file_path, encoding)
    expected_output_file_path = r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\gbk_utf8.txt"
    print(output_file_path)
    assert output_file_path == expected_output_file_path


def test_profile_file():
    methods = {
        0: tools.profile_all_functions,
        1: fileSize.get_total_file_size,
        2: fileSize.get_total_size,
    }
    profile_file = 'Profile'
    print("Profile enabled.")
    # 创建一个空的 Profile 文件
    with open(profile_file, 'w', encoding='UTF-8'):
        pass

    file_paths = [
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\index.html",
        r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\it-IT.json"
    ]
    user_input = 2
    if os.path.exists(profile_file):
        enable_profile = True
        methods = tools.apply_profile_to_methods(enable_profile, methods)
    methods.get(user_input, methods)(file_paths)
    if os.path.exists(profile_file):
        os.remove(profile_file)


import cv2
import ffmpeg
import py7zr
import rarfile


def test_global_exception_handler():
    class FileSelector:
        def __init__(self):
            self.file_paths = []
            self.gui_thread = None

    fileSelector = FileSelector()

    try:
        raise ffmpeg._probe.Error('', 'out', 'error')
    except ffmpeg._probe.Error as e:
        global_exception_handler(type(e), e, e.__traceback__)

    try:
        raise py7zr.Bad7zFile(fileSelector)
    except py7zr.Bad7zFile as e:
        global_exception_handler(type(e), e, e.__traceback__)

    try:
        raise rarfile.Error(fileSelector)
    except rarfile.Error as e:
        global_exception_handler(type(e), e, e.__traceback__)


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

    print('-' * 50 + 'All TestCase End' + '-' * 50)
    print("注意！如果未初始化测试数据多次测试会导致三个接口不通过，这是符合预期的结果")
    # e =d*c
    # print(e)


# 运行测试用例
if __name__ == "__main__":
    run_test_scase()
