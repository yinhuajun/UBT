import re
import datetime

testdata = 'gps.log'
with open(testdata, 'r') as fd:
    num = 0
    num1 = 0
    repeat = 0
    for line in fd:
        rs = re.match(r'(.*)(2019.*)', line)
        s1 = datetime.datetime.strptime(rs.group(2), '%Y|%m|%d|%H|%M|%S')
        break
    for line in fd:
        rs = re.match(r'(.*)(2019.*)', line)
        if rs is None:
            continue
        s = datetime.datetime.strptime(rs.group(2), '%Y|%m|%d|%H|%M|%S')
        delta = s1 - s
        num1 = num1 + 1
        discrepancy = 86399 - int(delta.seconds)
        if discrepancy >= 2:

            if discrepancy == 86399:
                pass
                # print(line, end='')
                # print("重复数据")
                #  repeat=repeat+1
            else:
                num = num + 1
                print(line, end='')
                print(line1, end='')
                print("相差%d秒" % discrepancy)
        s1 = s
        line1 = line
    # print("数据总共%d条,异常数据总共%d条（重复数据%d条）,异常数据占比%.4f%%"%(num1,num,repeat,(num / num1 * 100)))
    print("数据总共%d条,异常数据总共%d条,异常数据占比%.4f%%" % (num1, num, (num / num1 * 100)))
