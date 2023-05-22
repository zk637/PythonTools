import os
import py7zr
import patoolib
import rarfile
import tools



def check_zip_password():
    print("请输入需要检索的文件夹")
    var = input()
    rar_lists = []
    sevenzip_lists=[]
    # final_lists_rar=[]
    # final_lists_7z=[]
    final_lists=[]
    ex_final_lists=[]
    # final_list=tools.get_zippartfile(var)
    file_paths = tools.get_file_paths_limit(var, ".zip",  ".gz", "xz", ".bz2", ".tar", ".tar.gz",
                                           ".tar.xz",
                                           ".tar.bz2", ".gz", ".bz2", ".lzma", ".cab", ".zipx")
    sevenzip_lists=tools.get_file_paths_limit(var,".7z")
    rar_lists=tools.get_file_paths_limit(var,".rar")
    """检查压缩文件是否有密码"""
    # file_path.strip('"')
    for sevenzip_list in sevenzip_lists:
        try:
            with py7zr.SevenZipFile(sevenzip_list, mode='r') as archive:
                if archive.needs_password():
                    final_lists.append(sevenzip_list)
                    # print(f'{sevenzip_list} 存在密码')
                else:
                    ex_final_lists.append(sevenzip_list)
                    # print(f'{sevenzip_list} 没有密码')
        except py7zr.exceptions.Bad7zFile:
            print(f'{sevenzip_list} 不是有效的7z压缩文件')

    for file_path in file_paths:
        try:
            patoolib.test_archive(file_path ,verbosity=-1)
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
    """遍历结果"""
    print("--------------------------------------------------无密码----------------------------------------------------")
    for ex_final_list in ex_final_lists:
        print(ex_final_list)
    print("--------------------------------------------------有密码----------------------------------------------------")
    for final_list in final_lists:
        print(final_list)



