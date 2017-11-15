# find leaf nodes in CFG networks
# Rule: input degree * weight / output degree * weight

def findInList(big_List, value):
    # 返回 bigList 中所有值为 value 的下标
    result = []
    if big_List == []:  # List 为空
        return result
    count_in_list = big_List.count(value)
    if count_in_list == 0:  # List 中不存在该元素
        return result
    num = 0
    for i in range(len(big_List)):
        if big_List[i] == value:
            num += 1
            result.append(i)
            if num >= count_in_list:
                return result


def FuncFindLeaf(edges, weights, threshold):
    Leaf = []
    if not edges == []:
        Left = list((u for (u, v) in edges))
        Right = list((v for (u, v) in edges))

        Nodes = list(set(Left) | set(Right))

        for node in Nodes:
            input_degrees = findInList(Right, node)
            output_degrees = findInList(Left, node)
            if input_degrees == []:
                continue
            elif output_degrees == []:
                up_v = 0
                for i in input_degrees:
                    up_v += weights[i]
                    if up_v / 0.5 >= threshold:
                        Leaf.append(node)
            else:
                # 分子，入度的所有权值
                up_v = 0
                for i in input_degrees:
                    up_v += weights[i]
                # 分母，出度的所有权值
                down_v = 0
                for o in output_degrees:
                    down_v += weights[o]

                node_value = up_v / down_v
                if node_value >= threshold:
                    # 叶子结点
                    Leaf.append(node)
    return Leaf
