from sklearn import metrics as mr

x1 = []
y1 = []
y2 = []

fr1 = open("C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\Workflow\\Merged\\WorkflowID.txt")
for line in fr1.readlines():
    y1.append(int(line))
fr1.close()

# fr3=open("C:\\Users\\ThinkPad\\Desktop\\test\\RandomData\\Random4.txt")
# for line in fr3.readlines():
#     y2.append(int(line))
# fr3.close()

fr2 = open('C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\flowId.txt')
for line in fr2.readlines():
    x1.append(int(line))
fr2.close()

print("1 与 44 的互信息为 %f" % mr.normalized_mutual_info_score(x1, y1))
# print("1 与 1052 的互信息为 %f" % mr.normalized_mutual_info_score(x1, y2))
