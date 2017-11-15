# calculate value for Monte Carlo Tree Search
import DFS_FindRoad
import FindCountinTimeWindow
import FindLocation


def Value_MCTS(Edges, Weights, temp_Seq, time_Seq, window_size, valid_first_stage, thres1, thres2):
    root_node = temp_Seq[0]
    result_value = list((0 for i in range(window_size)))
    for i_vaild_first_stage in range(1, window_size + 1):
        tree_deep = 1  # 深度不要太大
        if not i_vaild_first_stage in valid_first_stage:
            # 该点不可用
            continue
        else:
            # 边
            edge = (root_node, temp_Seq[i_vaild_first_stage])
            if edge in Edges:
                # 边存在------
                tree_deep += 1
                edge_index = Edges.index(edge)
                probability = Weights[edge_index]
                result_value[i_vaild_first_stage - 1] = probability
                # 蒙特卡洛子树
                consi_size = FindCountinTimeWindow.FindCoutWindow(time_Seq[i_vaild_first_stage:], thres1)
                if consi_size == 0:
                    continue
                else:
                    consi_node = temp_Seq[i_vaild_first_stage + 1: i_vaild_first_stage + 1 + consi_size]
                    consi_edges = list(((temp_Seq[i_vaild_first_stage], u) for u in consi_node))
                    # 删掉概率小的边
                    # 新的 edges 对应的权值
                    consi_weight = []
                    for edge_ind in range(len(consi_edges)):
                        if consi_edges[edge_ind] in Edges:
                            s_index = Edges.index(consi_edges[edge_ind])
                            if Weights[s_index] < thres2:
                                consi_edges[edge_ind] = []
                                consi_weight.append(-1)
                            else:
                                consi_weight.append(Weights[s_index])
                        else:
                            consi_edges[edge_ind] = []
                            consi_weight.append(-1)
                    node_index_count = i_vaild_first_stage + 1
                    while len(consi_weight) > 0 and max(consi_weight) > 0:
                        tree_deep += 1
                        if tree_deep > 10:  # 也许应该重新弄个 threshold ......
                            break
                        elif max(consi_weight) < thres2:
                            break
                        # 找出 s_edge 中概率最大边
                        max_val = max(consi_weight)
                        max_index = consi_weight.index(max_val)
                        result_value[i_vaild_first_stage - 1] *= max_val
                        # 最大边指向的结点
                        node_index_count += max_index

                        # 下一个子结点
                        new_node = temp_Seq[node_index_count]
                        # 蒙特卡洛子树
                        consi_size = FindCountinTimeWindow.FindCoutWindow(time_Seq[node_index_count:], thres1)
                        consi_node = temp_Seq[node_index_count + 1: node_index_count + 1 + consi_size]
                        consi_edges = list(((new_node, u) for u in consi_node))

                        # 删掉概率小的边
                        # 新的 edges 对应的权值
                        consi_weight = []
                        for edge_ind in range(len(consi_edges)):
                            if consi_edges[edge_ind] in Edges:
                                s_index = Edges.index(consi_edges[edge_ind])
                                if Weights[s_index] < thres2:
                                    consi_edges[edge_ind] = []
                                    consi_weight.append(-1)
                                else:
                                    consi_weight.append(Weights[s_index])
                            else:
                                consi_edges[edge_ind] = []
                                consi_weight.append(-1)
            else:
                continue
    return result_value


