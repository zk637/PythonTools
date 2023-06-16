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
    #  20、获取符合录入文件名的文件路径
    #  21、获取不在指定后缀的文件路径（输入为路径列表）
    
    1. Obtain the file size code==01 in the same subdirectory
    2. Obtain the file size code==02 in different subdirectories
    3. Use keywords to find subtitle file code==03
    4. Match the subtitle file in the video directory and return the list code==04
    5. Search the subtitle file code==05 through the video path
    6. Find the subtitle file through the video path and create the directory code==06
    7. Search the media file code==07 in accordance with the resolution of the interval condition through the video directory
    8. Delete files smaller than the specified MB in the folder and output the list of deleted files code==08
    9. Get the number of files under file list code==09
    10.Get the list of files in the size range code==10
    11. Take the duration of all video files in the folder and sort the output code==11
    12. Get the "size "," duration ", "bitrate "," resolution "under the given folder [sort needs to change the value of x [2]]
    13. Get the files in the given directory that match the list under the search directory
    14. Take all the jpg files from the passed directory that match the file name and move them to the.ts folder
    15. Gets the paths to all files in a folder and returns a list of file paths whose file names match the specified rules. Currently, only *keyword* matches are supported
    16. Obtain all paths in the two directories. If the file name of the source file is the same as the folder name of the target file, create a symbolic link (administrator permission is required).
    17. Create symbolic links in the specified directory for the specified file list (administrator permission required). Support file and folder mixing ""
    18. Check whether the compressed files in the specified folder are encrypted
    19. determine whether the compressed file under the specified folder is encrypted - accurate (support 7z volume format)
    20. Get the file path that matches the input file name
    21. get the file path that is not the specified suffix (input as the path list)
   

  
