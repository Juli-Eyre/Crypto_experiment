from pwn import *

c = ['9F0B13944841A832B2421B9EAF6D9836',
     '813EC9D944A5C8347A7CA69AA34D8DC0',
     'DF70E343C4000A2AE35874CE75E64C31']
r = remote('128.8.130.16', 49101)


# 发送并判断返回是否正确
def send_payload(build):
    msg = bytes.fromhex(build)
    lst = list(msg)
    lst.insert(0, 2)
    lst.append(0)
    r.send(bytes(lst))
    return r.recv(numb=2).decode()[0] == '1'


# 从最后一块开始破译 c[-x]
for x in range(1, len(c)):
    print("Detecting Block {}".format(x))
    block = c[-x]  # 当前分组
    prior_block = [int(i) for i in bytes.fromhex(c[-x - 1])]  # 前一分组

    iv = [0] * 16  # 初始向量
    Ivalue = []  # 中间值
    m = []  # 明文(hex)

    # 一个分组16B
    for i in range(1, 17):
        print(" round {}".format(i))

        # 修正
        l = len(Ivalue)
        iv = iv[:16 - l] + [x ^ i for x in Ivalue[::-1]]

        # 爆破vi[-i]
        for j in range(1, pow(2, 8)):
            iv[-i] = j
            build = ''.join([str(hex(i)[2:].zfill(2)) for i in iv]) + block
            if send_payload(build):
                break

        # 更新
        Ivalue.append(iv[-i] ^ i)
        m.append(Ivalue[-1] ^ prior_block[-i])
        print(" - IV     : {}".format(''.join([str(hex(i)[2:].zfill(2)) for i in iv])))
        print(" - Ivalue : {}".format(''.join([str(hex(i)[2:].zfill(2)) for i in Ivalue[::-1]])))
        print(" - m      : {}".format(''.join([str(hex(i)[2:].zfill(2)) for i in m[::-1]])))

    # print the message
    print(''.join(chr(i) for i in m[::-1]))