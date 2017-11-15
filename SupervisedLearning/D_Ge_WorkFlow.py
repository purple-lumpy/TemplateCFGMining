# 按照 req ID 提取业务流
# 按照业务流的 req ID 标label

Log_seq_file_path = 'F:\\Anomoly_workflow_templates\\PreProcessedData\\log_clus_index_sequence.txt'
ReqID_path = 'F:\\Anomoly_workflow_templates\\PreProcessedData\\ReqId.txt'
TF_file = open('C:\\Users\\ThinkPad\\t800\\req_instance_TF.csv')

WorkFlow = []
ReqID = []
TF = []

# 去重复的 ReqID
with open(ReqID_path) as f:
    ReqID_temp = list((u.strip() for u in f.readlines()))
ReqID = list(set(ReqID_temp))

with open(Log_seq_file_path) as f:
    Log_seq_temp = list((int(u.strip()) for u in f.readlines()))

# 初始化WorkFlow
WorkFlow = list(([] for i in range(len(ReqID))))

# 生成workflow
for i in range(len(Log_seq_temp)):
    WF_index = ReqID.index(ReqID_temp[i])
    WorkFlow[WF_index].append(Log_seq_temp[i])

# 将 正/异常 信息 生成一个字典
Items = []
while 1:
    lines = TF_file.readlines(100000)
    if not lines:
        break
    for line in lines:
        content = line.strip().split(',')
        item = (eval(content[1]), int(eval(content[3])))
        Items.append(item)
TF_file.close()

TF_Dict = dict(Items)

for wf in ReqID:
    tf = TF_Dict[wf]
    TF.append(tf)

# workflow 信息写入
result_file = 'F:\\Anomoly_workflow_templates\\PreProcessedData\\WorkFlow\\eachflow.txt'
EachFlow_file = open(result_file, "w+")
EachFlow_file.truncate()
for item in WorkFlow:
    for index in range(len(item)):
        if index < len(item) - 1:
            EachFlow_file.write(str(item[index]) + ",")
        else:
            EachFlow_file.write(str(item[index]))
    EachFlow_file.write("\n")
EachFlow_file.close()

# ReqID 信息写入
raw_template_file = open("F:\\Anomoly_workflow_templates\\PreProcessedData\\WorkFlow\\ReqID.txt", "w+")
raw_template_file.truncate()
for line in ReqID:
    raw_template_file.write(line + '\n')
raw_template_file.close()

# TF 信息写入
raw_template_file = open("F:\\Anomoly_workflow_templates\\PreProcessedData\\WorkFlow\\TF.txt", "w+")
raw_template_file.truncate()
for line in TF:
    raw_template_file.write(str(line) + '\n')
raw_template_file.close()
