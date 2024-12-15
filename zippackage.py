'''

@Contact :   https://github.com/zk637/PythonTools
@License :   Apache-2.0 license
'''
import datetime
import os
import re
import subprocess
import shutil
import sys
import zipfile
import py7zr
import rarfile
import constants
import tools

# 注册模块对象
from model import tips_m, log_info_m, result_m

# 注册全局异常处理函数
from my_exception import global_exception_handler

global_exception_handler = global_exception_handler


def check_zip_password_old():
    """判断指定文件夹下的压缩文件是否加密（不支持7z分卷）"""
    tips_m.print_message(message="请输入需要检索的文件夹")
    var = tools.process_input_str_limit()
    tips_m.print_message(message="是否处理7zip格式？ y/n")
    zipflag = tools.process_input_str_limit()
    if zipflag and zipflag.upper() == 'Y':
        tips_m.print_message(message="选择7zip的处理模式 r-(默认：读取现有文件),w-(截断并写入新文件可以解决部分7z文件报错的情况),a-(追加到现有文件)")
        flag = tools.process_input_str_limit() or 'R'
        if flag.upper() not in ['R', 'W', 'A']:
            raise ValueError('错误的参数！')
    rar_lists = []
    sevenzip_lists = []
    # final_lists_rar=[]
    # final_lists_7z=[]
    final_lists = []
    ex_final_lists = []
    # final_list=tools.get_zippartfile(var)
    zip_list = tools.get_file_paths_limit(var, '.zip')
    sevenzip_lists = tools.get_file_paths_limit(var, ".7z")
    rar_lists = tools.get_file_paths_limit(var, ".rar")
    # file_paths = tools.get_file_paths_limit(var, ".zip")
    # sevenzip_lists = tools.get_file_paths_limit(var, ".7z")
    # rar_lists = tools.get_file_paths_limit(var, ".rar")
    """检查压缩文件是否有密码"""
    # file_path.strip('"')
    if zipflag and zipflag.upper() == 'Y' and sevenzip_lists:
        # print(datetime.datetime.now())
        for sevenzip_list in sevenzip_lists:
            try:
                if os.access(sevenzip_list, mode=os.W_OK):
                    with py7zr.SevenZipFile(sevenzip_list, mode=flag) as archive:
                        if archive.needs_password():
                            final_lists.append(sevenzip_list)
                            # print(f'{sevenzip_list} 存在密码')
                        else:
                            ex_final_lists.append(sevenzip_list)
                            # print(f'{sevenzip_list} 没有密码')
            except Exception as e:
                if 'Password is required for extracting given archive.' in str(e):
                    final_lists.append(sevenzip_list)
                    pass
                else:
                    log_info_m.print_message(message=f'{sevenzip_list} 不是有效的7z压缩文件')
    if zip_list:
        for zip in zip_list:
            try:
                zf = zipfile.ZipFile(zip)
                for zinfo in zf.infolist():
                    is_encrypted = zinfo.flag_bits & 0x1
                    if is_encrypted:
                        final_lists.append(zip)
                    else:
                        ex_final_lists.append(zip)
            except (zipfile.BadZipfile, subprocess.CalledProcessError) as err:
                pass
    if rar_lists:
        for rar_list in rar_lists:
            try:
                rf = rarfile.RarFile(rar_list)
                if rf.needs_password():
                    final_lists.append(rar_list)
                    # print(f"{rar_list} - Password required.")
                else:
                    # print(f"{rar_list} - No password needed.")
                    ex_final_lists.append(rar_list)
            except rarfile.NeedFirstVolume:
                pass
            except Exception as e:
                if isinstance(e, rarfile.NeedFirstVolume):
                    pass
                else:
                    log_info_m.print_message(message=rar_list + "发生错误：")
                    global_exception_handler(type(e), e, e.__traceback__)
                    pass
    # 去重
    ex_final_lists = set(ex_final_lists)
    final_lists = set(final_lists)
    """遍历结果"""
    log_info_m.print_message(
        message="--------------------------------------------------无密码----------------------------------------------------")
    tools.print_list_structure(sorted(ex_final_lists))
    log_info_m.print_message(
        message="--------------------------------------------------有密码----------------------------------------------------")
    tools.print_list_structure(sorted(final_lists))
    # print(datetime.datetime.now())


