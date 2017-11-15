import DFSinCFG
import FuncLongRelation as LongRelation
import FuncReal_CFG as CFG

#  生成CFG 网络图结构，挖掘其中的业务流

# 阈值-------------------------------------------------------------------------------------------------
# 时间阈值，超过阈值则认为非相邻日志 which in same flow ，单位为秒
threshold1 = 0.6
# 概率阈值（MCTS 中需要）
threshold2 = 0.5
# 业务叶子结点概率阈值
threshold3 = 0.3
# 长距离依赖因子的阈值
LongRelation_threshold = 0.7

# PreA 到 A 的时间窗，单位为秒
small_time_thres = 1
# PreB - PreA 的time-window
big_time_thres = 20

# 业务起始点与终结点的集合list 的list 【 [开始，结束], ... , [开始，结束]】
Start_End_list = [[1, 10], [1, 12]]
# ------------- 预处理后的输入日志文件们---------------------------------------------------
# Template file
template_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\Template\\raw_template.txt"
# log sequence file
log_sequence_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\log_clus_index_sequence.txt"
# Time sequence file
time_sequence_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\ProducedTimeStamp.txt"
# 日志时间 + 日志模板编码 序列
Log_Time_TempID_File = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\MergeTimeTid.txt"

# --------------- 阈值设定 ----------------------------------------------------------------
# NNS GROUP Generate : Time windows threshold
NNS_groups_Time_Windows_thres = 1  # 单位为秒
# NNS GROUP Generate : frequence threshold
NNS_groups_Frequence_thres = 0.07
# CFG : Time lag for any edges' threshold
CFG_edge_lap_thres = 0.6  # 单位为秒
# CFG : Bayes probability threshold
CFG_bayes_prob_thres = 0.3  # 概率阈值
# ------- 输出 文件 --------------------------------------------------------------------------------------------
# 业务流
Init_Workflow = []
Final_Workflow = []

# 日志序列对应业务流文件
WorkFlowID_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\FirstResult\\WorkflowID.txt"
EachFlow_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\FirstResult\\EachFlow.txt"
# 数据结构 -------------------------------------------------------------------------------------------------------
# CFG 网络
(Edgess, Weightss) = CFG.FuncRealCFG(template_path, log_sequence_path, time_sequence_path, Log_Time_TempID_File,
                                     NNS_groups_Time_Windows_thres, NNS_groups_Frequence_thres, CFG_edge_lap_thres,
                                     CFG_bayes_prob_thres)

# CFG 网络简化
Simple_Network = DFSinCFG.DFS(Edgess)
Simple_Network.Simplify_NetWork()
temp = Simple_Network.FindWorkFlow(Start_End_list)
for va in temp:
    Init_Workflow.append(va)

# ---------- 生成 csv 文件
# cfg_network = open("C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\Simplified.csv","w+")
# cfg_network.truncate()
# cfg_network.write('Source,Target,Weight\n')
# for itemm in new_edge:
#     cfg_network.write(str(itemm[0]) + ',' +str(itemm[1]) + "\n")
# cfg_network.close()
#
# ——————————————————————  真实数据  ———————————————————————————————
# 原始模板流
raw_template_sequence = []
# 原始时间流
raw_time_sequence = []
# 时间窗大小流
time_Win_size = []

Log_file = open(log_sequence_path)
while 1:
    lines = Log_file.readlines(100000)
    if not lines:
        break
    for line in lines:
        raw_template_sequence.append(line.strip())
Log_file.close()

time_gap_file = open(time_sequence_path)
while 1:
    lines = time_gap_file.readlines(100000)
    if not lines:
        break
    for line in lines:
        raw_time_sequence.append(line.strip())
time_gap_file.close()

# 时间窗大小，对每个位置
for index in range(len(raw_time_sequence)):
    size = 0
    sum_of_time = 0
    while sum_of_time <= small_time_thres:
        size += 1
        sum_of_time += raw_time_sequence
        if size + index >= len(raw_time_sequence):
            break
    size -= 1
    time_Win_size[index] = size

# 对每一条业务流，计算它的长距离依赖关系，删除掉一些不具备长距离依赖关系的链
Branch_Node = Simple_Network.Find_Branch_nodes()
Jump_Flag = 0
if not Init_Workflow == []:
    for flow in Init_Workflow:
        branches_index = []
        for nodes_id in range(len(flow) - 1):  # 不考虑最后一个结点
            if flow[nodes_id] in Branch_Node:  # 分支结点
                branches_index.append(nodes_id)

        if branches_index == []:  # 无分支结点
            Final_Workflow.append(flow)
        elif len(branches_index) == 1:
            if branches_index[0] == 0:  # 仅一个分支，且为第一个元素或最后一个元素
                Final_Workflow.append(flow)
            else:  # 仅一个分支，不是第一个元素，不是最后一个元素
                temp_index = branches_index[0]
                reliance = LongRelation.longRelation(flow[0], flow[1], flow[temp_index], flow[temp_index + 1],
                                                     small_time_thres, big_time_thres, raw_template_sequence,
                                                     raw_time_sequence, time_Win_size)
        else:
            gap = len(branches_index) - 1
            while gap >= 1:
                start = 0
                next_right = gap
                while next_right < len(branches_index):
                    start_branch = branches_index[start]
                    next_right_branch = branches_index[next_right]
                    reliance = LongRelation.longRelation(flow[start_branch], flow[start_branch + 1],
                                                         flow[next_right_branch], flow[next_right_branch + 1],
                                                         small_time_thres, big_time_thres, raw_template_sequence,
                                                         raw_time_sequence, time_Win_size)
                    if reliance < LongRelation_threshold:
                        # 长距离依赖因子过低，该flow pass 掉
                        Jump_Flag = 1
                        break
                    start = next_right
                    next_right += gap
                gap = gap // 2
                if Jump_Flag == 1:
                    break
            else:  # while 非break出来的
                Final_Workflow.append(flow)
