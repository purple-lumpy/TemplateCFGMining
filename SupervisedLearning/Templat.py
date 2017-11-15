import Levenshtein

# 对原始日式进行模板匹配，返回日志序列对应的模板序列 id , 保存在 regular_id 的结构中
# 写入到 results.txt 文件中，未匹配到的日志，对应 id 为 -1

# 要进行匹配的原始日志
raw_file = open("C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\Regulared.txt")

# 模板集合
with open("C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\raw_template.txt") as f:
    template_all = list((u.strip() for u in f.readlines()))

# 模板id 序列
regular_list = []

while 1:
    lines = raw_file.readlines(100000)
    if not lines:
        break
    for line in lines:
        # 每一条原始日志，重新访问一次模板库
        for index in range(len(template_all)):
            # 计算与模板的编辑距离
            template = template_all[index]
            dis = Levenshtein.distance(line.strip(), template)
            if (dis / len(line.strip())) <= 0.1:  # 与初略模板距离比较接近
                regular_list.append(index)
                break
            else:
                continue
        else:
            regular_list.append(-1)

# 原始日志序列对应的模板号序列---------------------------
filtered_file = open("C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\log_sequence.txt", 'w+')
filtered_file.truncate()
for item in regular_list:
    filtered_file.write(str(item) + "\n")
filtered_file.close()

raw_file.close()
