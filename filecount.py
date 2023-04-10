import os
import tools

def getfoldercount():
    count = 0
    print("输入文件列表")
    paths = tools.process_input_list()
    for path in paths:
        for root, dirs, files in os.walk(path):
            count += len(files)
    print(count)









