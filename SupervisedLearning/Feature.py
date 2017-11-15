# 特征，完整性特征

# 日志模板的总个数，即特征的维数
def Get_Integrity_Feature(counts, line):
    line_data = line
    feature = list((0 for i in range(counts)))
    for va in line_data:
        int_va = int(va)
        feature[int_va] += 1
    return feature
