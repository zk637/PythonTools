# This is a sample Python script.
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
from loggerconifg import InputLogger
from loggerconifg import createog
from loggerconifg import exit_handler
import sys



sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
out_put=createog()

sys.stdout = Logger(f'{out_put}', sys.stdout)
# sys.stderr = Logger('output_f.log', sys.stderr)
sys.stderr = Logger(f'{out_put}', sys.stderr)
atexit.register(exit_handler)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.




if __name__ == '__main__':
    """1、获取相同子目录下的文件大小            code==01
    #  2、获取不同子目录下的文件大小         code==02
    #  3、使用关键词来查找字幕文件           code==03
    #  4、匹配视频目录下对应的字幕文件并返回列表  code==04
    #  5、通过视频路径查找字幕文件列表（支持模糊匹配）           code==05
    #  6、通过视频路径查找字幕文件并创建目录     code==06
    #  7、通过视频目录查找符合区间条件分辨率的媒体文件          code==07
    #  8、删除文件夹下小于指定MB的文件并输出删除的文件列表   code==08
    #  9、获取文件列表下的文件数量                           code==09
    #  10、获取文件在大小区间下的列表或在修改时间区间下的列表       code==10
    #  11、取文件夹下所有视频文件的时长并排序输出或输出时长大小相同的文件            code==11
    #  12、获取给定文件夹下的 "大小", "时长", "比特率", "分辨率（排序需录入对应的属性）
    #  13、获取给定文件夹下在检索路径列表中以相同文件名匹配的列表或获取不匹配相同文件名的列表
    #  14、取传入目录下所有与文件名一致的jpg创建.ts文件夹并移入
    #  15、获取文件夹下所有文件的路径，并返回文件名符合指定规则的文件路径列表 （支持文件名模糊规则匹配）
    #  16、获取两个目录下所有路径，源文件的文件名和目标文件的文件夹名一致则建立符号链接（需管理员权限）
    #  17、为指定的文件列表在指定目录下创建符号链接（需管理员权限）支持文件和文件夹混合
    #  18、判断指定文件夹下的压缩文件是否加密
    #  19、判断指定文件夹下的压缩文件是否加密-精确(支持7z分卷格式）
    #  20、获取检索文件夹下和检索文件名相同的路径列表
    #  21、获取不在指定后缀的文件路径（输入为路径列表或文件夹）
    #  22、过滤规则格式化
    #  23、校验文件是否合法
    #  24、检查录入文件夹下的符号链接是否可用
    #  25、文件自动备份（更新-需提前创建符号链接）
    #  26、文件自动备份（创建-需提前创建符号链接）
    #  27、文件夹内容与csv对比
    #  28、获取给定文件夹或文件的音频文件
    #  29、文件夹下视频命名规范化
    #  30、根据限制大小拆分视频为多段
    #  31、为视频文件添加字幕
    #  32、检查视频是否存在字幕流
    #  33、获取指定文件夹下的目录结构并复制
    #  34、获取指定文件列表或文件夹下的视频是否完整
    #  35、获取指定文件类型的文件数量和路径
    #  36、获取指定文件类型外文件的数量和路径
    #  37、获取录入文件列表中子文件大于3GB且存在3个以上文件的文件夹并输出不符合条件的文件夹"""
    while True:
        # 需要重复执行的代码
        # ...
        def default_method():
            pass
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
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n-------------------------------------当前时间是: {time_str}-------------------------------------")
        print("""    #  1、获取相同子目录下的文件大小          
    #  2、获取不同子目录下的文件大小         
    #  3、使用关键词来查找字幕文件          
    #  4、匹配视频目录下对应的字幕文件并返回列表 
    #  5、通过视频路径查找字幕文件列表（支持模糊匹配）           
    #  6、通过视频路径查找字幕文件并创建目录    
    #  7、通过视频目录查找符合区间条件分辨率的媒体文件         
    #  8、删除文件夹下小于指定MB的文件并输出删除的文件列表  
    #  9、获取文件列表下的文件数量                           
    #  10、获取文件在大小区间下的列表或在修改时间区间下的列表     
    #  11、取文件夹或列表下所有视频文件的时长并排序输出或输出时长大小相同的文件      
    #  12、获取给定文件夹下的 "大小", "时长", "比特率", "分辨率（排序需录入对应的属性）
    #  13、获取给定文件夹下在检索路径列表中以相同文件名匹配的列表或获取不匹配相同文件名的列表
    #  14、取传入目录下所有与文件名一致的jpg创建.ts文件夹并移入
    #  15、获取文件夹下所有文件的路径，并返回文件名符合指定规则的文件路径列表 （支持文件名模糊规则匹配）
    #  16、获取两个目录下所有路径，源文件的文件名和目标文件的文件夹名一致则建立符号链接（需管理员权限）
    #  17、为指定的文件列表在指定目录下创建符号链接（需管理员权限）支持文件和文件夹混合
    #  18、判断指定文件夹下的压缩文件是否加密
    #  19、判断指定文件夹下的压缩文件是否加密-精确(支持7z分卷格式）
    #  20、获取检索文件夹下和检索文件名相同的路径列表
    #  21、获取不在指定后缀的文件路径（输入为路径列表或文件夹）
    #  22、过滤规则格式化
    #  23、校验文件是否合法
    #  24、检查录入文件夹下的符号链接是否可用
    #  25、文件自动备份（更新-需提前创建符号链接）
    #  26、文件自动备份（创建-需提前创建符号链接）
    #  27、文件夹内容与csv对比
    #  28、获取给定文件夹或文件的音频文件
    #  29、文件夹下视频命名规范化
    #  30、根据限制大小拆分视频为多段
    #  31、为视频文件添加字幕
    #  32、检查视频是否存在字幕流
    #  33、获取指定文件夹下的目录结构并复制
    #  34、获取指定文件列表或文件夹下的视频是否完整
    #  35、获取指定文件类型的文件数量和路径
    #  36、获取指定文件类型外文件的数量和路径
    #  37、获取录入文件列表中子文件大于3GB且存在3个以上文件的文件夹并输出不符合条件的文件夹""")
        profile_file = 'Profile'
        input_logger = loggerconifg.check_log_size(out_put)
        input_logger.start_logging()
        print("# 输入对应的编号")
        print("--------------------------------------------------In-----------------------------------------------------")
        try:
            print("Enter a number: \n")
            user_input = int(input().strip())
            if user_input == 0:
                # 如果用户输入0，则开启 profile
                enable_profile = True
                print("Profile enabled.")
                # 创建一个空的 Profile 文件
                with open(profile_file, 'w',encoding='UTF-8'):
                    pass
                continue
            elif user_input == -1:
                # 如果用户输入-1，则退出循环
                break
            if user_input == 1 or user_input == 2 or user_input == 13:
                # 再将标准输出和标准错误输出重定向回自定义的 MyStream 对象
                file_paths = []
                print("请输入文件路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
                while True:
                    # input_logger = InputLogger('output.txt')
                    # input_logger.start_logging()
                    path = input()
                    # input_logger.stop_logging()
                    # input_logger.close()
                    if not path:
                        break
                    file_paths.append(path.strip('"'))
                methods.get(user_input, default_method)(file_paths)
                input_logger.stop_logging()
                input_logger.close()
                print(
                    f"--------------------------------------------------End----------------------------------------------------")
            else:
                if os.path.exists(profile_file):
                    enable_profile = True
                    methods = tools.apply_profile_to_methods(enable_profile, methods)
                methods.get(user_input, default_method())()
                print(
                    f"--------------------------------------------------End----------------------------------------------------")
            input_logger.stop_logging()
            input_logger.close()
            print("是否继续执行？(Y/N)\n")
            user_input = tools.process_input_str()
            if user_input.upper() == "Y":
                # 继续执行，回到程序开头
                continue
            elif user_input.upper() == "N":
                # 结束循环，退出程序
                if os.path.exists(profile_file):
                    os.remove(profile_file)
                break
            else:
                # 提示输入有误，请重新输入
                print("输入有误，请重新输入！")
                continue
        except ValueError:
            if os.path.exists(profile_file):
                os.remove(profile_file)
            print("Invalid input. Please enter a valid integer.")
    # logging.basicConfig(filename='output.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')



