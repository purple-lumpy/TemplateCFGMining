# 将 亚业务进行合并 这是一个class
# 亚业务的中间结点之间时间差足够近 + 亚业务之间存在一定程度的关联（体现在CFG图中） 则合并
# 暂时不考虑 CFG 中的关联

class Merge_Miniature():
    # ******** 一个操作 function ************** find list all elements whose value is same with parameter ******************
    def findInList(self, big_List, value):
        # 返回 bigList 中所有值为 value 的下标,无值则返回-1，有值则返回一个list[a,b,c,d,...]
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

    # 初始化^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def __init__(self, temp, workflowID, rawTime):
        # 将硬盘数据写入
        # EachWorkFlow, 中心时间表
        self.EachWorkFlow = [];
        self.Centre_Time = []
        with open(temp) as f:
            self.Temp_Seq = list((int(u.strip()) for u in f.readlines()))
        with open(workflowID) as f:
            self.WorkFlowID = list((int(u.strip()) for u in f.readlines()))
        with open(rawTime) as f:
            self.Raw_Time = list((float(u.strip()) for u in f.readlines()))
        self.Centre_Time = self.Generate_Centre_Time()
        # with open( CFG_Edge_Path ) as f:
        #     Edges = list( ( u.strip() for u in f.readlines()) )
        # with open( CFG_Weight_Path ) as f:
        #     Weights = list( ( u.strip() for u in f.readlines()) )

    # 从 self.Temp_Seq 与 self.WorkFlowID 得到each workflow 的数据^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def Generate_Each_WorkFlow(self):
        WorkFlow = []
        workflow_id = list(set(self.WorkFlowID))
        workflow_id.sort()
        for u in workflow_id:
            temp = []
            index = self.findInList(self.WorkFlowID, u)
            if index == -1:
                WorkFlow.append(temp)
            else:
                for i in index:
                    temp.append(self.Temp_Seq[i])
                WorkFlow.append(temp)
        return WorkFlow

    # 生成中心时间表 Centre_Time ^^^^根据^^^self.WorkFlowID^^^^self.Raw_Time^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def Generate_Centre_Time(self):
        Centre = []
        workflow_id = list(set(self.WorkFlowID))
        workflow_id.sort()
        for u in workflow_id:
            temp = -1
            index = self.findInList(self.WorkFlowID, u)
            if index == -1:
                Centre.append(temp)
            else:
                temp = []
                for i in index:
                    temp.append(self.Raw_Time[i])
                average = round(sum(temp) / len(temp), 3)
                Centre.append(average)
        return Centre

    # 找到一对时间相近的中心点，时间阈值为Time_thres,单位为秒，有则返回一对[a,b],index 为a、b.否则返回 -1.^^^^^^^^^^^^^^
    def Find_Near_Pair(self, Centre_para, Time_thres):
        default_value = -1
        Centre = list((u for u in Centre_para))
        first_index = 0
        while (max(Centre) > -1) and (first_index <= (len(Centre) - 1)):
            if Centre[first_index] == -1:
                first_index += 1
                continue
            for seconde_index in range(first_index + 1, len(Centre)):
                if Centre[seconde_index] == -1:
                    continue
                first_time = Centre[first_index]
                second_time = Centre[seconde_index]
                if abs(first_time - second_time) < Time_thres:
                    return [first_index, seconde_index]
            first_index += 1
        else:
            return default_value

    # 合并业务 ^^^^^^^根据^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def Merge_Miniature(self, time_threshold):
        # 三个表
        WF_id = list((u for u in self.WorkFlowID));
        Temp_Seq = list((u for u in self.Temp_Seq))
        Centre_Time = list((u for u in self.Centre_Time))
        # 中心表中，合并两个元素的时间阈值
        Time_thres = time_threshold
        Merge_pair = self.Find_Near_Pair(Centre_Time, Time_thres)
        while not Merge_pair == -1:
            [first_index, seconde_index] = Merge_pair
            # 1. 更新 Centre_Time 表
            new_center_value = (WF_id.count(first_index) * Centre_Time[first_index] + WF_id.count(seconde_index) *
                                Centre_Time[seconde_index]) \
                               / (WF_id.count(first_index) + WF_id.count(seconde_index))
            Centre_Time[first_index] = new_center_value
            Centre_Time[seconde_index] = -1
            # 2. 更新 WF_id 表
            for i in range(len(WF_id)):
                if WF_id[i] == seconde_index:
                    WF_id[i] = first_index
            # 3. 更新 EachFlow 表 ------------------------------------------------------- 暂不写------------------------


            Merge_pair = self.Find_Near_Pair(Centre_Time, Time_thres)
        # 最终结果更新入类变量
        self.WorkFlowID = WF_id;
        self.Temp_Seq = Temp_Seq;
        self.Centre_Time = Centre_Time


# 调用类 和 类方法 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Temp_Seq_Path = 'F:\\A_Data_20171024\\ProcessedData\\log_clus_index_sequence.txt'
WorkFlowID_Path = 'C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\Workflow\\WorkflowID.txt'
Raw_Time_Path = 'C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\ProcessedData\\ProducedTimeLocation.txt'

test = Merge_Miniature(temp=Temp_Seq_Path, workflowID=WorkFlowID_Path, rawTime=Raw_Time_Path)
# 合并
# 合并函数的参数，中心时间的参数，单位为秒
Time_threshold = 100
test.Merge_Miniature(Time_threshold)
Final_WorkFlow_id = test.WorkFlowID
Final_Each_Workflow = test.Generate_Each_WorkFlow()

# 写 WorkFlow_id 与 Each_WorkFlow
# ---------- 生成CFG 的 csv 文件
WorkFlowID_F = open("C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\Workflow\\Merged\\WorkflowID.txt", "w+")
WorkFlowID_F.truncate()
for item in Final_WorkFlow_id:
    WorkFlowID_F.write(str(item) + "\n")
WorkFlowID_F.close()

Each_WorkFlow_F = open("C:\\Users\\ThinkPad\\Desktop\\TimeData\\0s\\Workflow\\Merged\\EachFlow.txt", "w+")
Each_WorkFlow_F.truncate()
for item in Final_Each_Workflow:
    for inner_item in item:
        Each_WorkFlow_F.write(str(inner_item) + ",")
    Each_WorkFlow_F.write("\n")
Each_WorkFlow_F.close()
