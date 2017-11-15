# Function for MCTS_Main.py
# find count in Time Window ------ threshold1

import TimeGap


def FindCoutWindow(TimeList, threshold1):
    # 初始时间
    PreTime = TimeList[0]
    win_s = 0
    for i in range(1, len(TimeList)):
        LaterTime = TimeList[i]
        DeltaTime = TimeGap.Time_Gap(PreTime, LaterTime)
        if DeltaTime > threshold1:
            break
        else:
            win_s += 1
    return win_s
