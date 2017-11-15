import Levenshtein

# 模板挖掘

# 原始日志正则匹配后的序列文件
filtered_file = open("F:\\Anomoly_workflow_templates\\PreProcessedData\\Regulared.txt")
# 模板的list集合
clusters_list = []
# 日志序列对应cluster_list的下标
log_clus_index_sequence = []
init_flag = 1

while 1:
    lines = filtered_file.readlines(100000)
    if not lines:
        break
    for line in lines:
        if init_flag == 1:
            # 文档第一行
            init_flag += 1
            clusters_list.append(line)
            log_clus_index_sequence.append(0)
        else:
            f_index = 0
            for items in clusters_list:
                dis = Levenshtein.distance(line, items)
                if (dis / len(items)) <= 0.05:  # 与初略模板距离比较接近
                    f_index = clusters_list.index(items)
                    log_clus_index_sequence.append(f_index)
                    break
            else:  # 一个新模板诞生
                clusters_list.append(line)
                f_index = len(clusters_list) - 1
                log_clus_index_sequence.append(f_index)

filtered_file.close()

# 原始日志序列对应的模板号序列---------------------------
log_id_seq_file = open("F:\\Anomoly_workflow_templates\\PreProcessedData\\log_clus_index_sequence.txt", "w+")
log_id_seq_file.truncate()
for item in log_clus_index_sequence:
    log_id_seq_file.write(str(item) + "\n")
log_id_seq_file.close()

# 原始日志模板集合------------------------------------------
raw_template_file = open("F:\\Anomoly_workflow_templates\\PreProcessedData\\raw_template.txt", "w+")
raw_template_file.truncate()
for line in clusters_list:
    raw_template_file.write(line)
raw_template_file.close()
