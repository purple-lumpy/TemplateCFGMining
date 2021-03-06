# MCTS_Main.py 的更新版，加入了叶子结点信息，作为蒙特卡洛树判优策略之中

import FindCountinTimeWindow
import FindValueForMCTS
import FuncFindLeaf
import FuncReal_CFG as CFG

# --------准备加入叶子结点在蒙特卡洛树搜索算法----------------- 根据CFG图产生的蒙特卡洛树 ------------------------------

# 读取模板流 ，使用蒙特卡洛树进行业务流提取

# 阈值------------------------------------------------------------------------------------------------------------------
# 时间阈值，超过阈值则认为非相邻日志 which in same flow ，单位为秒
threshold1 = 1
# 概率阈值（MCTS 中需要）
threshold2 = 0.5
# 业务叶子结点概率阈值
threshold3 = 0.3
# 蒙特卡洛树搜索的范围单位为秒
threshold4 = 1500

# -- 输入数据与阈值 ----------------------------------------------------------------------------------------------------
# Template file
template_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\Template\\raw_template.txt"
# log sequence file
log_sequence_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\log_clus_index_sequence.txt"
# Time sequence file
time_sequence_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\ProducedTimeStamp.txt"
# 日志时间 + 日志模板编码 序列
Log_Time_TempID_File = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\MergeTimeTid.txt"
# 时间戳序列
raw_time_sequence_path = 'C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\TimeStamp.txt'

# NNS GROUP Generate : Time windows threshold
NNS_groups_Time_Windows_thres = 1  # 单位为秒
# NNS GROUP Generate : frequence threshold
NNS_groups_Frequence_thres = 0.8
# CFG : Time lag for any edges' threshold
CFG_edge_lap_thres = 0.6  # 单位为秒
# CFG : Bayes probability threshold
CFG_bayes_prob_thres = 0.3  # 概率阈值
# ------- 输出到文件 --------------------------------------------------------------------------------------------
# 日志序列对应业务流文件
WorkFlowID_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW_v2\\workflow_results\\WorkflowID.txt"
EachFlow_path = "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW_v2\\workflow_results\\EachFlow.txt"
# 数据结构 -------------------------------------------------------------------------------------------------------
# CFG 网络
(Edgess, Weightss) = CFG.FuncRealCFG(template_path, log_sequence_path, time_sequence_path, Log_Time_TempID_File,
                                     NNS_groups_Time_Windows_thres, NNS_groups_Frequence_thres, CFG_edge_lap_thres,
                                     CFG_bayes_prob_thres)

Leaves = FuncFindLeaf.FuncFindLeaf(Edgess, Weightss, 10)
# 原始模板流
raw_template_sequence = []
# 原始时间流
raw_time_sequence = []

# 原始日志流可用标志流
valid_raw_template = []
# 日志序列对应业务流list
corres_flow_id = []
# 业务流集合
flows_collect = []
# 结束流程的结点（方便程序计算）
End_nodes = []
# --------------------------------------------------------------------------------------------------------

# 测试数据的模板序列 与 时间序列

# 将硬盘数据写入
with open(log_sequence_path) as f1:
    raw_template_sequence = list((int(u.strip()) for u in f1.readlines()))

with open(raw_time_sequence_path) as f2:
    raw_time_sequence = list((u.strip() for u in f2.readlines()))

# 原始日志可用标志 & 日志序列对应业务流 --初始化----------------------------------------------------------------------
for iii in range(len(raw_template_sequence)):
    valid_raw_template.append(1)
    corres_flow_id.append(-1)

# 主要步骤，MCTS 日志划分 -------------------------------------------------------------------

# 当前流程
current_flow = []

