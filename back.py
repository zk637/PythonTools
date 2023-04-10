    # file_paths = []
    # while True:
    #     path = input("请输入文件路径，每个路径都用双引号括起来并占据一行，输入空行结束：\n")
    #     if not path:
    #         break
    #     file_paths.append(path.strip('"'))
    # # total_size=fileSize.def_get_total_size(file_paths)
    # total_size=fileSize.get_total_file_size(file_paths)
    # print(f'Total size: {round(total_size, 2)} GB')

    # ----------------------------------------------------------

# ------------------------------------------
# 用于存放废弃代码
# def move_files_tosuffix():
#     # 指定目录路径
#     print("请输入需要对比的文件夹")
#     folder_path = tools.process_input_str("请输入需要对比的文件夹")
#
#     # 定义排除的文件后缀列表
#     excluded_extensions = [".png"]
#
#     # 存储所有.ts文件夹下jpg后缀的文件名
#     jpg_files = []
#     non_jpg_files = []
#
#     # 获取所有JPG以外的文件
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             file_extension = os.path.splitext(file_path)[1]
#             if file_extension == '.jpg':
#                 jpg_files.append(file_path)
#             elif file_extension not in excluded_extensions:
#                 non_jpg_files.append(file_path)
#     for non_jpg_file in non_jpg_files:
#         jpg_dir = os.path.dirname(non_jpg_file)
#         # print(jpg_dir)
#         file_name = os.path.splitext(os.path.basename(non_jpg_file))[0]
#         # file_name = os.path.splitext((non_jpg_file)[1])
#         same_name_files = []
#         for jpg_file in jpg_files:
#             jpg_file_base = os.path.splitext(os.path.basename(jpg_file))[0]
#             if jpg_file_base not in excluded_extensions and jpg_file != non_jpg_file and jpg_file_base == file_name:
#                 same_name_files.append(jpg_file)
#         print('same')
#         print(same_name_files)

    # for jpg_file in jpg_files:
    #     if jpg_file not in same_name_files:
    #         os.remove(jpg_file)

# def compare_and_move_files():
#
#     print("请输入需要对比的文件夹")
#     folder_path=tools.process_intput_strr("请输入需要对比的文件夹")
#     exclude_suffix = {'.ts', '.bat', '.dll'}  # 替换为您的排除列表
#     file_paths=tools.get_file_paths_e(folder_path,"111111",exclude_suffix)
#     tools.get_same_name_file_paths(file_paths)
#     for file_path in file_paths:
#         dir_path = os.path.dirname(file_path)
#         t_dir_path = os.path.join(dir_path, ".ts")
#         os.makedirs(t_dir_path, exist_ok=True)
#         try:
#             shutil.move(file_path, t_dir_path)
#         except Exception as e:
#             print("处理发生错误：", file_path)


# def compare_and_move_files():
#     excluded_extensions = ['.dll', '.mp4','.ts']
#     print("请输入需要对比的文件夹")
#     folder_path = tools.process_input_str("请输入需要对比的文件夹")
#     jpg_files = []
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             if os.path.splitext(file_path)[1] == '.jpg':
#                 jpg_files.append(file_path)
#
#     for jpg_file in jpg_files:
#         ts_dir = os.path.join(os.path.dirname(jpg_file), '.ts')
#         if not os.path.exists(ts_dir):
#             os.mkdir(ts_dir)
#
#         file_name = os.path.splitext(os.path.basename(jpg_file))[0]
#         print( os.path.splitext(os.path.basename(file_name))[0])
#         same_name_files = [f for f in jpg_files if (
#             os.path.splitext(os.path.basename(f))[0] == file_name)]
#         print(f"同名文件列表：{same_name_files}")
#         for file in same_name_files:
#             if os.path.splitext(file)[1] not in excluded_extensions:
#                 try:
#                     shutil.move(file, ts_dir)
#                 except Exception as e:
#                     print(f'处理发生错误：{file}')
#                     print(e)


    # for root, dirs, files in os.walk(folder, topdown=False):
    #     for name in files:
    #         path = os.path.join(root, name)
    #         if os.path.getsize(path) < min_size:  # 小于30MB
    #             os.remove(path)
    #     for name in dirs:
    #         path = os.path.join(root, name)
    #         if not os.listdir(path):  # 空文件夹
    #             os.rmdir(path)
    # to_remove = set()
    # for root, dirs, files in os.walk(folder, topdown=False):
    #     for file in files:
    #         path = os.path.join(root, file)
    #         if os.path.getsize(path) < min_size:
    #             to_remove.add(os.path.dirname(path))
    # for folder in to_remove:
    #     os.rmdir(folder)
    # return tools.get_file_paths(folder)


