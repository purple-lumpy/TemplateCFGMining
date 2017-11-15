import re

import Levenshtein

# 对原始日式进行模板匹配，返回日志序列对应的模板序列 id , 保存在 regular_id 的结构中
# 写入到 results.txt 文件中，未匹配到的日志，对应 id 为 -1

# 要进行匹配的原始日志
raw_file = open("C:\\Users\\ThinkPad\\Desktop\\test\\test\\Test\\creat.txt")
# 模板集合
template_path = "C:\\Users\\ThinkPad\\Desktop\\test\\test\\Train\\template\\raw_template.txt"
template_file = open(template_path)
# 模板id 序列
regular_list = []

r_g1 = '''[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}'''
r_time = '''[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+.[0-9]+ [0-9]+'''
r_req = '''\[req-.*?\]'''
r_inst = '''\[instance.*?\]'''
r_jk = '''<.*?>'''
r_bk = '''\[-\]|\[\]'''
r_sk = '''\(.*?\)'''
r_mk = '''\[.*?\]'''
r_path = '''/usr.*|http://.* '''
r_sy = '''".*"'''
r_m = '''-*[0-9]+:-*[0-9]+:-*[0-9]+'''
r_var = '''/var/.*'''
r_bbk = '''\{.*?\}'''
r_val = '''[0-9]+.[0-9]+s|[0-9]+ MB|[0-9]+.[0-9]+ MB|[0-9]+ GB|[0-9]+.[0-9]+ GB'''
r_date = '''date:.*GMT'''
r_someone1 = '''\|'''
r_someone2 = '''::|File ,'''
r_someone3 = '''/etc.*. '''
r_someone4 = '''[a-z0-9]{26,100}'''
r_someone5 = '''[0-9]+.[0-9]+.[0-9]+.[0-9]+'''
r_num = "[0-9]+|[0-9]+.[0-9]+"
r_space = ''' +'''
r_someone6 = "'.*?'"
r_someone7 = ",|:"
r_someone8 = "\(|\)|\[|\]|\{|\}|'"
r_someone9 = "\*+|=+"

while 1:
    lines = raw_file.readlines(100000)
    if not lines:
        break
    for line in lines:
        # 每一条原始日志，重新访问一次模板库
        template_file.close()
        template_file = open(template_path)
        # ----------------
        c = re.sub(r_time, "", line)
        c1 = re.sub(r_req, "ReqId", c)
        c2 = re.sub(r_inst, "InstsId", c1)
        c3 = re.sub(r_jk, "", c2)
        c4 = re.sub(r_bk, "", c3)
        c5 = re.sub(r_sk, "", c4)
        c6 = re.sub(r_mk, "", c5)
        c7 = re.sub(r_sy, "", c6)
        c8 = re.sub(r_m, "", c7)
        c9 = re.sub(r_g1, "", c8)
        c10 = re.sub(r_path, "", c9)
        c11 = re.sub(r_var, "", c10)
        c12 = re.sub(r_bbk, "", c11)
        c13 = re.sub(r_val, "", c12)
        c14 = re.sub(r_date, "", c13)
        c15 = re.sub(r_someone1, "", c14)
        c16 = re.sub(r_someone2, "", c15)
        c17 = re.sub(r_someone3, "", c16)
        c18 = re.sub(r_someone4, "", c17)
        c19 = re.sub(r_someone5, "", c18)
        c20 = re.sub(r_num, "", c19)
        c21 = re.sub(r_space, " ", c20)
        c22 = re.sub(r_someone6, "", c21)
        c23 = re.sub(r_someone7, " ", c22)
        c24 = re.sub(r_someone8, "", c23)
        c25 = re.sub(r_someone9, "", c24)
        c26 = re.sub(r_space, " ", c25)
        line_regular = c26
        index = 0
        # 计算与模板的编辑距离
        while 1:
            template = template_file.readline()
            if not template:
                regular_list.append(-1)
                break
            else:
                dis = Levenshtein.distance(line_regular, template)
                if (dis / len(line_regular)) <= 0.1:  # 与初略模板距离比较接近
                    regular_list.append(index)
                    break
                else:
                    index += 1

# 原始日志序列对应的模板号序列---------------------------
filtered_file = open("C:\\Users\\ThinkPad\\Desktop\\test\\test\\Test\\results.txt")
filtered_file.truncate()
for item in regular_list:
    filtered_file.write(str(item) + "\n")
filtered_file.close()

raw_file.close()
template_file.close()
