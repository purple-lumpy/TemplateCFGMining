# ******************************* find list all elements whose value is same with parameter ****************************

def findInList(big_List, value):
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
