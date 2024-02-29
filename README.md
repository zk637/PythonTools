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
    #  10、获取文件在大小区间下的列表或在修改时间区间下的列表       code==10
    #  11、取文件夹下所有视频文件的时长并排序输出或输出时长大小相同的文件            code==11
    #  12、获取给定文件夹下的 "大小", "时长", "比特率", "分辨率（排序需录入对应的属性）
    #  13、获取给定目录中在检索目录下以相同文件名匹配的列表或获取不匹配条件的列表
    #  14、取传入目录下所有与文件名一致的jpg创建.ts文件夹并移入
    #  15、获取文件夹下所有文件的路径，并返回文件名符合指定规则的文件路径列表 （支持文件名规则匹配 目前只支持 *keyword*匹配）
    #  16、获取两个目录下所有路径，源文件的文件名和目标文件的文件夹名一致则建立符号链接（需管理员权限）
    #  17、为指定的文件列表在指定目录下创建符号链接（需管理员权限）支持文件和文件夹混合
    #  18、判断指定文件夹下的压缩文件是否加密
    #  19、判断指定文件夹下的压缩文件是否加密-精确(支持7z分卷格式）
    #  20、获取符合录入文件名的文件路径
    #  21、获取不在指定后缀的文件路径（输入为路径列表或文件夹）
    #  22、过滤规则格式化
    #  23、校验文件是否合法
    #  24、检查录入文件夹下的符号链接是否可用
    #  25、文件自动备份（更新-需提前创建符号链接）
    #  26、文件自动备份（创建-需提前创建符号链接）
    #  27、文件夹内容与csv对比
    #  28、获取给定文件夹或文件的音频文件
    
    # 1. Get the size of files in the same subdirectory code==01
    # 2. Get the size of files in different subdirectories code==02
    # 3. Use keywords to find subtitle files code==03
    # 4. Match the corresponding subtitle file in the video directory and return the list code==04
    # 5. Find subtitle file list by video path (support fuzzy matching) code==05
    # 6. Find subtitle files by video path and create directory code==06
    # 7. Find the media files that meet the interval condition resolution by video catalog code==07
    # 8. Delete files smaller than the specified MB in a folder and output a list of deleted files. code==08
    # 9. Get the number of files in the file list code==09
    # 10, get the list of files in the size range or in the modification time range code==10
    # 11, take the length of all the video files in the folder and sort the output or output the files with the same length and size. code==11
    # 12. Get the "size", "duration", "bitrate", "resolution" (sorting requires entry of the corresponding attributes) for a given folder
    # 13, Get a list of matches in a given directory with the same filename in the retrieved directory or get a list of mismatched conditions
    # 14, take all the jpg's in the incoming directory with the same filename to create a .ts folder and move it into the
    # 15, get the paths of all files in the folder, and return a list of file paths whose filenames match the specified rules (supports filename rule matching Currently only supports *keyword* matching)
    # 16, get all the paths in two directories, the source file's file name and the target file's folder name are the same, then establish a symbolic link (requires administrator privileges)
    # 17, for a specified list of files in a specified directory to create symbolic links (requires administrator privileges) support for file and folder mixing
    # 18, to determine whether the compressed file in the specified folder is encrypted or not
    # 19, to determine whether the zip file under the specified folder is encrypted-exact (support 7z split-volume format)
    # 20. Get the path to the file that matches the name of the entry file.
    # 21. Get the path to a file that is not in the specified suffix (enter as path list or folder)
    # 22, Filter rule formatting
    # 23. Checking documents for legality
    # 24. Check the availability of symbolic links under the entry folder
    # 25, Automatic backup of documents (update - need to create symbolic links in advance)
    # 26, Automatic backup of documents (creation - need to create symbolic links in advance)
    # 27, folder contents vs. csv
    # 28. Get the audio file for a given folder or file


  
