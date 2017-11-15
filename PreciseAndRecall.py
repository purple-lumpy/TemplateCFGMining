# 计算精确度和召回率
# 0 为异常，1 为正常

test_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW\\workflow_results\\4\\TOrFinLog.txt'
baseline_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\TorFseq.txt'

Test_data = []
Baseline_data = []
TF_test = open(test_path)
while 1:
    lines = TF_test.readlines(100000)
    if not lines:
        break
    for line in lines:
        Test_data.append(int(line.strip()))
TF_test.close()

TF_Baseline = open(baseline_path)
while 1:
    lines = TF_Baseline.readlines(100000)
    if not lines:
        break
    for line in lines:
        Baseline_data.append(int(line.strip()))
TF_Baseline.close()

# 计算Precise 与 Recall
# TP 为 test 与 baseline 中，都是异常的个数，即异常判断正确的次数
TP = 0
for i in range(len(Baseline_data)):
    if Baseline_data[i] + Test_data[i] == 0:
        TP += 1
# TP_FP 为 baseline 中，异常的个数
TP_FP = Baseline_data.count(0)
# TP_FN 为 test 中，异常的个数
TP_FN = Test_data.count(0)

Precise = TP / TP_FP
Recall = TP / TP_FN

print('Precise  is : ', Precise)
print('Recall   is : ', Recall)

# 计算Accuracy
# TP_TN 为 TP + TN 的值
TP_TN = 0
for i in range(len(Baseline_data)):
    if Baseline_data[i] + Test_data[i] == 0 or Baseline_data[i] + Test_data[i] == 2:
        TP_TN += 1
Accuracy = TP_TN / (len(Baseline_data))

print('Accuracy is : ', Accuracy)
