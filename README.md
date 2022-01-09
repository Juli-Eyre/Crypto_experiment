# crypto_experiment
## RSA大礼包

### 题目描述

已知帧数据的数据格式如下，其中数据都是16进制表示，结构如下：1024bit模数N | 1024bit加密指数e | 1024bit密文c。请给出原文和参数，如不能请给出已恢复部分并说明剩余部分不能恢复的理由？

### 攻击原理

1. 低指数加密攻击
   若有几组密文是由同一明文、同一加密密钥加密得到，则 利用中国剩余定理，然后开e次方即可还原明文

3. 共模攻击

   若有几组密文在加密时使用了相同的模数，则可用扩展欧几里德算法还原明文：

   由$gcd(e_1,e_2)=1$,得

   ​									$$e_1*x+e_2*y=1$$

   ​									$$c_1^xc_2^y \equiv (m_1^{e_1})^x(m_2^{e_2})^y \equiv (m^{e_1})^x(m^{e_2})^y \equiv m(mod N)$$

   

3. 因数碰撞法

   若p或q在不同组的加密中出现多次，则生成的不同模数n可能有相同的因子。这里，以p同，q不同为例：

   ​														$$ \left\{ \begin{aligned} n_1 & = p*q_1 \\ n_2 & = p*q_2 \\ \end{aligned} \right. $$

   再利用$gcd(n_1,n_2)=p$即可

   

4.  费马分解法

   若p和q相差不大：

   $$n=p*q=\frac {1} {4}(p+q)^2-\frac {1} {4}(p-q)^2=x^2-y^2=(x-y)(x+y)$$

   由p和q相差不大，忽略p-q，可以从$x=\sqrt {n}$遍历，计算$x^2-n$，当其为完全平方数时，即可求出x,y，$p=x+y,q=x-y$
   
   

5. Pollard  p-1 分解法

   设大整数的一个因子是p, p-1的所有素因子都不大于B，合适的选取B使得$(p-1)|B!$，则由欧拉定理知道：

   ​	$$g^{B!}\equiv1(mod p)$$

   ​	$$p|((g^{B!}mod n)-1)$$
   ​		$$gcd(g^{B!}-1,n)$$就是n的一个因子

6. coppersmith攻击(已知m的高位)

   设明文 m 的高位为 m0，当e比较小时，有：

   $$c\equiv(m_0+x)^e (mod n)$$

   设多项式$f(x)=(m+x)^e-c$，有$f(x)=k*n,(k=0,1,2...)$，遍历得到x后，依据[coppersmith定理](https://paper.seebug.org/727/#41-coppersmith),可以求出剩下的所有明文部分

   可借助本地sage环境或[sage在线运行](https://sagecell.sagemath.org/)

