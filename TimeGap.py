# 计算两个时间的时间间隔，单位是秒
import time


def Time_Gap(before, later):
    t_b = time.strptime(before, "%Y-%m-%d %H:%M:%S.%f")
    t_l = time.strptime(later, "%Y-%m-%d %H:%M:%S.%f")

    timeStamp_b = int(time.mktime(t_b))
    timeStamp_l = int(time.mktime(t_l))

    # 秒级时间差
    timeStamp = timeStamp_l - timeStamp_b
    # 毫秒部分
    b_ms = before.split(".")[1]
    l_ms = later.split(".")[1]
    int_b_ms = 0.0
    int_l_ms = 0.0
    exp_int_b_ms = -1
    exp_int_l_ms = -1
    for i in b_ms:
        int_b_ms += (10 ** (exp_int_b_ms)) * int(i)
        exp_int_b_ms -= 1
    for i in l_ms:
        int_l_ms += (10 ** (exp_int_l_ms)) * int(i)
        exp_int_l_ms -= 1

    delta_ms = int_l_ms - int_b_ms
    real_time_delta = timeStamp + delta_ms
    return round(real_time_delta, 3)