def zip_process_conception():
    process_map = {
        1: encryp_judgment,
        2: verify_zip,
        3: extract_zip,
    }
    tips_m.print_message(message="请输入要执行的操作（1-判断指定文件夹下的压缩文件是否加密， 2-批量校验压缩包, 3-批量解压缩）")
    index = int(tools.process_input_str_limit())

    process_function = process_map.get(index)

    if process_function:
        log_info_m.print_message(f"process_name: {process_function.__name__}")
        process_function()  # 调用对应的函数
    else:
        result_m.print_message("参数有误！")


# TODO 更多格式的判断
def encryp_judgment():
    """判断指定文件夹下的压缩文件是否加密-精确(支持7z分卷格式）"""
    tips_m.print_message(message="请输入文件夹")
    folder = tools.process_input_str_limit()

    filelists = tools.get_file_paths_limit(folder, *constants.ZIP_SUFFIX)
    file_list = tools.get_file_paths(folder)

    file_parts_lists = tools.keep_duplicate_files(file_list)

    final_lists = set()
    ex_lists = set()
    flag = True
    if hasattr(sys, '_MEIPASS') and flag:
        # 打包后的 exe 运行环境
        exe_path = sys.executable
        target_path = os.path.join(os.path.dirname(exe_path), '7z.exe')
        flag = False
        target_path_dll = os.path.join(os.path.dirname(exe_path), '7z.dll')
    else:
        # 非打包调试环境
        target_path = os.path.join(os.getcwd(), '7z.exe')
        target_path_dll = os.path.join(os.getcwd(), '7z.dll')
        flag = False
    if not os.path.exists(target_path):
        # 从打包后的 exe 文件中复制
        source_path = os.path.join(sys._MEIPASS, '7z.exe')
        source_path_dll = os.path.join(sys._MEIPASS, '7z.dll')
        shutil.copy2(source_path, target_path)
        shutil.copy2(source_path_dll, target_path_dll)
        flag = False
    if flag == False:
        log_info_m.print_message(message=datetime.datetime.now())
        log_info_m.print_message(message="正在执行：压缩文件的加密判断...")
        zip_path_list = tools.get_file_paths_list_limit(filelists, '.zip')
        rar_path_list = tools.get_file_paths_list_limit(filelists, '.rar')
        seven_z_path_list = tools.get_file_paths_list_limit(filelists, '.7z')

        if zip_path_list:
            for zip in zip_path_list:
                if check_zip_password(zip) == True:
                    final_lists.add(zip)
                else:
                    ex_lists.add(zip)
        if rar_path_list:
            for rar in rar_path_list:
                if check_rar_password(rar) == True:
                    final_lists.add(rar)
                else:
                    ex_lists.add(rar)
        if seven_z_path_list:
            for seven in seven_z_path_list:
                output = check_seven_z_password(seven)
                if "ERROR: Wrong password" in output or "Data Error" in output or \
                        'Cannot open encrypted archive. Wrong password?' in output:
                    final_lists.add(seven)
                else:
                    ex_lists.add(seven)

        log_info_m.print_message(message="正在执行：7z分卷压缩文件的加密判断...")
        file_sevenparts_lists = tools.register_findone(file_list, r"(\.7z\.\d+)")
        # print(file_sevenparts_lists)
        if file_sevenparts_lists:
            for file_parts_list in file_sevenparts_lists:
                output = check_seven_z_password(file_parts_list[0])
                if "ERROR: Wrong password" in output or "Data Error" in output or \
                        'Cannot open encrypted archive. Wrong password?' in output:
                    final_lists.update(file_parts_list)
                else:
                    ex_lists.update(file_parts_list)

        log_info_m.print_message(message="正在执行：zip分卷压缩文件的加密判断...")

        file_zipparts_lists = tools.register_findone(file_parts_lists, "([\*^\.$]+[z$][0$+][0$+\d])+")
        # print(file_zipparts_lists)
        if file_zipparts_lists:
            for file_zipparts in file_zipparts_lists:
                # list = ','.join('"{0}"'.format(x) for x in file_zipparts_lists).replace(',', " ")
                # 如果文件组有内容则代表是分卷因为是zip分卷需要手动替换后缀
                if not tools.check_is_None(file_zipparts[0]):
                    file_zipparts_head = file_zipparts[0][:file_zipparts[0].rfind('.')] + '.zip'
                    # print(file_zipparts)
                    if check_zip_password(file_zipparts_head) == True:
                        final_lists.update(file_zipparts)
                    else:
                        ex_lists.update(file_zipparts)

        log_info_m.print_message(message="正在执行：rar分卷压缩文件的加密判断...")
        # print(file_parts_lists)
        file_rarparts_lists = tools.register_findone(filelists, "([\*^\.$])part\d+\.rar")
        if file_rarparts_lists:
            for file_rarparts in file_rarparts_lists:
                # list = ','.join('"{0}"'.format(x) for x in file_rarparts_lists_group).replace(',', " ")
                if not tools.check_is_None(file_rarparts[0]):

                    if check_rar_password(file_rarparts[0]) == True:
                        final_lists.update(file_rarparts)
                    else:
                        ex_lists.update(file_rarparts)

        if ex_lists:
            ex_lists = ex_lists - final_lists
            result_m.print_message(message=
                                   "--------------------------------------------------无密码----------------------------------------------------")
            tools.print_list_structure(sorted(ex_lists))
        if final_lists:
            result_m.print_message(message=
                                   "--------------------------------------------------有密码----------------------------------------------------")
            tools.print_list_structure(sorted(final_lists))
        print(datetime.datetime.now())
        if not tools.check_is_None(final_lists, ex_lists):
            return sorted(ex_lists), sorted(final_lists)


