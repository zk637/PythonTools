import datetime
import os
import re
import subprocess
import shutil
import sys
import zipfile
import py7zr
import patoolib
import rarfile
import tools


def check_zip_password():
    print("请输入需要检索的文件夹")
    var = input()
    print("是否处理7zip格式？ y/n")
    zipflag = input()
    if str(zipflag).lower() == 'y':
        print("选择7zip的处理模式 r-(默认：读取现有文件),w-(截断并写入新文件可以解决部分7z文件报错的情况),a-(追加到现有文件)")
        flag = input() or 'r'
        flag = str(flag)
    rar_lists = []
    sevenzip_lists = []
    # final_lists_rar=[]
    # final_lists_7z=[]
    final_lists = []
    ex_final_lists = []
    # final_list=tools.get_zippartfile(var)
    file_paths = tools.get_file_paths_limit(var, ".zip", ".gz", "xz", ".bz2", ".tar", ".tar.gz",
                                            ".tar.xz",
                                            ".tar.bz2", ".gz", ".bz2", ".lzma", ".cab", ".zipx")
    sevenzip_lists = tools.get_file_paths_limit(var, ".7z")
    rar_lists = tools.get_file_paths_limit(var, ".rar")
    # file_paths = tools.get_file_paths_limit(var, ".zip")
    # sevenzip_lists = tools.get_file_paths_limit(var, ".7z")
    # rar_lists = tools.get_file_paths_limit(var, ".rar")
    """检查压缩文件是否有密码"""
    # file_path.strip('"')
    if zipflag.lower() == 'y':
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
            except py7zr.exceptions.Bad7zFile as e:
                pass
                print(f'{sevenzip_list} 不是有效的7z压缩文件')
    for file_path in file_paths:
        try:
            patoolib.test_archive(file_path, verbosity=-1)
            # patoolib.test_archive(file_path, program=f'D:\\Softwere green\\winrar\\WinRAR.exe' ,verbosity=-1)
            # patoolib.test_archive(file_path, program=f"D:\\Green software\\7-Zip\\7zFM.exe" ,verbosity=-1)
            ex_final_lists.append(file_path)
            # print(file_path + "无密码")
            # return False  # No password protection
        except patoolib.util.PatoolError as e:
            if "password required" in str(e):
                final_lists.append(file_path)
                # print(file_path + "存在密码")
                # return True  # Password protected
            else:
                print(file_path + "发生错误：")
                print(e)
                pass
    for rar_list in rar_lists:
        try:
            rf = rarfile.RarFile(rar_list)
            if rf.needs_password():
                final_lists.append(rar_list)
                # print(f"{rar_list} - Password required.")
            else:
                # print(f"{rar_list} - No password needed.")
                ex_final_lists.append(rar_list)
        except Exception as e:
            print(rar_list + "发生错误：")
            print(e)
            pass
    """遍历结果"""
    print("--------------------------------------------------无密码----------------------------------------------------")
    for ex_final_list in ex_final_lists:
        print(ex_final_list)
    print("--------------------------------------------------有密码----------------------------------------------------")
    for final_list in final_lists:
        print(final_list)
    # print(datetime.datetime.now())

#TODO 更多格式支持和更精确的检索

