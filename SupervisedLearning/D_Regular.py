import re

# 正则化日志（序列中）
# ------------- NEW  2017.9.18  -------------------------------------------------------------------------------

raw_file = open("C:\\Users\\ThinkPad\\t800\\SortedLog.log")
filtered_file = open("F:\\Anomoly_workflow_templates\\PreProcessedData\\Regulared.txt", "w+")
filtered_file.truncate()  # delete content
ReqId_file = open("F:\\Anomoly_workflow_templates\\PreProcessedData\\ReqId.txt", "w+")
ReqId_file.truncate()  # delete content

r_time = '''[0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+.[0-9]+ [0-9]+? '''
r_req = '''\[req-.*?\]'''
r_inst = '''\[instance.*?\]'''
r_jk = "<[^<>]*>"  # r_jk = '''<.*?>'''
r_sk = "\([^()]*\)"  # r_sk = '''\(.*?\)'''
r_mk = "\[[^\[\]]*\]"  # r_mk = '''\[.*?\]'''
r_bbk = "\{[^{}]*\}"  # r_bbk = '''\{.*?\}'''
r_http = "http:.*? "
r_path = '''/usr.*\.py:[0-9]+'''
r_g = "/?[0-9a-z]+/[0-9a-z/\-_]+"
r_someone1 = "'.*?'"
r_someone2 = "`.*?'"
r_someone3 = '''".*?"'''
r_someone4 = "`.*?`"
r_date = '''date:.*GMT'''
r_long = "[0-9a-zA-Z\-]{26,100}"
r_num1 = "[0-9]+.[0-9]+"
r_num2 = "[0-9]+"
r_equal = "=.*? "
r_someone5 = "\-[a-zA-Z]"
r_someone6 = "[\s]{1}\.|[\s]{1}-|:|MB|GB|,|;|\|"
r_space = ''' +'''

while 1:
    lines = raw_file.readlines(100000)
    if not lines:
        break
    for line in lines:
        c = re.sub(r_time, "", line)
        c1 = re.sub(r_req, "ReqId", c)
        c2 = re.sub(r_inst, "InstsId", c1)
        c3 = re.sub(r_jk, "", c2)
        while not c3 == re.sub(r_jk, "", c3):
            c3 = re.sub(r_jk, "", c3)
        c4 = re.sub(r_sk, "", c3)
        while not c4 == re.sub(r_sk, "", c4):
            c4 = re.sub(r_sk, "", c4)
        c5 = re.sub(r_mk, "", c4)
        while not c5 == re.sub(r_mk, "", c5):
            c5 = re.sub(r_mk, "", c5)
        c6 = re.sub(r_bbk, "", c5)
        while not c6 == re.sub(r_bbk, "", c6):
            c6 = re.sub(r_bbk, "", c6)
        c7 = re.sub(r_http, "", c6)
        c8 = re.sub(r_path, "", c7)
        c9 = re.sub(r_g, "", c8)
        c10 = re.sub(r_someone1, "", c9)
        c11 = re.sub(r_someone2, "", c10)
        c12 = re.sub(r_someone3, "", c11)
        c13 = re.sub(r_someone4, "", c12)
        c14 = re.sub(r_date, "", c13)
        c15 = re.sub(r_long, "", c14)
        c16 = re.sub(r_num1, "", c15)
        c17 = re.sub(r_num2, "", c16)
        c18 = re.sub(r_equal, "= ", c17)
        c19 = re.sub(r_someone5, "", c18)
        c20 = re.sub(r_someone6, "", c19)
        c21 = re.sub(r_space, " ", c20)

        filtered_file.write(c21)

        # 提取req ID
        ccc = re.findall(r"req-(.+?) ", line)[0]
        ReqId_file.write('req-' + ccc + '\n')
raw_file.close()
filtered_file.close()
