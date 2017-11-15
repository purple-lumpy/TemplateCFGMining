# 处理数据， 将业务流的异常正常，关联到日志流上

TFinFlow_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW\\workflow_results\\4\\TOrFinFlow.txt'
flow_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW\\workflow_results\\4\\WorkflowID.txt'
log_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW\\workflow_results\\4\\TOrFinLog.txt'

TF = []
TF_File = open(TFinFlow_path)
while 1:
    lines = TF_File.readlines(100000)
    if not lines:
        break
    for line in lines:
        TF.append(int(line.strip()))
TF_File.close()

TF_Log = []
LoginFlow_File = open(flow_path)
while 1:
    lines = LoginFlow_File.readlines(100000)
    if not lines:
        break
    for line in lines:
        row = int(line.strip())
        TF_Log.append(TF[row])

# 将TF_Log 写入到 log_path 中
Log_file = open(log_path, "w+")
Log_file.truncate()
for item in TF_Log:
    Log_file.write(str(item) + "\n")
Log_file.close()


# baseline 部分数据处理
# TFinFlow_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\workflow_TF_for_table2.csv'
# flow_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\flowId.txt'
# log_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\TorFseq.txt'
#
# # 第一行
# init_flag=1
#
# TF = []
# TF_File = open(TFinFlow_path)
# while 1:
#     lines = TF_File.readlines(100000)
#     if not lines:
#         break
#     for line in lines:
#         if init_flag == 1:
#             # 文档第一行
#             init_flag += 1
#             continue
#         TF.append(int( line.strip().split(',')[2] ))
# TF_File.close()
#
# TF_Log = []
# LoginFlow_File = open(flow_path)
# while 1:
#     lines = LoginFlow_File.readlines(100000)
#     if not lines:
#         break
#     for line in lines:
#         row = int(line.strip())
#         TF_Log.append(TF[row])
#
# # 将TF_Log 写入到 log_path 中
# Log_file = open( log_path,"w+" )
# Log_file.truncate()
# for item in TF_Log:
#     Log_file.write(str(item) + "\n")
# Log_file.close()
