import re
import datetime

testdata = 'gps.log'

with open(testdata, 'r', encoding='utf-8') as fd:
    line1 = fd.readlines()[0]
    rs1 = re.match(r'(.*)(2019.*)', line1)
    s1 = datetime.datetime.strptime(rs1.group(2), '%Y|%m|%d|%H|%M|%S')
    s2 = s1
with open(testdata, 'r', encoding='utf-8') as fd:
    num, num1, repeat, dis2, dis3, dis4, disn = 0, 0, 0, 0, 0, 0, 0

    for line in fd:
        rs = re.match(r'(.*)(2019.*)', line)
        if rs is None:
            continue
        s = datetime.datetime.strptime(rs.group(2), '%Y|%m|%d|%H|%M|%S')
        delta = s1 - s
        num1 = num1 + 1
        discrepancy = 86400 - int(delta.seconds)
        if discrepancy != 86400:
            if discrepancy >= 3:
                num = num + 1
                print(line, end='')
                print(line1, end='')
                print("相差%d秒" % discrepancy)
                if discrepancy == 2:
                    dis2 = dis2 + 1
                if discrepancy == 3:
                    dis3 = dis3 + 1
                if discrepancy == 4:
                    dis4 = dis4 + 1
                if discrepancy > 4:
                    disn = disn + 1
            s1 = s
            line1 = line
    print("开始时间：" + str(s2))
    print("结束时间：" + str(s))
    print("数据总共%d条,异常数据总共%d条,异常数据占比%.4f%%" % (num1, num, (num / num1 * 100)))
    print("相差2秒的共{0}条，相差3秒的共{1}条，相差4秒的共{2}条,相差4秒以上共{3}条".format(dis2, dis3, dis4, disn))
