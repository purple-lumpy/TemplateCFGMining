import re

# 正则化日志（序列中）
# OLD ------------ 2017.8.30 --------------------------------------------------------------------------------------------------------------
raw_file = open(
    "C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\ReqConnectedLogCreate.log")
filtered_file = open("C:\\Users\\ThinkPad\\Desktop\\test\\new_data\\newTemplate\\Closed\\createLog\\Regulared.txt",
                     "w+")
filtered_file.truncate()  # delete content

# r = '''\\[-\\]|-|:|,|>|.\d|\\n|\d|[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}|\\[req-[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}[\s\S]*\\]|\\[instance: [0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}\\]|[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}|/usr/[\s\S]*|[0-9]*\\.[0-9]*\\.[0-9]*\\.[0-9]|http://.*/.*/[\s\S]*id=|[0-9a-z]{40}|[0-9a-z]{32}|/var/.*'''

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
        filtered_file.write(c26)

raw_file.close()
filtered_file.close()