# 加入叶子结点进入判优策略中
def Value_MCTS_v2(Edges, Weights, leaves, temp_Seq, time_Seq, window_size, valid_first_stage, thres1, thres2):
    root_node = temp_Seq[0]
    result_value = list((0 for i in range(window_size)))

    for i_vaild_first_stage in range(1, window_size + 1):

        if not i_vaild_first_stage in valid_first_stage:
            # 该点不可用
            continue
        else:
            # 边
            edge = (root_node, temp_Seq[i_vaild_first_stage])
            if edge in Edges:
                # 边存在------
                if temp_Seq[i_vaild_first_stage] in leaves:
                    result_value[i_vaild_first_stage - 1] = 1
                    return result_value
                else:
                    # 蒙特卡洛子树
                    consi_size = FindCountinTimeWindow.FindCoutWindow(time_Seq[i_vaild_first_stage:], thres1)
                    if consi_size == 0:
                        return result_value
                    else:
                        consi_node = temp_Seq[i_vaild_first_stage + 1: i_vaild_first_stage + 1 + consi_size]
                        for t_node in consi_node:
                            if not (temp_Seq[i_vaild_first_stage], t_node) in Edges:
                                consi_node.remove(temp_Seq[i_vaild_first_stage])
                        consi_edges = list(((temp_Seq[i_vaild_first_stage], u) for u in consi_node))
                        for c_edge in consi_edges:
                            if c_edge[1] in leaves:
                                return result_value


            else:
                continue
    return result_value


def Value_MCTS_v3(Edges, Weights, leaves, temp_Seq, time_Seq, window_size, valid_first_stage, thres1, thres2):
    root_node = temp_Seq[0]
    result_value = list((0 for i in range(window_size)))
    possib_leaves = set(leaves) & set(temp_Seq[1:])

    if possib_leaves == []:
        return result_value

    Edges_Test = []
    some_node = []
    All_root = {0}
    for i_vaild_first_stage in range(1, window_size + 1):
        if not i_vaild_first_stage in valid_first_stage:
            # 该点不可用
            continue
        else:
            # 边
            edge = (root_node, temp_Seq[i_vaild_first_stage])
            if edge in Edges:
                Edges_Test.append((0, i_vaild_first_stage))
                some_node.append(i_vaild_first_stage)
    le = list((u for (u, v) in Edges_Test))
    All_root = All_root | set(le)
    # 生成更新 Edges_Test
    while not some_node == []:
        content = list((u for u in some_node))
        some_node_test = []
        for t_index in content:
            if t_index in All_root:  # 曾经访问过，跳过
                continue
            w_size = FindCountinTimeWindow.FindCoutWindow(time_Seq[t_index:], thres1)
            if w_size == 0:
                continue
            else:
                for number in range(w_size):
                    edge = (temp_Seq[t_index], temp_Seq[t_index + number + 1])
                    if edge in Edges:
                        Edges_Test.append((t_index, t_index + number + 1))
                        some_node_test.append(t_index + number + 1)
        some_node = list(set(some_node_test))
        le = list((u for (u, v) in Edges_Test))
        All_root = All_root | set(le)
    # find 到叶子结点的所有位置 in temp_Seq
    p_index = []
    for p_le in possib_leaves:
        temp_locate = FindLocation.findInList(temp_Seq, p_le)
        p_index.extend(temp_locate)

    # Edges_Test 的出度点（Left）,与入度点（Right）
    Left = list((u for (u, v) in Edges_Test))
    Right = list((v for (u, v) in Edges_Test))

    #  可达根节点的那些叶子的位置信息
    access_root_leaves = list(set(Right) & set(p_index))
    if access_root_leaves == []:
        return result_value
    if 0 in access_root_leaves:
        access_root_leaves.remove(0)

    # 那些可用的叶子结点的位置信息
    # a_r_l_location = []
    # for a_r_l in access_root_leaves:
    #     temp = FindLocation.findInList(temp_Seq, a_r_l)
    #     a_r_l_location.extend(temp)
    # if 0 in a_r_l_location:
    #     a_r_l_location.remove(0)

    # root 到可用叶子结点的路径
    Road_Test_index = []
    for leaf in access_root_leaves:
        a_test = DFS_FindRoad.DFS(Edges_Test)
        a_road = a_test.FindRoad_in_Simplified_CFG_v2(0, leaf)
        Road_Test_index.append(a_road)

    # Road_Test_index 中0 后面的元素
    # second_element = list( (u[1] for u in Road_Test_index) )
    # va = min(second_element)
    # result_value[va] = 1

    # return result_value
    return Road_Test_index