def get_archive_uncompressed_size(zip_path):
    """获取压缩包解压后所需的磁盘空间"""
    try:
        # 调用 7z 命令并获取输出
        cmd = f'"D:\\Green software\\7-Zip\\7z.exe" l "{zip_path}"'
        result = subprocess.run(cmd, capture_output=True, text=True)

        # 检查是否成功运行
        if result.returncode != 0:
            result_m.print_message(f"无法处理压缩包 {zip_path}，错误信息:\n{result.stderr}")
            return 0

            # 解析输出以获取未压缩大小
        uncompressed_size = 0
        lines = result.stdout.splitlines()

        log_info_m.print_message("命令输出:", result.stdout)  # 查看命令输出

        for line in lines:
            # 检查最后一行，寻找包含未压缩大小的行
            if "files" in line:  # 检查是否为最后统计信息行
                # parts = line.split()
                try:
                    # 更新正则表达式：限制最后部分为文件名，而不是 "files" 或 "folders"
                    summary_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s+(\d+)\s+\d+\s+\d+ files')
                    match = summary_pattern.search(line)

                    if match:
                        uncompressed_size = int(match.group(1))  # 提取未压缩大小
                        return uncompressed_size
                    else:
                        print(f"未匹配汇总行: {line}")
                except ValueError as e:
                    result_m.print_message(f"解析错误: {e} - 行内容: {line}")  # 输出错误行以便调试

        return uncompressed_size
    except Exception as e:
        result_m.print_message(f"处理压缩包 {zip_path} 时出错: {e}")
        return 0


def verify_zip():
    parent_folder, zip_paths, passwords = tools.get_input_paths_and_passes()
    if zip_paths and passwords:
        # 如果只输入一行密码，将该密码应用于所有文件
        if len(passwords) == 1:
            passwords = passwords * len(zip_paths)

        for zip_path, password in zip(zip_paths, passwords):
            if not os.path.isfile(zip_path):
                result_m.print_message(f"压缩包 {zip_path} 无效，跳过...")
                continue
            # 定义验证压缩包命令
            cmd = f'"D:\Softwere green\winrar\WinRAR.exe" t -p"{password}" "{zip_path}"'
            tools.subprocess_with_progress(cmd, success_tip=f"验证通过： {zip_path} ", faild_tip=f"False:验证失败： {zip_path} ")

        total_uncompressed_size = 0
        print('-' * 50)
        for zip_path in zip_paths:
            if not os.path.isfile(zip_path):
                result_m.print_message(f"压缩包 {zip_path} 无效，跳过...")
                continue
            # 获取解压后所需的空间
            uncompressed_size = get_archive_uncompressed_size(zip_path)
            result_m.print_message(f"压缩包 {zip_path} 解压后需要空间: {tools.display_size_in_mb(uncompressed_size)} MB")
            total_uncompressed_size += uncompressed_size

        # 输出总的解压空间
        result_m.print_message(f"\n所有压缩包解压后总共需要空间: {tools.display_size_in_mb(total_uncompressed_size)} MB")


