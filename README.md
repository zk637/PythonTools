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
    #  18、判断指定文件夹下的压缩文件是否加密（不支持7z分卷）
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
    #  38、拆分音频为两段（支持文件列表和文件夹）
    #  39、获取文件夹列表中文件夹不存在指定后缀的文件
    
    # 1. Get the file size in the same subdirectory code==01
	# 2. Get the file sizes in different subdirectories code==02
	# 3. Use keywords to find subtitle files code==03
	# 4. Match the corresponding subtitle files in the video directory and return the list code==04
	# 5. Search the subtitle file list through the video path (supports fuzzy matching) code==05
	# 6. Find the subtitle file through the video path and create a directory code==06
	# 7. Find media files that meet the interval condition resolution through the video directory code==07
	# 8. Delete files smaller than the specified MB in the folder and output the deleted file list code==08
	# 9. Get the number of files under the file list code==09
	# 10. Get the list of files in the size range or the list in the modification time range code==10
	# 11. Get the duration of all video files in the folder and sort them for output or output files with the same duration and size code==11
	# 12. Get the "size", "duration", "bitrate", and "resolution" under the given folder (the corresponding attributes need to be entered for sorting)
	# 13. Get a list of files matching the same file name in the search path list under a given folder or get a list of files that do not match the same file name.
	# 14. Get all the jpg files with the same file name in the incoming directory, create a .ts folder and move them in
	# 15. Get the paths of all files in the folder and return a list of file paths whose file names comply with the specified rules (supports file name fuzzy rule matching)
	# 16. Obtain all paths in the two directories. If the file name of the source file is consistent with the folder name of the target file, a symbolic link will be established (administrator rights are required)
	# 17. Create a symbolic link in the specified directory for the specified file list (administrator permissions required). Supports mixing files and folders.
	# 18. Determine whether the compressed files in the specified folder are encrypted (7z volumes are not supported)
	# 19. Determine whether the compressed files in the specified folder are encrypted - accurate (supports 7z volume format)
	# 20. Get a list of paths in the search folder that have the same name as the search file.
	# 21. Get the file path that is not in the specified suffix (input as a path list or folder)
	# 22. Format filtering rules
	# 23. Verify whether the file is legal
	# 24. Check whether the symbolic link under the input folder is available
	# 25. Automatic file backup (update - symbolic links need to be created in advance)
	# 26. Automatic file backup (create - symbolic link needs to be created in advance)
	# 27. Comparison of folder content and csv
	# 28. Get the audio file of a given folder or file
	# 29. Standardize the naming of videos under folders
	# 30. Split the video into multiple segments according to the size limit
	# 31. Add subtitles to video files
	# 32. Check whether there is a subtitle stream in the video
	# 33. Get the directory structure under the specified folder and copy it
	# 34. Get the completeness of the video in the specified file list or folder
	# 35. Get the number and path of files of the specified file type
	# 36. Get the number and path of files outside the specified file type
	# 37. Get the folders whose sub-files are larger than 3GB and contain more than 3 files in the input file list and output the folders that do not meet the conditions.
	# 38. Split the audio into two segments (supports file list and folder)
	# 39. Get files with the specified suffix that do not exist in the folder list.


  
