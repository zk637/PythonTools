# PythonTools
个人工具
=======


主要包含了多级文件夹和视频文件及字幕相关操作，由python编写。当前仅由命令行控制，以下是现有的功能列表
It mainly includes folder multilevel retrieval of video files and video subtitles related operations,make in python currently only controlled by the command line, 
the following is a list of existing functions

    #  1、获取相同子目录下的文件大小            code==01
    #  2、获取不同子目录下的文件大小         code==02
    #  3、使用关键词来查找字幕文件           code==03
    #  4、匹配视频目录下对应的字幕文件并返回列表  code==04
    #  5、通过视频路径查找字幕文件列表（支持模糊匹配）           code==05
    #  6、通过视频路径查找字幕文件并创建目录     code==06
    #  7、通过视频目录查找符合区间条件分辨率的媒体文件          code==07
    #  8、删除文件夹下小于指定MB的文件并输出删除的文件列表   code==08
    #  9、获取文件列表下的文件数量                           code==09
    #  10、获取文件在大小区间下的列表或在修改时间区间下的列表     code==10
    #  11、取文件夹下所有视频文件的时长并排序输出             code==11
    #  12、获取给定文件夹下的 "大小", "时长", "比特率", "分辨率（排序需录入对应的属性）
    #  13、获取给定目录中在检索目录下以相同文件名匹配的列表
    #  14、取传入目录下所有与文件名一致的jpg创建.ts文件夹并移入
    #  15、获取文件夹下所有文件的路径，并返回文件名符合指定规则的文件路径列表 （支持文件名规则匹配 目前只支持 *keyword*匹配）
    #  16、获取两个目录下所有路径，源文件的文件名和目标文件的文件夹名一致则建立符号链接（需管理员权限）
    #  17、为指定的文件列表在指定目录下创建符号链接（需管理员权限）支持文件和文件夹混合
    #  18、判断指定文件夹下的压缩文件是否加密
    #  19、判断指定文件夹下的压缩文件是否加密-精确(支持7z分卷格式）
    #  20、获取符合录入文件名的文件路径
    #  21、获取不在指定后缀的文件路径（输入为路径列表）
    #  22、过滤规则格式化
    #  23、校验文件是否合法
    #  24、文件自动备份（需提前创建符号链接
    #  25、检查录入文件夹下的符号链接是否可用
    
    1. Obtain the file size code==01 in the same subdirectory
    2. Obtain the file size code==02 in different subdirectories
    3, use keywords to find subtitle file code==03
    4, Match the corresponding subtitle file in the video directory and return the list code==04
    5, through the video path to find the subtitle file list (support fuzzy matching) code==05
    6. Find subtitle files through the video path and create directory code==06
    7, through the video directory to find the media file code==07 that meets the resolution of the interval condition
    8, delete files smaller than the specified MB under the folder and output the list of deleted files code==08
    9, get the number of files in the file list code==09
    10, get the list of files under the size interval or the list of files under the modification time interval code==10
    11, Take the duration of all video files in the folder and sort the output code==11
    12, get the "size "," duration ", "bit rate "," resolution "under the given folder (sort needs to enter the corresponding attribute)
    13. Get a list of the names matching the same name in the search directory in the given directory
    14. Take all the jpg files in the incoming directory that are consistent with the file name to create a.ts folder and move them into it
    15, get the path of all files under the folder, and return the file path list of file names that meet the specified rules (support file name rules matching currently only support *keyword* matching)
    16, get all paths in the two directories, the source file name and the target file folder name is the same to establish a symbolic link (administrator permission is required)
    17, for the specified file list in the specified directory to create symbolic links (administrator permissions required) support file and folder mixing
    18, determine whether the compressed file in the specified folder is encrypted
    19, determine whether the compressed file under the specified folder is encrypted - accurate (support 7z volume format)
    20, Get the file path that matches the input file name
    21, get the file path that is not the specified suffix (input as the path list)
    22, filter rule formatting
    23. Check whether the file is legitimate
    24, automatic file backup (need to create symbolic links in advance
    25. Check whether the symbolic links in the folder are available


  
