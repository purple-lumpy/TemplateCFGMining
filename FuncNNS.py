# function of GenerateNNS
# v1 is old version, which calculates the frequence of NNS Group menbers in a way: the ALL elements in Time Windows will be considered
# v2 is newer than v1, which calculates the frequency of NNS Group members in a way: the Same elements in Time Window will be throwed away, and
# the Frequen_thres is different from v1, in v2, it use  ( group members count ) / ( object count ) as a threshold
# v3 is newer than v2, which used backward look for each object to find the more appropriate NNs Group

def NNS_generate_v1(Templates, Temp_index, Temp_Time, TimeWin_thres, Frequen_thres):
    # threshold thres1 ---> time windows threshold, threshold thres2 ---> frequence threshold, 单位为秒
    thres1 = TimeWin_thres;
    thres2 = Frequen_thres
    # NNS Group data
    NNS = []

    # Template file
    template_path = Templates
    Template_file = open(template_path)
    # log sequence file
    log_sequence_path = Temp_index
    # Time sequence file
    time_sequence_path = Temp_Time

    # 模板个数
    Template_num = len(Template_file.readlines())
    Template_file.close()

    # 生成NNS group
    for i in range(Template_num):
        group = []
        ## find indexes of i in the sequence ----------------------------------
        # i_indexes 记录了序列中 i 出现的位置
        i_indexes = []
        Log_file = open(log_sequence_path)
        temp_index = 0  # 当前i 出现的位置
        while 1:
            lines = Log_file.readlines(100000)
            if not lines:
                break
            for line in lines:
                if line.strip() == str(i):
                    i_indexes.append(temp_index)
                    temp_index += 1
                else:
                    temp_index += 1
        Log_file.close()
        ## find sequence window for thres1(time) -------------------------------
        # record 数组记录了每一个点在window
        t_index = 0  # 将要达到的i_indexes的index
        record = []  # 记录个数 for 每个结点在 windows 中有多少个后驱结点
        while t_index < len(i_indexes):  # 对每个位置，分别求时间窗在序列维度上的大小
            Time_sequence_file = open(time_sequence_path)
            time_index = 0  # 时间差文件中当前访问点的index
            while 1:
                lines = Time_sequence_file.readline()
                if not lines:
                    break
                if time_index == i_indexes[t_index]:
                    sum_of_next = 0  # 合计后面的时间差
                    node_count = 0
                    while sum_of_next < thres1:
                        node_count += 1
                        temp_line = Time_sequence_file.readline()
                        if not temp_line:
                            break  # 读到文件尾
                        time_temp = float(temp_line.strip())
                        sum_of_next += time_temp
                    node_count -= 1
                    Time_sequence_file.close()
                    record.append(node_count)
                    t_index += 1  # 跳到下一条
                    break
                else:
                    time_index += 1

        ## 构建直方图 --- 模板的后驱结点们出现的频数-------------------------------------------
        # 直方图生成变量
        frequences = list((0 for i in range(Template_num)))
        t_index = 0  # 将要达到的i_indexes的index
        while t_index < len(i_indexes):
            Log_file = open(log_sequence_path)
            time_index = 0  # 序列上遍历的index
            while 1:
                lines = Log_file.readline()
                if not lines:
                    break
                if time_index == i_indexes[t_index]:
                    temp_next = record[t_index]  # 窗口大小
                    for i in range(temp_next):  # 将时间窗口中的结点记录进直方图
                        temp_line = Log_file.readline()
                        fre_index = int(temp_line.strip())
                        frequences[fre_index] += 1
                    Log_file.close()
                    t_index += 1  # 跳到下一条
                    break
                else:
                    time_index += 1

        # 频率直方图
        big_value = sum(frequences)
        fre_his = []
        if big_value == 0:
            fre_his = frequences
        else:
            fre_his = list((round(value / big_value, 3) for value in frequences))
        # 频率超过阈值，成为NNS group 成员
        for i in range(Template_num):
            if fre_his[i] >= thres2:
                group.append(i)
        NNS.append(group)
    return NNS


