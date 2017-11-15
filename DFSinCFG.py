import CompareListTurn as Comp


class DFS():
    # …………………………………………………DFS 找到循环结构……………………………………………………………………………………
    # …………………………&&&&&&&&&&&&&& 不考虑单点循环结构 *********##########&&&&&&&&&&&&&…………………………………………

    def __init__(self, edges):
        self.edges_raw = edges
        self.edges = list((v for v in edges))  # 原始边信息
        self.OneNodeCycle = []  # 单点循环
        self.GenOneNodeCycle()  # 删除 self.edges 单点循环结构，并将它保存在 self.OneNodeCycle 中
        # 图中包含的结点, 出度结点, 入度结点, 每个结点的邻接结点
        self.nodes = [];
        self.Left = [];
        self.Right = [];
        self.node_neighbors = []
        self.nodes, self.Left, self.Right, self.node_neighbors = self.generate_data(self.edges)
        self.leaf = self.genetate_leaf(self.nodes, self.Left)  # 原始图中叶子结点

        self.possi_roots = self.generate_roots()  # 可能是循环的点
        self.root = []  # 当前检测是否存在循环的点
        self.Cycle = []  # 循环结构 ------------------------------------- 图结构中的一个特殊点
        self.Depth_Fist_Search()  # Find 图中循环结构
        self.SubCycle = []  # 循环结构中非循环子路 结构：list 的 list 一个循环对应一个 --> [[road1],...,[roadn]]
        self.PartCycle = []  # 半循环结构 ------------------------------- 图结构中的一个特殊点
        self.generate_subcycle()  # Find 循环结构中非循环子结构
        self.order = []  # Never mind.

        self.NewEdges = []  # 新的网络图中边的信息
        # 图中包含的结点, 出度结点, 入度结点, 每个结点的邻接结点
        self.NewNodes = [];
        self.NewLeft = [];
        self.NewRight = [];
        self.NewNode_neighbors = []
        self.NewLeaf = []  # 简化后CFG 中叶子结点
        self.WorkFlow = []  # WorkFlow的集合， list 的 list

    # ******************************* find list all elements whose value is same with parameter ****************************
    def findInList(self, big_List, value):
        # 返回 bigList 中所有值为 value 的下标
        result = []
        if big_List == []:  # List 为空
            return -1
        count_in_list = big_List.count(value)
        if count_in_list == 0:  # List 中不存在该元素
            return -1
        num = 0
        for i in range(len(big_List)):
            if big_List[i] == value:
                num += 1
                result.append(i)
                if num >= count_in_list:
                    return result
                    # ***************************** find internet node in a cycle **********************************************************

    def find_Internet_node_in_cycle(self, cycle):
        # 输出为（enter,outer）: enter 为该 cycle 有入度的结点， outer 为cycle 中有出度的结点
        enter = []
        outer = []
        for node in cycle:
            # 外界 ---> 循环，入度结点
            temp1 = self.findInList(self.Right, node)
            if not temp1 == -1:
                # 排除掉循环中的边
                for val in temp1:
                    if not self.Left[val] in cycle:
                        enter.append(node)
                        break
            # 循环 --> 外界，出度结点
            temp2 = self.findInList(self.Left, node)
            if not temp2 == -1:
                # 排除掉循环中的边
                for val in temp2:
                    if not self.Right[val] in cycle:
                        outer.append(node)
                        break
        return enter, outer

    # ******************************************* 从边信息中得到点信息 *****************************************************
    def EdgeToPoint(self, edges):
        left = [];
        right = []
        for u, v in edges:
            left.append(u)
            right.append(v)
        node_set = set(left) | set(right)
        node_set_list = list(node_set)
        return node_set_list

    # ******************************************* 根据循环 Find 某两点的路径 ***********************************************
    def find_Road(self, cycle_para, start_node, end_node):
        cycle = list((va for va in cycle_para))
        start_index = cycle.index(start_node)
        end_index = cycle.index(end_node)
        if end_index > start_index:
            return cycle[start_index:end_index + 1]
        elif end_index == start_index:
            if end_index == 0:
                temp = cycle
                temp.append(temp[0])
                return temp
            else:
                temp = cycle[start_index:]
                temp.extend(cycle[:end_index + 1])
                return temp
        else:
            temp = cycle[start_index:]
            temp.extend(cycle[:end_index + 1])
            return temp

    # 两个cycle 有交集，求路径
    def find_Road_Two_Cycles(self, cycle1, cycle2, start_node, end_node):
        # 假设start_node 在 cycle1， end_node 在 cycle2
        if start_node == end_node:
            return -1
        same_node = list(set(cycle1) & set(cycle2))
        road = self.find_Road(cycle1, start_node, same_node[0])
        road1 = self.find_Road(cycle2, same_node[0], end_node)
        road.extend(road1[1:])
        return road

    # ******************************************* 找到图中所有分支结点 *****************************************************
    def Find_Branch_nodes(self):
        result = []
        for v in self.Left:
            if self.Left.count(v) > 1:
                if not v in result:
                    result.append(v)
        return result

    # ******************************************* 初始化数据 self.nodes & self.node_neighbors ******************************
    # 去掉self.edges 中的单点循环，并将单点循环保存在 self.OneNodeCycle
    def GenOneNodeCycle(self):
        for u, v in self.edges_raw:
            if u == v:
                # 单点循环
                self.OneNodeCycle.append(u)
                self.edges.remove((u, v))

    # 根据edges 生成 nodes, left. right, neighbors
    def generate_data(self, edges):
        # 初始化所有Node
        left = [];
        right = [];
        nodes = [];
        neighbors = []
        for u, v in edges:
            left.append(u)
            right.append(v)
        nodes = self.EdgeToPoint(edges)
        # 初始化邻接点
        for single_node in nodes:
            neigh = []
            neigh_index = self.findInList(left, single_node)
            if not neigh_index == -1:
                for index in neigh_index:
                    neigh.append(right[index])
            neighbors.append(neigh)
        return nodes, left, right, neighbors

    # ______________________________________________ 生成叶子结点集合 ______________________________________________________
    def genetate_leaf(self, nodes, left):
        leaves = []
        for node in nodes:
            if not node in left:
                leaves.append(node)
        return leaves

    # 生成可能有循环的结点的集合（有至少两个度的点，有出度，有入度）________________________________________________________
    def generate_roots(self):
        root_list = []
        for node in self.nodes:
            L_count = self.Left.count(node)
            R_count = self.Right.count(node)
            if L_count >= 1 and R_count >= 1:
                root_list.append(node)
        return root_list
        # return [1]

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 从名字计算出链结点内容 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def FromNameGetNoded(self, name):
        name1, name2 = name.split("#")
        index = int(name2)
        if name1 == 'P':
            return self.PartCycle[index]
        elif name1 == 'C':
            return self.Cycle[index]
        else:
            return "Cannot find structure- func 'FromNameGetNoded(self,name)'"
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  WorkFlow 的翻译处理  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def TransferWorkFlow(self, chains, start_node, end_node):
        result_list = []
        for chain in chains:
            result = []
            # 不需要翻译
            for i in chain:
                if not type(i) == int:
                    break
            else:
                result_list.append(chain)
                continue
            # 进行翻译
            last_node = 0
            if chain[0] == start_node:
                # 普通结点
                result.append(start_node)
                last_node = start_node
            else:
                # 特殊结点
                context = self.FromNameGetNoded(chain[0])
                s1, s2 = chain[0].split("#")
                # 非环结构
                if s1 == "P":
                    index = context.index(start_node)
                    result.append(context[index:])
                    last_node = result[-1]
                else:  # 环结构
                    index = context.index(start_node)
                    if index == 0:
                        temp = list((u for u in context))
                        temp.append(context[0])
                        result.extend(temp)
                    else:
                        temp = context[index:]
                        temp.extend(context[:index + 1])
                        result.extend(temp)
                    last_node = result[-1]
            for i in range(1, len(chain) - 1):
                if type(chain[i]) is int:
                    result.append(chain[i])
                    last_node = result[-1]
                else:
                    context = self.FromNameGetNoded(chain[i])
                    s1, s2 = chain[i].split('#')
                    if s1 == "P":  # 非环结构
                        result.extend(context)
                        last_node = result[-1]
                    else:  # 环结构
                        for va in context:
                            if (last_node, va) in self.edges:
                                index = context.index(va)
                                break
                        if index == 0:
                            temp = list((u for u in context))
                            temp.append(context[0])
                            result.extend(temp)
                            last_node = result[-1]
                        else:
                            temp = context[index:]
                            temp.extend(context[:index + 1])
                            result.extend(temp)
                            last_node = result[-1]
                        # 如果下一个是特殊结构
                        if type(chain[i + 1]) is not int:
                            result.pop()
                            last_node = result[-1]
            if chain[-1] == end_node:
                result.append(end_node)
            else:
                context = self.FromNameGetNoded(chain[-1])
                if context[0] == last_node:
                    end_index = context.index(end_node)
                    result.extend(context[:end_index + 1])
                else:
                    for va in context:
                        if (last_node, va) in self.edges:
                            index = context.index(va)
                            break
                    end_index = context.index(end_node)
                    if index < end_index:
                        result.extend(context[index:end_index + 1])
                    elif index == end_index:
                        result.extend(context[index:end_index + 1])
                    else:
                        temp = context[index:]
                        temp.extend(context[:end_index + 1])
                        result.extend(temp)
            result_list.append(result)
        return result_list

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 删除重复元素 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def DeleteSame(self, cols):
        result = cols
        if not cols == []:
            for va in result:
                if result.count(va) > 1:
                    result.remove(va)
        return result

    # ############################################## 循环结构挖掘 ##########################################################
    def Depth_Fist_Search(self):
        # 递归进行深度优先遍历图
        def dfs(node, order_para):

            order_para.append(node)
            if not node in self.leaf:  # node 非叶子结点
                # node 的位置
                node_index = self.nodes.index(node)
                for n in self.node_neighbors[node_index]:
                    state_order = list((u for u in order_para))
                    if n == self.root:
                        if self.Cycle == []:
                            self.Cycle.append(state_order)
                        else:
                            for old_order in self.Cycle:
                                if Comp.SameCycle(old_order, state_order):
                                    break
                            else:
                                self.Cycle.append(state_order)
                        continue
                    if n in state_order:
                        continue
                    dfs(n, state_order)

        # 根节点循环
        for root_node in self.possi_roots:
            # 更新 order
            self.order = []
            # 更新 root
            self.root = root_node
            dfs(root_node, self.order)
            # -------------------------------------- 循环结构 Finish ---------------------------------------------------------------
            # ********************************************* 简化后的网络发现可达路径 ***********************************************

    def FindRoad_in_Simplified_CFG(self, start_node, end_node):
        Road = []

        def dfs_road(start, end, order_para):
            order_para.append(start)
            if not start in self.leaf:  # node 非叶子结点
                # node 的位置
                node_index = self.NewNodes.index(start)
                for n in self.NewNode_neighbors[node_index]:
                    state_order = list((u for u in order_para))
                    if n == end:
                        if Road == []:
                            temp = list((u for u in state_order))
                            temp.append(n)
                            Road.append(temp)
                        else:
                            temp = list((u for u in state_order))
                            temp.append(n)
                            if not temp in Road:
                                Road.append(temp)
                        continue
                    if n in state_order:
                        continue
                    dfs_road(n, end, state_order)

        init_road = []
        dfs_road(start_node, end_node, init_road)
        return Road

    # ------  循环结构内部非循环子路挖掘  ----------------------------------------------------------------------------------
    def generate_subcycle(self):
        if not self.Cycle == []:
            for cy in self.Cycle:
                record_road = []
                # 一个 Cycle 结构
                enter_node, out_node = self.find_Internet_node_in_cycle(cy)
                if (not enter_node == []) and (not out_node == []):
                    for e_node in enter_node:
                        for o_node in out_node:
                            if not e_node == o_node:
                                # 计算路径
                                road = self.find_Road(cy, e_node, o_node)
                                record_road.append(road)
                self.SubCycle.append(record_road)
        for val in self.SubCycle:
            if not val == []:
                for micro_val in val:
                    if not micro_val in self.PartCycle:
                        self.PartCycle.append(micro_val)
                        # ****************** 循环结构内部非循环子路 Finish ********* 网络简化 START * ******************************************

    def Simplify_NetWork(self):
        # 新的结点在self.Cycle and self.PartCycle 中保存
        # 构建新的结点的边关系
        for index in range(len(self.Cycle)):
            # 第 index 个Cycle
            cyc = self.Cycle[index]
            # 循环中与外界交流的结点
            in_c, out_c = self.find_Internet_node_in_cycle(cyc)
            if in_c == [] and out_c == []:
                # 该循环与外界无联系
                self.NewEdges.append(['C#' + str(index), 'End'])
            elif (not in_c == []) and out_c == []:
                # 该循环无出度，只有入度
                ancestors = list((u for u, v in self.edges if v in in_c and not u in cyc))
                if not ancestors == []:
                    for va in ancestors:
                        self.NewEdges.append([va, 'C#' + str(index)])
            elif in_c == [] and (not out_c == []):
                # 该循环无入度，只有出度
                descendants = list((v for u, v in self.edges if u in out_c and not v in cyc))
                if not descendants == []:
                    for va in descendants:
                        self.NewEdges.append(['C#' + str(index), va])
            else:
                # 该循环有入度有出度
                for i in in_c:
                    for j in out_c:
                        if i == j:
                            # 入度点和出度点是同一个点
                            # --> i -->
                            # --> 循环 -->
                            for u, v in self.edges:
                                if u == i and (not v in cyc):
                                    self.NewEdges.append([u, v])
                                    self.NewEdges.append(['C#' + str(index), v])
                                elif v == i and (not u in cyc):
                                    self.NewEdges.append([u, v])
                                    self.NewEdges.append([u, 'C#' + str(index)])
                        else:
                            # 入度点和出度点不是同一个点
                            part_road = self.find_Road(cyc, i, j)
                            # part_road 在 self.PartCycle 中的下标
                            part_road_id = self.PartCycle.index(part_road)
                            # --> 路径（i,j）-->
                            # --> 循环 --> 路径（i,j）-->
                            for u, v in self.edges:
                                if v == i and (not u in cyc):
                                    self.NewEdges.append([u, 'P#' + str(part_road_id)])
                                    self.NewEdges.append([u, 'C#' + str(index)])
                                    self.NewEdges.append(['C#' + str(index), 'P#' + str(part_road_id)])
                                if u == j and (not v in cyc):
                                    self.NewEdges.append(['P#' + str(part_road_id), v])
        # self.NewEdges 重复结点删除
        for va in self.NewEdges:
            if self.NewEdges.count(va) > 1:
                self.NewEdges.remove(va)
        # 循环中的所有结点
        node_in_Cycle = []
        if not self.Cycle == []:
            for cycle in self.Cycle:
                # 每个cycle
                for n in cycle:
                    if not n in node_in_Cycle:
                        node_in_Cycle.append(n)
        # 加入除循环结构外的边信息进self.NewEdges
        for u, v in self.edges:
            if (not u in node_in_Cycle) and (not v in node_in_Cycle):
                self.NewEdges.append([u, v])
        # 加入但单节点循环
        # for u in self.OneNodeCycle:ew
        #     self.NewEdges.append([u,u])
        # 新数据及叶子结点的生成
        self.NewNodes, self.NewLeft, self.NewRight, self.NewNode_neighbors = self.generate_data(self.NewEdges)
        self.NewLeaf = self.genetate_leaf(self.NewNodes, self.NewLeft)

    # **************************** 网络简化 Finish *************** Find 业务流 *********************************************
    def FindWorkFlow(self, init_points):
        if init_points:
            # 有起始结点与终止结点
            for pair in init_points:
                start_node = pair[0]
                end_node = pair[1]
                # start_node and end_node 分别属于哪些( 普通 + 特殊即环 )结构Start_Stru, End_Stru -----> 值仅为p#i 与 i
                Start_Stru = [];
                End_Stru = []
                for i in range(len(self.Cycle)):
                    if start_node in self.Cycle[i]:
                        Start_Stru.append("C#" + str(i))
                    if end_node in self.Cycle[i]:
                        End_Stru.append("C#" + str(i))
                if start_node in self.NewNodes:
                    Start_Stru.append(start_node)
                if end_node in self.NewNodes:
                    End_Stru.append(end_node)
                for start_sss in Start_Stru:
                    for end_sss in End_Stru:
                        cycle1 = [];
                        cycle2 = []
                        if not type(start_sss) is int:
                            cycle1 = self.FromNameGetNoded(start_sss)
                        if not type(end_sss) is int:
                            cycle2 = self.FromNameGetNoded(end_sss)
                        # end 与 start 在同一个循环中
                        if start_sss == end_sss:
                            road = self.find_Road(cycle1, start_node, end_node)
                            if not road in self.WorkFlow:
                                self.WorkFlow.append(road)
                        elif not list(set(cycle1) & set(cycle2)) == []:
                            road = self.find_Road_Two_Cycles(cycle1, cycle2, start_node, end_node)
                            if not road in self.WorkFlow:
                                self.WorkFlow.append(road)
                        else:
                            if not (start_sss in cycle2 or end_sss in cycle1):
                                road = self.FindRoad_in_Simplified_CFG(start_sss, end_sss)
                                if not road == []:
                                    road_trans = self.TransferWorkFlow(road, start_node, end_node)
                                    for va in road_trans:
                                        if not va in self.WorkFlow:
                                            self.WorkFlow.append(va)


# ******************************************** 业务流挖掘结束 **********************************************************
edges = [(0, 2), (1, 2), (2, 1), (1, 0), (1, 3), (4, 2), (4, 3), (3, 5), (5, 3), (5, 4), (1, 1), (0, 0), (3, 3), (4, 6)]
aaa = DFS(edges)
# print(" Raw nodes are : ",aaa.nodes)
# print("    Cycles are : ",aaa.Cycle)
# print("PartCycles are : ",aaa.PartCycle)
#
aaa.Simplify_NetWork()
# print(" New nodes are : ", aaa.NewNodes)
# print("     Edges are : ", aaa.NewEdges)
# print(" Neighbors are : ", aaa.NewNode_neighbors)

aaa.FindWorkFlow([[1, 6]])
print("  WorkFlow are : ", aaa.WorkFlow)

# # ---------- 生成 csv 文件
# cfg_network = open("C:\\Users\\ThinkPad\\Desktop\\aaa\\Simplified1.csv","w+")
# cfg_network.truncate()
# cfg_network.write('Source,Target,Weight\n')
# for itemm in aaa.NewEdges:
#     cfg_network.write(str(itemm[0]) + ',' +str(itemm[1]) + "\n")
# cfg_network.close()
