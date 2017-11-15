# 模N 位置，内容不变的list 的判断

def SameCycle(base, test):
    # 长度不等
    if not len(base) == len(test):
        return False
    S_b = set(base)
    S_t = set(test)
    # 内容不等
    if not S_b == S_t:
        return False
    # 序列 + 内容 不等
    first_base = base[0]
    first_base_in_test = test.index(first_base)
    for index in range(len(base)):
        if not base[index] == test[(index + first_base_in_test) % len(base)]:
            return False

    return True