def NNS_generate_v2(Templates, Temp_index, Temp_Time, TimeWin_thres, Frequen_thres):
    # threshold thres1 ---> time windows threshold, threshold thres2 ---> frequence threshold, 单位为秒
    thres1 = TimeWin_thres;
    thres2 = Frequen_thres
    # NNS Group data
    NNS = []

    # Template file
    template_path = Templates
    Template_file = open(template_path)
    # log sequence file
    log_sequence_path = Temp_index
    # Time sequence file
    time_sequence_path = Temp_Time

    # 模板个数
    Template_num = len(Template_file.readlines())
    Template_file.close()

    # 生成NNS group
    for i in range(Template_num):
        group = []
        ## find indexes of i in the sequence ----------------------------------
        # i_indexes 记录了序列中 i 出现的位置
        i_indexes = []
        Log_file = open(log_sequence_path)
        temp_index = 0  # 当前i 出现的位置
        while 1:
            lines = Log_file.readlines(100000)
            if not lines:
                break
            for line in lines:
                if line.strip() == str(i):
                    i_indexes.append(temp_index)
                    temp_index += 1
                else:
                    temp_index += 1
        Log_file.close()
        ## find sequence window for thres1(time) -------------------------------
        # record 数组记录了每一个点在window
        t_index = 0  # 将要达到的i_indexes的index
        record = []  # 记录个数 for 每个结点在 windows 中有多少个后驱结点
        while t_index < len(i_indexes):  # 对每个位置，分别求时间窗在序列维度上的大小
            Time_sequence_file = open(time_sequence_path)
            time_index = 0  # 时间差文件中当前访问点的index
            while 1:
                lines = Time_sequence_file.readline()
                if not lines:
                    break
                if time_index == i_indexes[t_index]:
                    sum_of_next = 0  # 合计后面的时间差
                    node_count = 0
                    while sum_of_next < thres1:
                        node_count += 1
                        temp_line = Time_sequence_file.readline()
                        if not temp_line:
                            break  # 读到文件尾
                        time_temp = float(temp_line.strip())
                        sum_of_next += time_temp
                    node_count -= 1
                    Time_sequence_file.close()
                    record.append(node_count)
                    t_index += 1  # 跳到下一条
                    break
                else:
                    time_index += 1

        ## 构建直方图 --- 模板的后驱结点们出现的频数-------------------------------------------
        # 直方图生成变量
        frequences = list((0 for i in range(Template_num)))
        t_index = 0  # 将要达到的i_indexes的index
        while t_index < len(i_indexes):
            Log_file = open(log_sequence_path)
            time_index = 0  # 序列上遍历的index
            while 1:
                lines = Log_file.readline()
                if not lines:
                    break
                if time_index == i_indexes[t_index]:
                    temp_next = record[t_index]  # 窗口大小
                    temp_win_content = []
                    for i in range(temp_next):  # 将时间窗口中的结点记录进直方图
                        temp_line = int(Log_file.readline().strip())
                        temp_win_content.append(temp_line)
                    set_temp_win_content = set(temp_win_content)
                    for va in set_temp_win_content:
                        frequences[va] += 1
                    Log_file.close()
                    t_index += 1  # 跳到下一条
                    break
                else:
                    time_index += 1

        # 频率超过阈值，成为NNS group 成员
        if max(frequences) > 0:
            for i in range(Template_num):
                if frequences[i] / len(i_indexes) >= thres2:
                    group.append(i)
        NNS.append(group)
    return NNS


