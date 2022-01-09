import base64
## So we can use XOR for each pair of bytes, count the 1 bits and the result is the Hamming Distance.
def hamm (s1, s2):
    tot = 0
    for a,b in zip(s1,s2):
        tot += (bin(a^b).count('1'))
    #print('test Hamming distance is: ', tot)
    return(tot)
#print(hamm(b'this is a test',b'wokka wokka!!!'))
def find_key_len(c):
    aver_hamm=[]
    for keylen in range(2,41):
        #将密文分组
        tmp_aver_hamm=[]
        test1 = c
        while len(test1) >= (2 * keylen):
            x = test1[:keylen]
            y = test1[keylen:(2 * keylen)]
            # take the hamming distance and normalize by keysize
            score = hamm(x, y) / keylen
            test1 = test1[ keylen:]
            tmp_aver_hamm.append(score)
            res={
            'keylength': keylen,
            'avg distance': sum(tmp_aver_hamm)/len(tmp_aver_hamm)
            }
            aver_hamm.append(res)
            possible_key_length = sorted(aver_hamm, key=lambda x: x['avg distance'])[0]
    return possible_key_length['keylength']

##按照同一密钥进行分组c[::keylen]
##每个就转化成了 single_key_XOR: 根据字母出现的频率得到分数最高的
def get_english_score(input_bytes):
    """Compares each input byte to a character frequency
    chart and returns the score of a message based on the
    relative frequency the characters occur in the English
    language
    """

    # From https://en.wikipedia.org/wiki/Letter_frequency
    # with the exception of ' ', which I estimated.
    character_frequencies = {
    'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
    'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
    'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
    'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
    'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
    'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
    'y': .01974, 'z': .00074, ' ': .13000
    }
    return sum([character_frequencies.get(chr(byte), 0) for byte in input_bytes.lower()])

def repeat_key_xor(m,key):
    output_bytes=b''
    index=0
    for byte in m:#直接就是对应的ASCII
        #print(byte)
        #print(key[index])
        output_bytes+=bytes([byte^key[index]])
        #bytes[116,112]转为b'tp'
        if(index+1)==len(key):
            index=0
        else:
            index+=1
    return output_bytes

def single_char_xor(input_bytes, char_value):
    """Returns the result of each byte being XOR'd with a single value.
    """
    output_bytes = b''
    for byte in input_bytes:
        output_bytes += bytes([byte ^ char_value])
    return output_bytes

def bruteforce_single_char_xor(ciphertext):
    """Performs a singlechar xor for each possible value(0,255), and
    assigns a score based on character frequency. Returns the result
    with the highest score.
    """
    potential_messages = []
    for key_value in range(256):
        message = single_char_xor(ciphertext, key_value)
        score = get_english_score(message)
        data = {
        'message': message,
        'score': score,
        'key': key_value
        }
        potential_messages.append(data)
    return sorted(potential_messages, key=lambda x: x['score'], reverse=True)[0]['key']#最大的

cipher=open('ex1.4.txt').read().replace('\n','')
# convert to bytes
cipher=base64.b64decode(cipher)
keylen=find_key_len(cipher)
print(keylen)
#分组
key=[]
for index in range(keylen):
    sub_cipher=cipher[index::keylen]
    ## single_key_XOR:
    key.append(bruteforce_single_char_xor(sub_cipher))
print(''.join(chr(i) for i in key))
print(repeat_key_xor(cipher,bytes(''.join(chr(i) for i in key),encoding='utf8')))

