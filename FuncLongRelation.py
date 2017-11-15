# 计算长距离依赖关系

def longRelation(PreA, A, PreB, B, small_time_thres, big_time_thres, template_seq, time_seq, win_size):
    # 阈值（两个：1. PreA 到 A 的time-window; 2. PreB - PreA 的time-window）
    time_Win_PreA_A = small_time_thres  # 1     # 单位为秒
    time_Win_PreA_PreB = big_time_thres  # 20 # 单位为秒

    # log sequence
    log_sequence = template_seq
    # Time sequence(记录的是time gap)
    time_sequence_path = time_seq
    # Windows size sequence
    Windows_size = win_size

    # PreA and PreB 在时间轴上的index,第一个元素(的位置)为0
    PreA_locat = [];
    PreB_locat = []
    # 有用的PreA（在PreB前面的PreA） and 有用的PreB的位置（PreB后面有B）
    Useful_PreA_locat = [];
    Useful_PreB_locat = []

    # 变量（PreA, A）-> (PreB,B) 与 （PreA,A）<- (PreB,B)
    A_B = 0
    A_not_B = 0

    # __________________________________________________________________________________________________________________

    # PreA_locat，PreB_locat 的生成
    for index in range(len(log_sequence)):
        if log_sequence[index] == PreA:
            PreA_locat.append(index)
        elif log_sequence[index] == PreB:
            PreB_locat.append(index)

    # Useful_PreB_locat 与 Useful_PreA_locat 的生成
    for index in range(len(PreB_locat)):
        location = PreB_locat[index]
        windows = Windows_size[location]
        if not windows == 0:
            # 窗口非空
            temp = log_sequence[location + 1: location + windows + 1]
            if B in temp:
                # 窗口中包含 B
                for i in range(location - 1, -1, -1):
                    if log_sequence[i] == PreA:
                        # 最近的PreA
                        time_sum = 0
                        for num in range(i + 1, location + 1):
                            time_sum += time_sequence_path[num]
                        if time_sum <= time_Win_PreA_PreB:
                            # 存在PreA
                            Useful_PreB_locat.append(location)
                            Useful_PreA_locat.append(i)
                            break
    # 计算（PreA, A）-> (PreB,B) 与 （PreA,A）<- (PreB,B)
    for index in range(len(Useful_PreA_locat)):
        location = Useful_PreA_locat[index]
        windows = Windows_size[location]
        if not windows == 0:
            # 窗口非空
            temp = log_sequence[location + 1: location + windows + 1]
            if A in temp:
                A_B += 1
                break

    A_not_B = len(Useful_PreA_locat) - A_B

    result = (A_B - A_not_B) / (1 + A_B + A_not_B)
    return result
