# Function of RealDrawCFGGraph
# 返回 CFG 的网络结构: 一个元组（边集合（list）,权值集合（list））
import numpy as np

import FuncEdges
import FuncNNS


def FuncRealCFG(template_path, log_sequence_path, time_sequence_path, Log_Time_TempID_File,
                NNS_groups_Time_Windows_thres, NNS_groups_Frequence_thres, CFG_edge_lap_thres, CFG_bayes_prob_thres):
    # args -------------------------------------------------------------
    # Template file 日志模板文件             -----> template_path
    # log sequence file 原始日志对应模板序列 -----> log_sequence_path
    # Time sequence file 时间差序列          -----> time_sequence_path
    # 日志时间 + 日志模板编码 序列           -----> Log_Time_TempID_File
    # NNS GROUP : Time windows threshold -------------------> NNS_groups_Time_Windows_thres 单位为秒
    # NNS GROUP : frequence threshold    -------------------> NNS_groups_Frequence_thres
    # CFG : time lag for any edges' threshold --------------> CFG_edge_lap_thres  单位为秒
    # CFG : Bayes probability threshold  -------------------> CFG_bayes_prob_thres 概率阈值
    # ------------------------------------------------------------------
    # NNS group 成员，数据组成方式：一个list , 包含若干个list
    NNS_groups = FuncNNS.NNS_generate_v2(template_path, log_sequence_path, time_sequence_path,
                                         NNS_groups_Time_Windows_thres, NNS_groups_Frequence_thres)

    # NNS group 结构，数据组成方式：一个list , 包含若干个numpy 的 ndarrary
    small_edges_groups = FuncEdges.funcEdges(NNS_groups, Log_Time_TempID_File, CFG_edge_lap_thres, CFG_bayes_prob_thres)

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
                temp_weight = valueee

                if not temp_edge in CFG_edges:
                    CFG_edges.append(temp_edge)
                    CFG_weight.append(temp_weight)
                else:
                    same_index = CFG_edges.index(temp_edge)
                    if CFG_weight[same_index] < valueee:
                        CFG_weight[same_index] = valueee

    return CFG_edges, CFG_weight
