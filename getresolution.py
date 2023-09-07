import os
from PIL import Image
import cv2
import tools

def get_low_resolution_media_files():
    print("-----------------------请输入第一个分辨率阈值（格式为 宽*高）：--------------------------")
    size_limit1 = input("")
    width_limit1, height_limit1 = map(int, size_limit1.split("*"))

    print("-----------------------请输入第二个分辨率阈值（格式为 宽*高）:--------------------------")
    size_limit2 = input("")
    width_limit2, height_limit2 = map(int, size_limit2.split("*"))

    if width_limit1 > width_limit2:
        width_limit1, width_limit2 = width_limit2, width_limit1
    if height_limit1 > height_limit2:
        height_limit1, height_limit2 = height_limit2, height_limit1

    print(f"分辨率区间阈值：{width_limit1}*{height_limit1}~{width_limit2}*{height_limit2}")

    print("请输入视频文件夹：")
    path = tools.process_input_str("")
    print("比特率排序Y/N")
    flag = input()
    files = []
    for file_path in tools.get_file_paths(path):
        _, ext = os.path.splitext(file_path)
        if ext.lower() in ('.mp4', '.avi', '.mkv', '.jpg', '.jpeg', '.png', '.gif'):
            try:
                if ext.lower() in ('.mp4', '.avi', '.mkv'):
                    cap = cv2.VideoCapture(file_path)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cap.release()
                    if width * height >= width_limit1 * height_limit1 and width * height <= width_limit2 * height_limit2:
                        files.append(file_path)
                elif ext.lower() in ('.jpg', '.jpeg', '.png', '.gif'):
                    width, height = Image.open(file_path).size
                    if width >= width_limit1 and height >= height_limit1 and width <= width_limit2 and height <= height_limit2:
                        files.append(file_path)
            except Exception as e:
                print(f"Error occurred while processing file {file_path}: {str(e)}")
    if ('Y' == flag.upper()):
        try:
            files = tools.getbitratesort(files)
            files=tools.add_quotes_forpath(files)
            print("分辨率符合要求的媒体文件列表（按比特率由大到小排序）：")
            print("\n".join(files))
        except Exception as e:
            print(f"Error occurred while sorting files by bitrate: {str(e)}")
    else:
        print("分辨率符合要求的媒体文件列表：")
        files = tools.add_quotes_forpath(files)
        print("\n".join(files))