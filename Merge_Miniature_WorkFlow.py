# 将 亚业务进行合并
# 亚业务的中间结点之间时间差足够近 + 亚业务之间存在一定程度的关联（体现在CFG图中） 则合并
# 暂时不考虑 CFG 中的关联

# 将硬盘数据写入
Temp_Seq_Path = 'F:\\A_Data_20171024\\ProcessedData\\log_clus_index_sequence.txt'
WorkFlowID_Path = 'F:\\A_Data_20171024\\WorkFlow\\WorkflowID.txt'
Raw_Time_Path = 'F:\\A_Data_20171024\\ProcessedData\\ProducedTimeLocation.txt'

# CFG_Edge_Path = ''
# CFG_Weight_Path = ''

with open(Temp_Seq_Path) as f:
    Temp_Seq = list((u.strip() for u in f.readlines()))
with open(WorkFlowID_Path) as f:
    WorkFlowID = list((u.strip() for u in f.readlines()))
with open(Raw_Time_Path) as f:
    Raw_Time = list((int(u.strip()) for u in f.readlines()))


# with open( CFG_Edge_Path ) as f:
#     Edges = list( ( u.strip() for u in f.readlines()) )
# with open( CFG_Weight_Path ) as f:
#     Weights = list( ( u.strip() for u in f.readlines()) )
def Generate_Each_WorkFlow():
    pass
