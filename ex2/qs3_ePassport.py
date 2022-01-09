from Crypto.Cipher import AES
import binascii
import hashlib
import base64
import codecs


def get_unkown_digit():
    a = [1, 1, 1, 1, 1, 6]
    b = [7, 3, 1, 7, 3, 1]
    c = 0
    for i in range(6):
        c += a[i] * b[i]
        res = c % 10
    return res


# 奇偶校验位的判断
def jiaoyan(x):
    k = []
    a = bin(int(x, 16))[2:]
    for i in range(0, len(a), 8):
        if (a[i:i + 7].count("1")) % 2 == 0:
            k.append(a[i:i + 7])
            k.append('1')
        else:
            k.append(a[i:i + 7])
            k.append('0')
    a1 = hex(int(''.join(k), 2))
    # print("this is " + x + "---" +a1)
    return a1[2:]


s = '123456788111018211111674'
K_seed = hashlib.new("sha1", s.encode("utf8")).hexdigest()[:32]

c = '00000001'
# 0x00000001
d = K_seed + c
print(d)
H_d = hashlib.sha1(codecs.decode(d, "hex")).hexdigest()
# 十六进制先变为二进制散列再换成十六进制
# print(H_d)
ka = hashlib.sha1(codecs.decode(d, "hex")).hexdigest()[:16]
kb = hashlib.sha1(codecs.decode(d, "hex")).hexdigest()[16:32]

k_1 = jiaoyan(ka)
k_2 = jiaoyan(kb)
key = k_1 + k_2
print(key)
# ea8645d97ff725a898942aa280c43179
IV = bytes(AES.block_size)
print(IV)
cipher = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
cipher = base64.b64decode(cipher)
print(cipher)
# returns the binary string that is represented by any hexadecimal string
m = AES.new(binascii.unhexlify(key), AES.MODE_CBC, IV)
# m = AES.new(key.encode(), AES.MODE_CBC, IV.encode())
print(m.decrypt(cipher))
# b'Herzlichen Glueckwunsch. Sie haben die Nuss geknackt. Das Codewort lautet: Kryptographie!\x01\x00\x00\x00\x00\x00\x00'
