# KMeans---： 2-means,异常判定基于假设：正常类包含样本更多，异常类包含样本更少
from sklearn.cluster import KMeans

import KMeans_feature as Feature

# 模板个数 Template_num ----- 即特征的维数
template_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\Template\\raw_template.txt'
template_file = open(template_path)
Template_num = len(template_file.readlines())  # 特征维数
template_file.close()

# 特征们
Features_matrix = []

# 质心
Center_point = []

# 每个特征据质心的距离
Distance = []

# workflow 原始数据 ---> 特征
WorkFlow_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW\\workflow_results\\4\\EachFlow.txt'
WorkFlow_file = open(WorkFlow_path)
while 1:
    lines = WorkFlow_file.readlines(100000)
    if not lines:
        break
    for line in lines:
        flow = line.strip().split(',')
        f_temp = Feature.Get_Integrity_Feature(Template_num, flow)
        Features_matrix.append(f_temp)
WorkFlow_file.close()

# 调用kmeans类
clf = KMeans(n_clusters=2)
s = clf.fit(Features_matrix)
print(s)

# 2个中心
print(clf.cluster_centers_)

KMeans_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW\\workflow_results\\4\\TOrF.txt'
KMeans_file = open(KMeans_path, "w+")
KMeans_file.truncate()
# 每个样本所属的簇 clf.labels_
# 正常类 label 等于 1, 异常类 label 等于 0
labels = list(clf.labels_)
one = labels.count(1)
zero = labels.count(0)
if one < zero:
    for i in range(len(labels)):
        labels[i] = abs(labels[i] - 1)
for line in labels:
    KMeans_file.write(str(line) + '\n')
KMeans_file.close()
# 每个样本所属的簇
# print(clf.labels_)
#
# # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
# print(clf.inertia_)
#
# # 进行预测
# print( clf.predict(Features_matrix) )
#
# # 保存模型
# joblib.dump(clf, 'c:/km.pkl')
#
# # 载入保存的模型
# clf = joblib.load('c:/km.pkl')

'''
#用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
for i in range(5,30,1):
    clf = KMeans(n_clusters=i)
    s = clf.fit(feature)
    print i , clf.inertia_'''