def extract_archive():
    print("请输入文件夹")
    folder = input()
    password = "password"
    # filelists = tools.get_file_paths(folder)
    filelists = tools.get_file_paths_limit(folder, ".7z", ".rar", ".zip", ".gz", "xz", ".bz2", ".tar", ".tar.gz",
                                           ".tar.xz",
                                           ".tar.bz2", ".gz", ".bz2", ".lzma", ".cab", ".zipx")
    folder = tools.get_file_paths(folder)
    # file_parts_lists = tools.get_files_matching_pattern(folder,r'.*.[^.]*0[^.]*$')
    # lists=tools.get_same_namefile(folder)
    file_parts_lists = tools.keep_duplicate_files(folder)
    # file_zipparts_lists=tools.register_find(file_parts_lists,"([\*^\.$]+[z$][0$+][0$+\d])+")
    # file_rarparts_lists=tools.register_find(filelists,"(([\*^\.$]part\d)([\*^\.$]rar))")
    final_lists = []
    ex_lists = []
    flag=True
    if hasattr(sys, '_MEIPASS') and flag:
        # 打包后的 exe 运行环境
        exe_path = sys.executable
        target_path = os.path.join(os.path.dirname(exe_path), '7z.exe')
        flag=False
        target_path_dll = os.path.join(os.path.dirname(exe_path), '7z.dll')
    else:
        # 非打包调试环境
        target_path = os.path.join(os.getcwd(), '7z.exe')
        target_path_dll = os.path.join(os.getcwd(), '7z.dll')
        flag=False
    if not os.path.exists(target_path):
        # 从打包后的 exe 文件中复制
        source_path = os.path.join(sys._MEIPASS, '7z.exe')
        source_path_dll=os.path.join(sys._MEIPASS, '7z.dll')
        shutil.copy2(source_path, target_path)
        shutil.copy2(source_path_dll, target_path_dll)
        flag=False
    if flag==False:
        print(datetime.datetime.now())
        print("正在执行：压缩文件的加密判断...")
        for filelist in filelists:
            try:
                # command = f'cmd_·zip.bat "{filelist}"'
                # path_to_7z=os.path.join("\\lib\\7z.exe")
                command = f'7z t -p "{filelist}"'
                # print(command)
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError as err:
                output = err.output

            output = output.decode('gbk')
            if "ERROR: Wrong password" in output or "Data Error" in output:
                match = re.search(r"(([\*^\.$]part\d)([\*^\.$]rar))", filelist,
                                  re.UNICODE)
                if not match:
                    final_lists.append(filelist)
                # print(f"Wrong password for {filelist}")
            else:
                match=re.search(r"(([\*^\.$]part\d)([\*^\.$]rar))", filelist,
                              re.UNICODE)
                if not match:
                    ex_lists.append(filelist)

        print("正在执行：7z分卷压缩文件的加密判断...")
        for file_parts_list in file_parts_lists:
            match = re.search(r"([\*^\.$]+[z$][0$+][0$+\d])+|([\*^\.$]+[0$+])+|(([\*^\.$]part\d)([\*^\.$]rar))", file_parts_list,
                              re.UNICODE)
            if match:
                try:
                    # command = f'cmd_zip.bat "{filelist}"'
                    command = f'7z t -p "{file_parts_list}"'
                    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                except subprocess.CalledProcessError as err:
                    output = err.output

                output = output.decode('gbk')

                if "ERROR: Wrong password" in output or "Data Error" in output:
                    final_lists.append(file_parts_list)
                    # print(f"Wrong password for {filelist}")
                else:
                    ex_lists.append(file_parts_list)
        print("正在执行：zip分卷压缩文件的加密判断...")
        for file_parts_list in file_parts_lists:
            # match = re.search(r"([\*^\.$]+[z$][0$+][0$+\d])+|([\*^\.$]+[0$+])+|(([\*^\.$]part\d)([\*^\.$]rar))", file_parts_list,
            #                   re.UNICODE)
            # if match:
                try:
                    file_zipparts_lists = tools.register_findone(file_parts_lists, "([\*^\.$]+[z$][0$+][0$+\d])+")
                    list=','.join('"{0}"'.format(x) for x in file_zipparts_lists).replace(','," ")
                    # command = f'cmd_zip.bat "{filelist}"'
                    command = f'7z t -p {list}'
                    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                except subprocess.CalledProcessError as err:
                    output = err.output
                output = output.decode('gbk')
                if "ERROR: Wrong password" in output or "Data Error" in output:
                    final_lists.append(file_parts_list)
                    # print(f"Wrong password for {filelist}")
                else:
                    ex_lists.append(file_parts_list)
        print("正在执行：rar分卷压缩文件的加密判断...")
        file_rarparts_lists=tools.register_find( filelists,"(([\*^\.$]part\d)([\*^\.$]rar))")
        for file_rarparts_list in file_rarparts_lists:
            # match = re.search(r"([\*^\.$]+[z$][0$+][0$+\d])+|([\*^\.$]+[0$+])+|(([\*^\.$]part\d)([\*^\.$]rar))", file_parts_list,
            #                   re.UNICODE)
            # if match:
                try:
                    file_rarparts_lists_group = tools.register_findone(file_rarparts_lists, "(([\*^\.$]part\d)([\*^\.$]rar))")
                    list=','.join('"{0}"'.format(x) for x in file_rarparts_lists_group).replace(','," ")
                    # print(list)
                    # command = f'cmd_zip.bat "{filelist}"'
                    command = f'7z t -p {list}'
                    # print(command)
                    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                except subprocess.CalledProcessError as err:
                    output = err.output
                output = output.decode('gbk')
                # print(output)
                if "ERROR: Wrong password" in output or "Data Error" in output:
                    final_lists.append(file_rarparts_list)
                    # print(f"Wrong password for {filelist}")
                else:
                    ex_lists.append(file_rarparts_list)
        if ex_lists:
            print(
                "--------------------------------------------------无密码----------------------------------------------------")
            for ex_list in ex_lists:
                print(ex_list)
        if final_lists:
            print(
                "--------------------------------------------------有密码----------------------------------------------------")
            for final_list in final_lists:
                print(final_list)
        print(datetime.datetime.now())


def ziptest():
    file = "D:\\Green software\\zip\\test\\TreeSizeFree-Portable.zip"
    zf = zipfile.ZipFile(file)
    for zinfo in zf.infolist():
        is_encrypted = zinfo.flag_bits & 0x1
        if is_encrypted:
            print("true")
            return True
        else:
            print("false")
            return False
