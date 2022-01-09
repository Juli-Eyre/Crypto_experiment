from gmpy2 import invert ,  is_prime , gcd , next_prime , iroot,powmod
from Crypto.Util.number import long_to_bytes
from functools import reduce
n = []
e = []
c = []
# m = [' ']*21 #存储明文，初始化
m={}
solved = []

##中国剩余定理
def chinese_remainder_theorem(mi, ai):
    M = reduce(lambda x, y: x * y, mi)
    ai_ti_Mi = [a * (M // m) * invert(M // m, m) for (m, a) in zip(mi, ai)]
    return reduce(lambda x, y: x + y, ai_ti_Mi) % M

##低加密指数攻击
#e=3得到的结果没意义
def small_e_attack(nlist , clist,e=5 ):
    m = chinese_remainder_theorem(nlist , clist)
    tmp = iroot(m , e)
    if tmp[1] == 1:
        return tmp[0]
    return 0

##共模攻击
def same_module_attack(N , e1 , e2 , c1 , c2):
    ##e1*x+e2*y=1
    x = invert(e1 , e2)
    y = (x * e1 - 1) // e2
    true_c2 = invert(c2 , N)
    return (powmod(c1 , x , N) * powmod(true_c2 ,y , N)) % N

def fermat(n):
    x = iroot(n, 2)[0]
    for _ in range(20000):
        x += 1
        if iroot(x ** 2 - n, 2)[1] == 1:
            y = iroot(x ** 2 - n, 2)[0]
            p = (x + y)
            q = (x - y)
            return p,q


def Pollard_p_1(N):
    a = 2
    g = a
    ##当n太大时，就 变化g，降低复杂度
    while 1:
        for n in range(1,200000):
            g = powmod(g, n, N)
            if is_prime(n):
                d = gcd(g-1, N)
                if 1 < d < N:
                    return d, N//d
                elif d >= N:
                    g = next_prime(a)
                    break
        else:
            break

##因数碰撞法
def yinshupz():
    for i in range(21):
        for j in range(21):
            if i != j:
                if 1 < gcd(n[i] , n[j]) < n[i]:
                    p = gcd(n[i] , n[j])
                    q1 = n[i] // p
                    q2 = n[j] // p
                    tmp1 = get_plain(RSA_std(p , q1 , e[i],c[i]))
                    tmp2 = get_plain(RSA_std(p , q2 , e[j],c[j]))
                    if tmp1 ==1:
                        solved.append(i)
                    if tmp2 == 1:
                        solved.append(j)


##由p q求d m
def RSA_std(p , q , e , c):
    phi = (p-1)*(q-1)
    d = invert(e , phi)
    m = powmod(c , d , p*q)
    return m

def get_plain(mm):
    tmp = hex(mm)[2:]
    number = int(tmp[16:24],16)
    plain = long_to_bytes(int(tmp[-16:] , 16))
    m[number] = plain
    return 1

def crack_PRG(n):
    a = 365
    b = -1
    m = pow(2,16)
    # j: RandSeed
    for j in range(m):
        x = j
        p = bin(x)[2:].zfill(16)
        for _ in range(63):
            y = (a*x+b)%m
            x = y
            p += bin(x)[2:].zfill(16)
            if n%int(p,2) == 0:
                return int(p,2)

def same_module():
    for i in range(21):
        for j in range(21):
            if i != j and n[i] == n[j] and e[i] != e[j]:#Same modulus found!
                tmp = get_plain(same_module_attack(n[i] , e[i],e[j],c[i],c[j]))
                if tmp == 1:
                    solved.append(i)
                    solved.append(j)

def pollard_resolve():
    for i in range(21):
        if i not in solved:
            tmp = Pollard_p_1(n[i])
            if isinstance(tmp , tuple):
                p , q = tmp
                if get_plain(RSA_std(p,q,e[i],c[i])):
                    solved.append(i)



def fermat_resolve():
    for i in range(21):
        if i not in solved:
            tmp=fermat(n[i])##成功返回
            if isinstance(tmp, tuple):
                p, q = tmp
                if get_plain(RSA_std(p, q, e[i], c[i])):
                    solved.append(i)

def small_e():
   # e = 5
    frame = [3,8,12,16,20]#Frame 3 8 12 16 20的指数都是5
    nlist = [n[i] for i in frame]
    clist = [c[i] for i in frame]
    m = small_e_attack(nlist , clist)
    if get_plain(m):
        for i in frame:
            solved.append(i)



name = ['./cipher_frame/Frame' + str(i) for i in range(21)]
for i in range(21):
    f = open(name[i] , 'r')
    data = f.read()
    tn , te , tc = int(data[:256] , 16) , int(data[256:512] , 16) , int(data[512:] , 16)
    n.append(tn)
    e.append(te)
    c.append(tc)


same_module()#共模攻击
yinshupz()#因数碰撞
pollard_resolve()#pollard p-1
fermat_resolve()#费马分解
small_e()#低指数加密攻击


#coppersmith攻击的结果，见.sage文件
m[2] = b'amous sa'
m[3] = b'ying of '
m[4] = b'Albert E'


plain = b''
print(m)
for i in range(21):
    if i in m :
        plain += m[i]
    else:
        plain += b' '*8
print(plain)

