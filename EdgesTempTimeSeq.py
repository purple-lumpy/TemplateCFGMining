# 为每个NNS group 找到在（模板-时间戳）序列中的位置
# 输入： 模板 + NNS group memners + 序列文件
# 输出： 相关模板序列 + 对应时间序列


def Temp_Time_get(nns, filepath):
    # 记录 相关模板 与 对应时间 序列
    Template_seq = []
    Time_Gap_seq = []

    # 生成 模板序列 & 时间序列
    Temp_Time_file = open(filepath)
    while 1:
        lines = Temp_Time_file.readlines(100000)
        if not lines:
            break
        for line in lines:
            line_content = line.strip().split("*")
            if int(line_content[0].strip()) in nns:
                Template_seq.append(int(line_content[0].strip()))
                Time_Gap_seq.append(line_content[1].strip())

    # 结束 - 关闭文件 - 输出
    Temp_Time_file.close()
    return Template_seq, Time_Gap_seq