def NNS_generate_v3(Templates, Temp_index, Temp_Time, TimeWin_thres, Frequen_thres):
    # threshold thres1 ---> time windows threshold, threshold thres2 ---> frequence threshold, 单位为秒
    thres1 = TimeWin_thres;
    thres2 = Frequen_thres
    # NNS Group data
    NNS_F = []
    NNS_B = []
    # Template file
    template_path = Templates
    Template_file = open(template_path)
    # 模板个数
    Template_num = len(Template_file.readlines())
    Template_file.close()

    # log sequence file
    log_sequence_path = Temp_index
    # 将序列保存进来
    Log_Seq = []
    with open(log_sequence_path) as f:
        a = f.readlines()
    for line in a:
        Log_Seq.append(int(line.strip()))

    # Time sequence file
    time_sequence_path = Temp_Time
    # 将时间保存进来
    Time_Gap_Seq = []
    with open(time_sequence_path) as f:
        time_raw = reversed(f.readlines())
    for line in time_raw:
        Time_Gap_Seq.append(float(line.strip()))

    # 生成NNS group
    for i in range(Template_num):
        group_forward = []
        group_backward = []
        ## find indexes of i in the sequence ----------------------------------
        # i_indexes 记录了序列中 i 出现的位置
        i_indexes = []
        Log_file = open(log_sequence_path)
        temp_index = 0  # 当前i 出现的位置
        while 1:
            lines = Log_file.readlines(100000)
            if not lines:
                break
            for line in lines:
                if line.strip() == str(i):
                    i_indexes.append(temp_index)
                    temp_index += 1
                else:
                    temp_index += 1
        Log_file.close()
        # -- 前向的 频繁元素发现 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ## find sequence window for thres1(time) -------------------------------
        # record_forward 数组记录了每一个点在window
        t_index = 0  # 将要达到的i_indexes的index
        record_forward = []  # 记录个数 for 每个结点在 windows 中有多少个后驱结点
        while t_index < len(i_indexes):  # 对每个位置，分别求时间窗在序列维度上的大小
            Time_sequence_file = open(time_sequence_path)
            time_index = 0  # 时间差文件中当前访问点的index
            while 1:
                lines = Time_sequence_file.readline()
                if not lines:
                    break
                if time_index == i_indexes[t_index]:
                    sum_of_next = 0  # 合计后面的时间差
                    node_count = 0
                    while sum_of_next < thres1:
                        node_count += 1
                        temp_line = Time_sequence_file.readline()
                        if not temp_line:
                            break  # 读到文件尾
                        time_temp = float(temp_line.strip())
                        sum_of_next += time_temp
                    node_count -= 1
                    Time_sequence_file.close()
                    record_forward.append(node_count)
                    t_index += 1  # 跳到下一条
                    break
                else:
                    time_index += 1

        # -- 后向的 频繁元素发现 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ## find sequence window for thres1(time) -------------------------------
        # record_backward 数组记录了每一个点在window
        t_index = 0  # 将要达到的i_indexes的index
        record_backward = []  # 记录个数 for 每个结点在 windows 中有多少个前驱结点
        while t_index < len(i_indexes):  # 对每个位置，分别求时间窗在序列维度上的大小
            time_index = i_indexes[t_index]  # 时间差序列中当前访问点的index
            sum_of_next = Time_Gap_Seq[len(Time_Gap_Seq) - time_index - 1]  # 合计前面的时间差
            node_count = 1
            i = 1
            while sum_of_next < thres1 / 2:
                if time_index - i < 0:
                    break
                sum_of_next += Time_Gap_Seq[len(Time_Gap_Seq) - (time_index - i) - 1]
                node_count += 1
                i += 1
            node_count -= 1
            record_backward.append(node_count)
            t_index += 1

        ## 构建直方图 --- 模板的后驱结点们出现的频数--------------------------------------------------------------------
        # 直方图生成变量
        frequences_forward = list((0 for i in range(Template_num)))
        t_index = 0  # 将要达到的i_indexes的index
        while t_index < len(i_indexes):
            Log_file = open(log_sequence_path)
            time_index = 0  # 序列上遍历的index
            while 1:
                lines = Log_file.readline()
                if not lines:
                    break
                if time_index == i_indexes[t_index]:
                    temp_next = record_forward[t_index]  # 窗口大小
                    temp_win_content = []
                    for i in range(temp_next):  # 将时间窗口中的结点记录进直方图
                        temp_line = int(Log_file.readline().strip())
                        temp_win_content.append(temp_line)
                    set_temp_win_content = set(temp_win_content)
                    for va in set_temp_win_content:
                        frequences_forward[va] += 1
                    Log_file.close()
                    t_index += 1  # 跳到下一条
                    break
                else:
                    time_index += 1

        ## 构建直方图 --- 模板的前驱结点们出现的频数--------------------------------------------------------------------
        # 直方图生成变量 Log_Seq
        frequences_backward = list((0 for i in range(Template_num)))
        t_index = 0  # 将要达到的i_indexes的index
        while t_index < len(i_indexes):
            time_index = i_indexes[t_index]  # 序列上遍历的index
            temp_next = record_backward[t_index]  # 窗口大小
            if temp_next >= 1:
                temp_win_content = Log_Seq[time_index - temp_next: time_index]
                set_temp_win_content = set(temp_win_content)
                for va in set_temp_win_content:
                    frequences_backward[va] += 1
            t_index += 1  # 跳到下一条

        # frequences_forward 频率超过阈值，很可能是NNS group 成员
        if max(frequences_forward) > 0:
            for i in range(Template_num):
                if frequences_forward[i] / len(i_indexes) >= thres2:
                    group_forward.append(i)

        # 前驱结点 is the most frequent items
        if max(frequences_backward) > 0:
            for i in range(Template_num):
                if frequences_backward[i] / len(i_indexes) >= thres2 / 2:
                    group_backward.append(i)

        NNS_F.append(group_forward)
        NNS_B.append(group_backward)

    # Compare NNS_F VS NNS_B, Modify NNS_F
    for i_NNS_index in range(len(NNS_F)):
        if NNS_F[i_NNS_index] == []:
            continue
        else:
            bef = i_NNS_index
            temp = list((u for u in NNS_F[i_NNS_index]))
            for lat in temp:
                if not bef in NNS_B[lat]:
                    NNS_F[i_NNS_index].remove(lat)
            if NNS_F[i_NNS_index] == []:
                NNS_F[i_NNS_index] = list((u for u in temp))
    return NNS_F
