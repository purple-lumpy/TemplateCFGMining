import TimeGap

# 时间数据预处理，第一个时间为 0 时，后面时间与第一时间的偏移，单位为毫秒

time_sequence_file = open('C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\ProcessedData\\TimeStamp.txt')
time_produce_file = open("C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\ProcessedData\\ProducedTimeLocation.txt", "w+")
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
