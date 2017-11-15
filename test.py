# 倒序读文件
# with open("C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\TimeStamp.txt") as f:
#     a = reversed(f.readlines())
# # for line in a:
# #     print(line.strip())
# b = list(a)
# for i in range( len( b )):
#     print(b[i].strip())

# 随机生成业务流编号
# import random
#
# up_bound = 1145
# flow_len  = 5264
#
# flow_id = []
# for i in range(flow_len):
#     va = random.randint(0,up_bound)
#     flow_id.append(va)
#
# # 随机数保存进文件------------------------------------------------------------------------------------------------------
# random_file = open("C:\\Users\\ThinkPad\\Desktop\\test\\RandomData\\Random4.txt","w+")
# random_file.truncate()
# for line in flow_id:
#     random_file.write( str(line) + '\n' )
# random_file.close()

# import re
#
# str = "hello world! d"
# print(re.findall(r"he(.+?) ",str)[0])

# 画图
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

plt.title('标准互信息与业务间时间间隔关系图', color='red')
plt.ylabel('标准互信息')
plt.xlabel('增加时间间隔（秒）')
x = [0, 1, 3, 5, 10, 30, 60, 180, 300, 600]
y = [0.962, 0.962, 0.962, 0.962, 0.962, 0.963, 0.978, 0.990, 0.994, 0.997]
# x1 = np.arange(0,600,0.2)
# y1 = list(0.997 for i in range(len(x1)))
# x2 = np.arange(0,60,0.2)
# y2 = list(0.978 for i in range(len(x2)))
plt.axis([0, 630, 0.960, 1])
plt.plot(x, y, 'g^')
# plt.plot(x1,y1,'--',color='#CDC8B1')
# plt.plot(x2,y2,'--',color='#CDC8B1')
plt.show()
