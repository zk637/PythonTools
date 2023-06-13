# This is a sample Python script.
import atexit
import fileSize
import filecount
import fileduration
import getresolution
import removefolder
import srt
import datetime
import zippackage
from loggerconifg import Logger
from loggerconifg import InputLogger
from loggerconifg import createog
from loggerconifg import exit_handler
import sys
import translate


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
    #  10、获取文件在大小区间下的列表                       code==10
    #  11、取文件夹下所有视频文件的时长并排序输出             code==11
    #  12、12、获取给定文件夹下的 "大小", "时长", "比特率", "分辨率（排序需录入对应的属性）
    #  13、获取给定目录中在检索目录下以相同文件名匹配的列表
    #  14、取传入目录下所有与文件名一致的jpg创建.ts文件夹并移入
    #  15、获取文件夹下所有文件的路径，并返回文件名符合指定规则的文件路径列表 （支持文件名规则匹配 目前只支持 *keyword*匹配）
    #  16、获取两个目录下所有路径，源文件的文件名和目标文件的文件夹名一致则建立符号链接（需管理员权限）
    #  17、为指定的文件列表在指定目录下创建符号链接（需管理员权限）支持文件和文件夹混合
    #  18、判断指定文件夹下的压缩文件是否加密
    #  19、判断指定文件夹下的压缩文件是否加密-精确(支持7z分卷格式）
    #  20、获取符合录入文件名的文件路径"""
    while True:
        # 需要重复执行的代码
        # ...
        def default_method():
            print("Invalid input")
        methods = {
            1: fileSize.get_total_file_size,
            2: fileSize.def_get_total_size,
            3: srt.getSrt,
            4: srt.getSrtNew,
            5: translate.find_matching_subtitles,
            6: translate.find_matching_subtitles_create,
            7: getresolution.get_low_resolution_media_files,
            8: removefolder.remove_small_folders,
            9: filecount.getfoldercount,
            10: fileSize.filter_files_by_size,
            11: fileduration.get_video_duration_sorted,
            12: fileduration.print_video_info_list,
            13: fileduration.check_files_in_folder,
            14: fileduration.compare_and_move_files,
            15: fileduration.get_file_paths_with_rules,
            16: fileduration.create_symbolic_links,
            17: fileduration.same_file_createsymbolic_links,
            18: zippackage.check_zip_password,
            19: zippackage.extract_archive,
            20: fileduration.get_file_paths_with_name
            # 17: fileduration.compare_file_and_folder_names
        }
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n-------------------------------------当前时间是: {time_str}-------------------------------------")
        print(    """1、获取相同子目录下的文件大小            code==01
    #  2、获取不同子目录下的文件大小         code==02
    #  3、使用关键词来查找字幕文件           code==03
    #  4、匹配视频目录下对应的字幕文件并返回列表  code==04
    #  5、通过视频路径查找字幕文件列表（支持模糊匹配）           code==05
    #  6、通过视频路径查找字幕文件并创建目录     code==06
    #  7、通过视频目录查找符合区间条件分辨率的媒体文件          code==07
    #  8、删除文件夹下小于指定MB的文件并输出删除的文件列表   code==08
    #  9、获取文件列表下的文件数量                           code==09
    #  10、获取文件在大小区间下的列表                       code==10
    #  11、取文件夹下所有视频文件的时长并排序输出             code==11
    #  12、12、获取给定文件夹下的 "大小", "时长", "比特率", "分辨率（排序需录入对应的属性）
    #  13、获取给定目录中在检索目录下以相同文件名匹配的列表
    #  14、取传入目录下所有与文件名一致的jpg创建.ts文件夹并移入
    #  15、获取文件夹下所有文件的路径，并返回文件名符合指定规则的文件路径列表 （支持文件名规则匹配 目前只支持 *keyword*匹配）
    #  16、获取两个目录下所有路径，源文件的文件名和目标文件的文件夹名一致则建立符号链接（需管理员权限）
    #  17、为指定的文件列表在指定目录下创建符号链接（需管理员权限）支持文件和文件夹混合
    #  18、判断指定文件夹下的压缩文件是否加密
    #  19、判断指定文件夹下的压缩文件是否加密-精确(支持7z分卷格式）
    #  20、获取符合录入文件名的文件路径""")
        input_logger = InputLogger(out_put)
        input_logger.start_logging()
        print("# 输入对应的编号")
        print("--------------------------------------------------In-----------------------------------------------------")
        try:
            user_input = int(input("Enter a number: \n"))
            if user_input == 1 or user_input == 2 or user_input == 13:
                # 再将标准输出和标准错误输出重定向回自定义的 MyStream 对象
                file_paths = []
                while True:
                    # input_logger = InputLogger('output.txt')
                    # input_logger.start_logging()
                    path = input("请输入文件路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
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
                methods.get(user_input, default_method)()
                print(
                    f"--------------------------------------------------End----------------------------------------------------")
            input_logger.stop_logging()
            input_logger.close()
            print("是否继续执行？(Y/N)\n")
            user_input = input()
            if user_input.lower() == "y":
                # 继续执行，回到程序开头
                continue
            elif user_input.lower() == "n":
                # 结束循环，退出程序
                break
            else:
                # 提示输入有误，请重新输入
                print("输入有误，请重新输入！")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    # logging.basicConfig(filename='output.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')



