import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import FuncEdges
import FuncNNS

# 画 CFG 图

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
NNS_groups_Frequence_thres = 0.8
# CFG: time lag for any edges' threshold
CFG_edge_lap_thres = 0.3  # 单位为秒
# CFG : Bayes probability threshold
CFG_bayes_prob_thres = 0.1  # 概率阈值

# -------------------------------------------------------------------------------------------


# NNS group 成员，数据组成方式：一个list , 包含若干个list
NNS_groups = FuncNNS.NNS_generate_v3(template_path, log_sequence_path, time_sequence_path,
                                     NNS_groups_Time_Windows_thres, NNS_groups_Frequence_thres)

# NNS group 结构，数据组成方式：一个list , 包含若干个numpy 的 ndarrary
small_edges_groups = FuncEdges.funcEdges(NNS_groups, Log_Time_TempID_File, CFG_edge_lap_thres, CFG_bayes_prob_thres)

# 生成多重边有向图
CFG = nx.MultiDiGraph()
# 添加结点（模板）
node_len = len(small_edges_groups)
CFG.add_nodes_from(list(range(node_len)))

# 添加边
CFG_edges = []
CFG_weight = []
for countss in range(len(NNS_groups)):
    G_menbers = NNS_groups[countss]
    if not G_menbers:
        continue
    else:
        if not countss in G_menbers:
            G_menbers.append(countss)

        # 排序
        G_menbers.sort()

        # 取出该模板的NNS group 结构
        Condition_transfer = small_edges_groups[countss]

        # 找到非零元
        Non_zeros = np.argwhere(Condition_transfer)

        # 添加非零元到 CFG_edges 中
        for nz_id in range(len(Non_zeros)):
            # 矩阵中的 行 与 列 与 概率值
            row = Non_zeros[nz_id][0]
            column = Non_zeros[nz_id][1]
            valueee = round(Condition_transfer[row][column], 3)

            # 对应的模板 id 号码
            row_template = G_menbers[row]
            column_template = G_menbers[column]

            # 边 与 权重
            temp_edge = (row_template, column_template)
            temp_weight = {'weight': valueee}

            if not temp_edge in CFG_edges:
                CFG_edges.append(temp_edge)
                CFG_weight.append(temp_weight)
            else:
                same_index = CFG_edges.index(temp_edge)
                if CFG_weight[same_index]["weight"] < valueee:
                    CFG_weight[same_index]["weight"] = valueee
# 拆分 与 合并
CFG_edges_f, CFG_edges_l = zip(*CFG_edges)
end_CFG_struc = zip(CFG_edges_f, CFG_edges_l, CFG_weight)
CFG.add_edges_from(end_CFG_struc)

# print(CFG.edges())

# 画图
# draw graph
# ------------ 参数 ---------------------------------------------------------------------------------
graph_layout = 'spring'  # 'spring'  'spectral'   'random'   'shell'
node_size = 20
edge_tickness = 1  # 厚度
node_alpha, edge_alpha = 0.3, 0.3
node_text_size = 5
text_font = 'sans-serif'
edge_text_pos = 0.3
labels = (v['weight'] for v in CFG_weight)
labels = list(labels)
edge_labels = dict(zip(CFG_edges, labels))
node_color, edge_color = 'blue', 'blue'
if graph_layout == 'spring':
    graph_pos = nx.spring_layout(CFG)
elif graph_layout == 'spectral':
    graph_pos = nx.spectral_layout(CFG)
elif graph_layout == 'random':
    graph_pos = nx.random_layout(CFG)
else:
    graph_pos = nx.shell_layout(CFG)
# ------------- 参数 -----------------------------------------------------------------------------------

nx.draw_networkx_nodes(CFG, graph_pos, node_size=node_size, alpha=node_alpha, node_color=node_color)
nx.draw_networkx_edges(CFG, graph_pos, width=edge_tickness, alpha=edge_alpha, edge_color=edge_color)
nx.draw_networkx_labels(CFG, graph_pos, font_size=node_text_size, font_family=text_font)
# nx.draw_networkx_edge_labels(CFG, graph_pos, edge_labels=edge_labels, label_pos=edge_text_pos)

plt.show()

# ---------- 生成 csv 文件
cfg_network = open(
    "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\CFG\\CFGnetwork1.csv",
    "w+")
cfg_network.truncate()
cfg_network.write('Source,Target,Weight\n')
for itemm in zip(CFG_edges_f, CFG_edges_l, labels):
    a = str(itemm[0])
    b = str(itemm[1])
    c = round(itemm[2], 3)
    cfg_network.write(str(itemm[0]) + ',' + str(itemm[1]) + ',' + str(c) + "\n")
cfg_network.close()

# ---------- 生成NNS group 写入文件
cfg_network = open(
    "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\editeDistance_0.95\\NNS5.txt", "w+")
cfg_network.truncate()
for itemm in NNS_groups:
    cfg_network.write(str(itemm) + "\n")
cfg_network.close()
