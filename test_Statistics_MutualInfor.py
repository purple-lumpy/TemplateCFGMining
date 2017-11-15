# 统计随机序列对比 baseline 的互信息，随机1000次，均值 & 方差
import random

import numpy as np
from sklearn import metrics as mr

# baseline
x1 = []
# fr2 = open('C:\\Users\\ThinkPad\\Desktop\\test\\baseline\\CreateVM\\flowId.txt')
fr2 = open(
    'C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW\\workflow_results\\3\\WorkflowID.txt')
for line in fr2.readlines():
    x1.append(int(line))
fr2.close()

mutualInfo = []
times = 1000

# 随机生成业务流编号
up_bound = 44
flow_len = 5264

for i in range(times):
    flow_id = []
    for i in range(flow_len):
        va = random.randint(0, up_bound)
        flow_id.append(va)
    mu = mr.normalized_mutual_info_score(x1, flow_id)
    mutualInfo.append(mu)

NP_mutualInfo = np.array(mutualInfo)
means_value = np.mean(NP_mutualInfo)
var_value = np.var(NP_mutualInfo)

print('Mean is :', means_value)
print('Var  is :', var_value)
