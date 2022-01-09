import hashlib
import itertools
import datetime
starttime = datetime.datetime.now()
hash1="67ae1a64661ac8b4494666f58c4822408dd0a3e4"
str1="QqWw%58(=0Ii*+nN"
str2=[['Q', 'q'],[ 'W', 'w'],[ '%', '5'], ['8', '('],[ '=', '0'], ['I', 'i'], ['*', '+'], ['n', 'N']]
##str2是用来交换的，比如 Qxxx xxxx xxxx都不对，就换成q xxxxxxxxx 时间复杂度为0()由于需要在10s之内求解，
str4=""
str3=[0]*8
#首先要知道密码有多少位吧。。咋确定就是8位呢
for a in range(0,2):
    str3[0]=str2[0][a]
    for b in range(0,2):
        str3[1]=str2[1][b]
        for c in range(0,2):
            str3[2]=str2[2][c]
            for d in range(0,2):
               str3[3] = str2[3][d]
               for e in range(0,2):
                   str3[4] = str2[4][e]
                   for f in range(0,2):
                       str3[5] = str2[5][f]
                       for g in range(0,2):
                           str3[6] = str2[6][g]
                           for h in range(0,2):
                               str3[7] = str2[7][h]
                               newS="".join(str3)
                               for i in itertools.permutations(newS, 8):#返回可迭代对象的所有数学全排列方式。
                                   str4 =hashlib.sha1("".join(i).encode("utf-8")).hexdigest()
                                   if str4==hash1:
                                       print("".join(i))
                                       endtime = datetime.datetime.now()
                                       print(f"运行时间是：{(endtime - starttime).seconds}s")
