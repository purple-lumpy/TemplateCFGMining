class DFS():
    def __init__(self, edges):
        self.edges = list((v for v in edges))  # 原始边信息

        # 图中包含的结点, 出度结点, 入度结点, 每个结点的邻接结点
        self.nodes = [];
        self.Left = [];
        self.Right = [];
        self.node_neighbors = []
        self.nodes, self.Left, self.Right, self.node_neighbors = self.generate_data(self.edges)
        self.leaf = self.genetate_leaf(self.nodes, self.Left)  # 原始图中叶子结点
        # 根据edges 生成 nodes, left. right, neighbors

    # ******************************************* 初始化数据 self.nodes & self.node_neighbors ******************************
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

                    # *********************************************        所有可达路径      ***********************************************

    def FindRoad_in_Simplified_CFG(self, start_node, end_node):
        Road = []

        def dfs_road(start, end, order_para):
            order_para.append(start)
            if not start in self.leaf:  # node 非叶子结点
                # node 的位置
                node_index = self.nodes.index(start)
                for n in self.node_neighbors[node_index]:
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

    # *********************************************        一条可达路径      ***********************************************
    def FindRoad_in_Simplified_CFG_v2(self, start_node, end_node):
        Road = []

        def dfs_road(start, end, order_para):
            order_para.append(start)
            if not start in self.leaf:  # node 非叶子结点
                # node 的位置
                node_index = self.nodes.index(start)
                for n in self.node_neighbors[node_index]:
                    state_order = list((u for u in order_para))
                    if n == end:
                        if Road == []:
                            temp = list((u for u in state_order))
                            temp.append(n)
                            Road.extend(temp)
                            return
                    if n in state_order:
                        continue
                    dfs_road(n, end, state_order)

        init_road = []
        dfs_road(start_node, end_node, init_road)
        return Road
