# 数据预处理， 将 flow 抽取出来

log_file = 'C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\log_sequence.txt'
flow_file = 'C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\flowId.txt'
label_file = 'C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\TFFlow.txt'

with open(log_file) as f:
    template_seq = list((int(u.strip()) for u in f.readlines()))
with open(flow_file) as f:
    flow_seq = list((int(u.strip()) for u in f.readlines()))
with open(label_file) as f:
    label_seq = list((int(u.strip()) for u in f.readlines()))

EachFlow = []
flag = -1
for i in range(len(template_seq)):
    flow_index = flow_seq[i]
    if flow_index > flag:
        flag = flow_index
        EachFlow.append([])
    EachFlow[flow_index].append(template_seq[i])

result_file = 'C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\eachflow.txt'
EachFlow_file = open(result_file, "w+")
EachFlow_file.truncate()
for item in EachFlow:
    for index in range(len(item)):
        if index < len(item) - 1:
            EachFlow_file.write(str(item[index]) + ",")
        else:
            EachFlow_file.write(str(item[index]))
    EachFlow_file.write("\n")
EachFlow_file.close()
