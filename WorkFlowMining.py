# 通过 CFG 网络，挖掘业务流 --- 长距离依赖关系、解耦和
import FuncReal_CFG as CFG

# -- 输入数据与阈值 ----------------------------------------------------------------------------------------------
# Template file
template_path = "C:\\Users\\ThinkPad\\Desktop\\test\\test\\Train\\template\\raw_template.txt"
# log sequence file
log_sequence_path = "C:\\Users\\ThinkPad\\Desktop\\test\\test\\Train\\log_clus_index_sequence.txt"
# Time sequence file
time_sequence_path = "C:\\Users\\ThinkPad\\Desktop\\test\\test\\Train\\ProducedTimeStamp.txt"
# 日志时间 + 日志模板编码 序列
Log_Time_TempID_File = "C:\\Users\\ThinkPad\\Desktop\\test\\test\\Train\\MergeTimeTid.txt"
# 时间戳序列
raw_time_sequence_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\test\\Train\\TimeStamp.txt'

# NNS GROUP Generate : Time windows threshold
NNS_groups_Time_Windows_thres = 0.80  # 单位为秒
# NNS GROUP Generate : frequence threshold
NNS_groups_Frequence_thres = 0.07
# CFG : Time lag for any edges' threshold
CFG_edge_lap_thres = 0.6  # 单位为秒
# CFG : Bayes probability threshold
CFG_bayes_prob_thres = 0.3  # 概率阈值

# ------- 输出到文件 ----------------------------------------------------------------------------------------------
# 日志序列对应业务流文件
WorkFlowID_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\FirstResult\\WorkflowID.txt"
EachFlow_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\FirstResult\\EachFlow.txt"
# -------- 数据结构 -----------------------------------------------------------------------------------------------
# 分支点集合
MUL = []
# 前驱结点集合
Former = []
# 后驱结点集合
Below = []
# 业务集合
WorkFlow = []
# 起始结点集合
InitNode = []
# 终止结点集合
EndNode = []

# CFG 网络
(Edgess, Weightss) = CFG.FuncRealCFG(template_path, log_sequence_path, time_sequence_path, Log_Time_TempID_File,
                                     NNS_groups_Time_Windows_thres, NNS_groups_Frequence_thres, CFG_edge_lap_thres,
                                     CFG_bayes_prob_thres)
# 原始模板流
raw_template_sequence = []
# 原始时间流
raw_time_sequence = []

# 原始模板序列 与 时间序列数据的录入--------------------------------------------------------------------------------
template_sequence = open(log_sequence_path)
time_sequence = open(raw_time_sequence_path)
# 将硬盘数据写入
while 1:
    temp_lines = template_sequence.readlines(100000)
    if not temp_lines:
        break
    for line_f in temp_lines:
        raw_template_sequence.append(int(line_f.strip()))

while 1:
    time_lines = time_sequence.readlines(100000)
    if not time_lines:
        break
    for line_s in time_lines:
        raw_time_sequence.append(line_s.strip())

template_sequence.close()
time_sequence.close()

# 多分支结点的统计，并保存进 MUL ------------------------------------------------------------------------------------
Raw_temp = list((u for (u, v) in Edgess))
for u in Raw_temp:
    if Raw_temp.count(u) > 1 and (not u in MUL):
        MUL.append(u)
MUL.sort()

# 初始化Formar 与 Below ----------------------------------------------------------------------------------------------------

Former = list(([] for i in range(len(MUL))))
Below = list(([] for i in range(len(MUL))))
# 出度点 与 入度点
Left = []
Right = []
for u, v in Edgess:
    Left.append(u)
    Right.append(v)
for index in range(len(MUL)):
    # MUL 中的结点
    index_node = MUL[index]
    for edge_index in range(len(Left)):
        if index_node == Left[edge_index]:
            Below[index].append(Right[edge_index])
        if index_node == Right[edge_index]:
            Former[index].append(Left[edge_index])

# 长距离依赖关系 ----------------------------------------------------------------------------------------------------
