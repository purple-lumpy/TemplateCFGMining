import TimeGap

# recode the timestamp，提取时间序列
# 时间数据预处理，第一个时间为 0 时，后面时间为前一时间的偏移，单位为毫秒

# 原始日志序列文件
# file = open("F:\\A_Data_20171024\\SourceData\\time_req__cv.log")
# # 时间戳序列文件
# time_sequence_file=open("F:\\A_Data_20171024\\ProcessedData\\TimeStamp.txt","w+")
# time_sequence_file.truncate()   #delete content
#
# time_sequence=[]
#
# while 1:
#     lines = file.readlines(100000)
#     if not lines:
#         break
#     for line in lines:
#         temp = line.split()
#         time_sequence.append((temp[0],temp[1]))
#         time_sequence_file.write(temp[0] + " " + temp[1] + "\n")
#
# file.close()
# time_sequence_file.close()


# Part2 时间预处理 ----------------------------------------------------------------------------------
time_sequence_file = open("C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\ProcessedData\\TimeStamp.txt")
time_produce_file = open("C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\ProcessedData\\ProducedTimeStamp.txt", "w+")
time_produce_file.truncate()  # 清空文件内容
init_flag = 1
while 1:
    lines = time_sequence_file.readlines(100000)
    if not lines:
        break
    for line in lines:
        if init_flag == 1:
            # 文档第一行
            init_flag += 1
            before = line
            time_produce_file.write("0" + "\n")
        else:
            # 与上一条的时间差
            gen_delta = TimeGap.Time_Gap(before.strip(), line.strip())
            time_produce_file.write(str(gen_delta) + "\n")
            before = line