def extract_zip():
    parent_folder, zip_paths, passwords = tools.get_input_paths_and_passes(parent_flag=True)
    if parent_folder and zip_paths and passwords:
        # 如果只输入一行密码，将该密码应用于所有文件
        if len(passwords) == 1:
            passwords = passwords * len(zip_paths)

        for zip_path, password in zip(zip_paths, passwords):
            if not os.path.isfile(zip_path):
                result_m.print_message(f"压缩包 {zip_path} 无效，跳过...")
                continue
            # 创建子文件夹
            zip_name = os.path.splitext(os.path.basename(zip_path))[0]
            extract_folder = os.path.join(parent_folder, zip_name)
            os.makedirs(extract_folder, exist_ok=True)

            # 定义解压缩命令
            cmd = f'"D:\Softwere green\winrar\WinRAR.exe" x -p"{password}" "{zip_path}" "{extract_folder}\\"'
            tools.subprocess_with_progress(cmd, success_tip=f"成功解压 {zip_path} 到 {extract_folder}",
                                           faild_tip=f"False:解压 {zip_path} 失败")


def get_rar_header_type(rar_file_path):
    # 打开RAR文件
    with rarfile.RarFile(rar_file_path) as rf:
        # 获取文件信息列表
        file_info_list = rf.infolist()

        # 选择第一个文件信息对象
        file_info = file_info_list[0]

        # 获取 Header type 标头类型
        header_type = file_info.flags
        return header_type


def check_rar_password(rar_file_path):
    """检查rar文件是否需要密码，返回布尔值"""
    try:
        # 打开RAR文件
        with rarfile.RarFile(rar_file_path) as rf:
            # 检查RAR文件是否需要密码
            needs_password = rf.needs_password()
            if needs_password:
                return True
            else:
                return False
    except (rarfile.NotRarFile, subprocess.CalledProcessError, rarfile.NeedFirstVolume) as err:
        pass
        # print(err)
        # print('as file:'+rar_file_path)


def check_zip_password(zip_file_path):
    """检查zip文件是否需要密码，返回布尔值"""
    try:
        zf = zipfile.ZipFile(zip_file_path)
        for zinfo in zf.infolist():
            is_encrypted = zinfo.flag_bits & 0x1
            if is_encrypted:
                return True
            else:
                return False
    except (zipfile.BadZipfile, subprocess.CalledProcessError) as err:
        pass
        # print(err)
        # print('as file:' + zip_file_path)


def check_seven_z_password(seven_file_path):
    """检查7z文件是否需要密码，返回布尔值"""
    try:
        command = f'7z t -p "{seven_file_path}"'
        # print(command)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as err:
        output = err.output

    output = output.decode('gbk')
    return output


def extract_and_print_binary_data(rar_file_path):
    with rarfile.RarFile(rar_file_path) as rf:
        # 读取压缩源文件数据区
        print(rf.needs_password())
        # compressed_data = rf.read('compressed_data.bin')
        #
        # # 读取压缩源文件目录区
        # file_info_list = rf.infolist()
        # directory_data = b''
        # for file_info in file_info_list:
        #     directory_data += file_info.FileHeader.to_binary() + file_info.file_header.raw
        #
        # # 读取压缩源文件目录结束标志
        # end_of_directory = rf.end_of_directory
        #
        # return compressed_data, directory_data, end_of_directory


def test():
    # 调用函数并传入RAR文件路径
    # rar_file_path = r"D:\Green software\zip\test\test2.part1.rar"
    # extract_and_print_binary_data(rar_file_path)
    res = check_rar_password(r"D:\Develop\PythonWorkSpace\PythonTools\test\test_Data\test_zip\test_1.part1.rar")
    print(res)
    # 打印提取的二进制数据
    # print("Compressed Data:")
    # print(compressed_data)
    # print("\nDirectory Data:")
    # print(directory_data)
    # print("\nEnd of Directory:")
    # print(end_of_directory)
