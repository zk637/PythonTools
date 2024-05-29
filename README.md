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
    #  13、获取给定文件夹下在检索路径列表中以相同文件名匹配的列表或获取不匹配相同文件名的列表
    #  14、取传入目录下所有与文件名一致的jpg创建.ts文件夹并移入
    #  15、获取文件夹下所有文件的路径，并返回文件名符合指定规则的文件路径列表 （支持文件名模糊规则匹配）
    #  16、获取两个目录下所有路径，源文件的文件名和目标文件的文件夹名一致则建立符号链接（需管理员权限）
    #  17、为指定的文件列表在指定目录下创建符号链接（需管理员权限）支持文件和文件夹混合
    #  18、判断指定文件夹下的压缩文件是否加密
    #  19、判断指定文件夹下的压缩文件是否加密-精确(支持7z分卷格式）
    #  20、获取检索文件夹下和检索文件名相同的路径列表
    #  21、获取不在指定后缀的文件路径（输入为路径列表或文件夹）
    #  22、过滤规则格式化
    #  23、校验文件是否合法
    #  24、检查录入文件夹下的符号链接是否可用
    #  25、文件自动备份（更新-需提前创建符号链接）
    #  26、文件自动备份（创建-需提前创建符号链接）
    #  27、文件夹内容与csv对比
    #  28、获取给定文件夹或文件的音频文件
    #  29、文件夹下视频命名规范化
    #  30、根据限制大小拆分视频为多段
    #  31、为视频文件添加字幕
    #  32、检查视频是否存在字幕流
    #  33、获取指定文件夹下的目录结构并复制
    #  34、获取指定文件列表或文件夹下的视频是否完整
    #  35、获取指定文件类型的文件数量和路径
    #  36、获取指定文件类型外文件的数量和路径
    #  37、获取录入文件列表中子文件大于3GB且存在3个以上文件的文件夹并输出不符合条件的文件夹
    
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
    # 13, get a given folder in the search path list with the same file name matching list or get a list that does not match the same file name
    # 14. Take all the jpg files in the incoming directory that are consistent with the file name to create a.ts folder and move them into it
    # 15, get the path of all files in the folder, and return the file path list of file names that meet the specified rules (support filename fuzzy rule matching)
    # 16, get all paths in the two directories, the source file name and the target file folder name is the same to establish a symbolic link (administrator permission is required)
    # 17, for the specified file list in the specified directory to create symbolic links (administrator permissions required) support file and folder mixing
    # 18, determine whether the compressed file in the specified folder is encrypted
    # 19, determine whether the compressed file under the specified folder is encrypted - accurate (support 7z volume format)
    # 20, get the search folder and search file name the same path list
    # 21, get the file path without the specified suffix (enter as a path list or folder)
    # 22, filter rule formatting
    # 23. Check whether the file is legitimate
    # 24, check whether the symbolic links in the folder are available
    # 25, automatic file backup (update - need to create a symbolic link in advance)
    # 26, automatic file backup (create - need to create a symbolic link in advance)
    # 27. Compare folder contents with csv
    # 28. Get the audio file for the given folder or file
    # 29, folder video naming normalization
    # 30. Split the video into multiple segments according to the limit size
    # 31. Add subtitles to the video file
    # 32. Check whether the video has a subtitle stream
    # 33. Get the directory structure in the specified folder and copy it
    # 34, get the video under the specified file list or folder is complete
    # 35. Gets the number and path of files for the specified file type
    # 36. Get the number and path of files outside the specified file type
    # 37. Get the folders whose sub-files are larger than 3GB and have more than 3 files in the input file list and output the folders that do not meet the conditions
  
