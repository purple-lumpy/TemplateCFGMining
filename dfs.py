import CompareListTurn as Comp


# old code,请转移到当前目录下 DFSinCFG.py

class DFS():
    # …………………………………………………DFS 找到循环结构…………………………………………………………………………………………
    # …………………………&&&&&&&&&&&&&& 不考虑单点循环结构 ********##########&&&&&&&&&&&&&……………………………………………………

    def __init__(self, edges):
        self.edges_raw = edges
        self.edges = list((v for v in edges))  # 原始边信息
        self.nodes = []  # 图中包含的结点
        self.OneNodeCycle = []  # 单点循环
        self.Left = []  # 出度结点
        self.Right = []  # 入度结点
        self.node_neighbors = []  # 每个结点的邻接结点
        self.generate_data()  # 初始化--> 图中结点，结点的邻接关系
        self.possi_roots = self.generate_roots()  # 可能是循环的点
        self.root = []  # 当前检测是否存在循环的点
        self.leaf = self.genetate_leaf()  # 图中叶子结点
        self.Cycle = []  # 循环结构 ------------------------------------- 图结构中的一个特殊点
        self.Depth_Fist_Search()  # Find 图中循环结构
        self.SubCycle = []  # 循环结构中非循环子路 结构：list 的 list 一个循环对应一个 --> [[road1],...,[roadn]]
        self.PartCycle = []  # 半循环结构 ------------------------------- 图结构中的一个特殊点
        self.generate_subcycle()  # Find 循环结构中非循环子结构
        self.NewEdges = []  # 新的网络图中边的信息
        self.workflow = []  # WorkFlow的集合， list 的 list
        self.order = []  # Never mind.

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

    # ******************************************* 根据循环 Find 某两点的路径 ***********************************************
    def find_Road(self, cycle, start_node, end_node):
        if start_node == end_node:
            return -1
        start_index = cycle.index(start_node)
        end_index = cycle.index(end_node)
        if end_index > start_index:
            return cycle[start_index:end_index + 1]
        else:
            temp = cycle[start_index:]
            temp.extend(cycle[:end_index + 1])
            return temp
            # ******************************************* 初始化数据 self.nodes & self.node_neighbors ******************************

    def generate_data(self):
        # 初始化所有Node
        for u, v in self.edges_raw:
            if u == v:
                # 单点循环
                self.OneNodeCycle.append(u)
                self.edges.remove((u, v))
        for u, v in self.edges:
            self.Left.append(u)
            self.Right.append(v)
        node_set = set(self.Left) | set(self.Right)
        node_set_list = list(node_set)
        # 做一个排序
        node_set_list.sort()
        self.nodes = node_set_list
        # 初始化邻接点
        for single_node in self.nodes:
            neigh = []
            neigh_index = self.findInList(self.Left, single_node)
            if not neigh_index == -1:
                for index in neigh_index:
                    neigh.append(self.Right[index])
            self.node_neighbors.append(neigh)
            # 生成叶子结点集合

    def genetate_leaf(self):
        leaves = []
        for node in self.nodes:
            if not node in self.Left:
                leaves.append(node)
        return leaves

    # 生成可能有循环的结点的集合（有至少两个度的点，有出度，有入度）
    def generate_roots(self):
        root_list = []
        for node in self.nodes:
            L_count = self.Left.count(node)
            R_count = self.Right.count(node)
            if L_count >= 1 and R_count >= 1:
                root_list.append(node)
        return root_list
        # return [1]

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
            # -------------------- 循环结构 Finish -----------  循环结构内部非循环子路挖掘  ----------------------------------------

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
        for u in self.OneNodeCycle:
            self.NewEdges.append([u, u])


# ********************************************** 网络简化 Finish *******************************************************
edges = [(0, 2), (1, 2), (2, 1), (1, 0), (1, 3), (4, 2), (4, 3), (3, 5), (5, 3), (5, 4), (1, 1), (0, 0), (3, 3)]
aaa = DFS(edges)
print(aaa.Cycle)
# print(aaa.Cycle[2])
# enter,outer = aaa.find_Internet_node_in_cycle(aaa.Cycle[2])
# print("enter of Cycle[2] is : ",enter)
# print("outer of Cycle[2] is : ",outer)
# print("SubCycle of whole Cycle is :", aaa.SubCycle)
# print("PartCycle of whole Graph is : ",aaa.PartCycle)
# aaa.Simplify_NetWork()
# print("Simplified Network is : ", aaa.NewEdges)
#
# # ---------- 生成 csv 文件
# cfg_network = open("C:\\Users\\ThinkPad\\Desktop\\aaa\\Simplified1.csv","w+")
# cfg_network.truncate()
# cfg_network.write('Source,Target,Weight\n')
# for itemm in aaa.NewEdges:
#     cfg_network.write(str(itemm[0]) + ',' +str(itemm[1]) + "\n")
# cfg_network.close()
