import numpy as np

import EdgesTempTimeSeq
import TimeGap


# generate cfg edges, 对 NNS Group 每个成员生成一个条件概率矩阵。

def funcEdges(NNS_GROUP, Time_TempID_File, edge_lap_thres, bayes_prob_thres):
    # threshold thres3 ---> time lag for any edges' threshold
    thres3 = edge_lap_thres  # 单位为秒
    # threshold thres4 ---> Bayes probability threshold
    thres4 = bayes_prob_thres  # 概率阈值

    # Edges data
    Edges = []
    # 日志时间 + 日志模板编码 序列
    Log_File = Time_TempID_File

    # NNS group 数据生成
    NNS_groups = NNS_GROUP

    for NNS_id in range(len(NNS_groups)):
        # 该模板的 NNS 成员
        G_members = NNS_groups[NNS_id]

        # NNS group 无成员
        if not G_members:
            Edges.append(np.array([]))
            continue

        # 将 G_members 对应的模板加入到 G_members 中
        if not NNS_id in G_members:
            G_members.append(NNS_id)

        # edges of cfg - 邻接矩阵（初始化为单位矩阵）
        NNS_groups_Matrix = np.eye(len(G_members))

        # 相关模板序列 & 时间差序列 ----------------------------------
        Template_sequence, Time_sequence = EdgesTempTimeSeq.Temp_Time_get(G_members, Log_File)
        np_Template_sequence = np.array(Template_sequence)

        # 贝叶斯部分 --------------------------------------------------
        # 先小后大排序
        G_members.sort()

        for condition in G_members:
            # condition 在序列中的个数
            count_condi = Template_sequence.count(condition)
            # condition 在序列中的位置
            condi_local = np.where(np_Template_sequence == condition)
            condi_local = condi_local[0]
            # 阈值内 - 每个 condition 的窗口容纳的结点个数
            node_count_thres3 = []
            # 计算时间阈值 node_count_thres3
            for i in range(len(condi_local)):
                before_time = Time_sequence[condi_local[i]]
                time_gap = 0
                for j in range(condi_local[i] + 1, len(Template_sequence)):
                    later_time = Time_sequence[j]
                    time_gap += TimeGap.Time_Gap(before_time, later_time)
                    if time_gap > thres3:
                        break
                node_count_thres3.append(j - condi_local[i] - 1)

            # 构建直方图
            histo = list((0 for i in range(len(G_members))))
            for i in range(len(condi_local)):  # 遍历每个 condition 结点
                node_gap = node_count_thres3[i]
                for j in range(condi_local[i] + 1, condi_local[i] + node_gap + 1):
                    histo[G_members.index(Template_sequence[j])] += 1

            # 计算贝叶斯概率P( except | condition)
            for i in range(len(histo)):
                histo[i] = histo[i] / count_condi
                if histo[i] < thres4:
                    histo[i] = 0
            # 精确度到0.001
            for i in range(len(histo)):
                if histo[i] > 0:
                    histo[i] = round(histo[i], 3)
                if histo[i] > 1:  # -------------------大于1 的归为1
                    histo[i] = 1

            NNS_groups_Matrix[G_members.index(condition)] = histo
        Edges.append(NNS_groups_Matrix)
    return Edges
