# Merge File ----- Time and Template id

OutputFile = open("C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\ProcessedData\\MergeTimeTid.txt", "w+")
OutputFile.truncate()  # 清空内容
TimeFile = open("C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\ProcessedData\\TimeStamp.txt")
TemplateFile = open("F:\\A_Data_20171024\\ProcessedData\\log_clus_index_sequence.txt")

while 1:
    time_line = TimeFile.readline().strip()
    template_line = TemplateFile.readline().strip()
    if not time_line:
        break
    context = template_line + "*" + time_line + "\n"
    OutputFile.write(context)