for i_th in range(len(raw_template_sequence)):
    if i_th == 0:
        # 访问第一个结点，更新当前业务流
        current_flow.append(raw_template_sequence[i_th])
        # 日志流对应的业务流序列更新
        corres_flow_id[0] = 0
        valid_raw_template[i_th] = 0
        flows_collect.append(current_flow)

    # 已属于某个流程, 或者单独建立一个流程( f_id ) ------------------------------------------------
    if valid_raw_template[i_th] == 0:
        # 属于流程 f_id
        f_id = corres_flow_id[i_th]
        # 该点是叶子结点
        if i_th in End_nodes:
            continue
    else:
        # 新建业务流
        current_flow = [raw_template_sequence[i_th]]
        corres_flow_id[i_th] = len(flows_collect)
        flows_collect.append(current_flow)
        f_id = corres_flow_id[i_th]

    # find subnode
    # Selection ---- 找到阈值 threshold1 内的结点
    window_size = FindCountinTimeWindow.FindCoutWindow(raw_time_sequence[i_th:], threshold1)
    # 不考虑已属于另一个流程中的结点
    valid_nodes = list(i + 1 for i in range(window_size) if valid_raw_template[i_th + 1 + i] == 1)

    if raw_template_sequence[i_th] in Leaves:
        # 叶子结点
        End_nodes.append(i_th)
        if valid_raw_template[i_th] == 1:
            valid_raw_template[i_th] = 0
    elif window_size == 0:
        # 叶子结点
        End_nodes.append(i_th)
        if valid_raw_template[i_th] == 1:
            valid_raw_template[i_th] = 0
    elif not valid_nodes:
        # 叶子结点
        End_nodes.append(i_th)
        if valid_raw_template[i_th] == 1:
            valid_raw_template[i_th] = 0
    else:
        deep = FindCountinTimeWindow.FindCoutWindow(raw_time_sequence[i_th:], threshold4)
        M_value_list = FindValueForMCTS.Value_MCTS_v3(Edgess, Weightss, Leaves,
                                                      raw_template_sequence[i_th: i_th + deep + 1],
                                                      raw_time_sequence[i_th: i_th + deep + 1], window_size,
                                                      valid_nodes, threshold1, threshold2)
        print(M_value_list)
        print("need to break")
        break
        # if max(M_value_list) == 0:
        #     # 叶子结点
        #     End_nodes.append(i_th)
        #     if valid_raw_template[i_th] == 1:
        #         valid_raw_template[i_th] = 0
        # else:
        #     # 非叶子结点
        #     max_val = max(M_value_list)
        #     max_index = M_value_list.index(max_val)
        #     # 子结点
        #     sub_node = raw_template_sequence[i_th + 1 + max_index]
        #     flows_collect[f_id].append(sub_node)
        #     corres_flow_id[ i_th + 1 + max_index ] = f_id
        #     valid_raw_template[ i_th + 1 + max_index ] = 0

# 日志划分结束，写出数据----------------------------------------------------------------------------------------------

WorkFlowID_file = open(WorkFlowID_path, "w+")
WorkFlowID_file.truncate()
for item in corres_flow_id:
    WorkFlowID_file.write(str(item) + "\n")
WorkFlowID_file.close()

EachFlow_file = open(EachFlow_path, "w+")
EachFlow_file.truncate()
for item in flows_collect:
    for index in range(len(item)):
        if index < len(item) - 1:
            EachFlow_file.write(str(item[index]) + ",")
        else:
            EachFlow_file.write(str(item[index]))
    EachFlow_file.write("\n")
EachFlow_file.close()

# ---------- 生成CFG 的 csv 文件
cfg_network = open(
    "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\NEW\\workflow_results\\CFGnetwork.csv",
    "w+")
cfg_network.truncate()
cfg_network.write('Source,Target,Weight\n')
for itemm in zip(Edgess, Weightss):
    a = str(itemm[0][0])
    b = str(itemm[0][1])
    c = round(itemm[1], 3)
    cfg_network.write(a + ',' + b + ',' + str(c) + "\n")
cfg_network.close()
