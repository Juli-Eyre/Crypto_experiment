from Crypto.Cipher import AES
from Crypto import Random
import re
prepend = b"comment1=cooking%20MCs;userdata="
append = b";comment2=%20like%20a%20pound%20of%20bacon"  # len==42
###long time ago的了

def pad(value, size):
    if len(value) % size == 0:
        return value
    padding = size - len(value) % size
    padValue = bytes([padding]) * padding
    return value + padValue


class InvalidPaddingError(Exception):
    """exception class for invalid PKCS#7 padding

    Args:
        Exception (class): inherits from the in-built `Exception` class
    """

    def __init__(self, paddedMsg, message="has invalid PKCS#7 padding."):
        self.paddedMsg = paddedMsg
        self.message = message
        super().__init__(self.message)

    def __repr__(self):
        return f"{ self.paddedMsg } { self.message }"


def valid_padding(paddedMsg, block_size):
    # if the length of the `paddedMsg` is not a multiple of `block_size`
    if len(paddedMsg) % block_size != 0:
        return False

    last_byte = paddedMsg[-1]

    # if the value of the last_byte is greater than or equal to block_size
    if last_byte >= block_size:
        return False

    padValue = bytes([last_byte]) * last_byte
    # if all the padding bytes are not the same
    if paddedMsg[-last_byte:] != padValue:
        return False

    # if, after removing the padding, the remaining characters are not all printable
    if not paddedMsg[:-last_byte].decode('ascii').isprintable():
        return False

    return True


def remove_padding(paddedMsg, block_size):
    """removes padding from `paddedMsg`, displays error-message if padding is invalid

    Args:
        paddedMsg (bytes): the message that is padded using PKCS#7 padding
        block_size (int): the block size that is obtained by said padding

    Raises:
        InvalidPaddingError: if the padding is invalid

    Returns:
        (byte): the message after removal of padding, if valid.
    """
    if not valid_padding(paddedMsg, block_size):
        raise InvalidPaddingError

    last_byte = paddedMsg[-1]
    unpadded = paddedMsg[:-last_byte]
    return unpadded


# this is the dictionary for replacements
QUOTE = {b';': b'%3B', b'=': b'%3D'}

KEY = Random.new().read(AES.block_size)
IV = bytes(AES.block_size)  # for simplicity just a bunch of 0's


def cbc_encrypt(input_text):
    """encrypts a the `input_text` using AES-128 in CBC mode,
    aftr replacing `:` with `%3B` and `=` with `%3D` in the `input_text`

    Args:
        input_text (byte): the input to encrypt

    Returns:
        byte: result of AES-128-CBC(prefix+input_text+suffix)
    """

    for key in QUOTE:
        input_text = re.sub(key, QUOTE[key], input_text)

    plaintext = prepend + input_text + append
    plaintext = pad(plaintext, AES.block_size)

    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    ciphertext = cipher.encrypt(plaintext)

    return ciphertext


def check(ciphertext):
    """checks if the `ciphertext` upon decryption has `;admin=true;` in it

    Args:
        ciphertext (bytes): the result of an AES-128-CBC encryption

    Returns:
        bool: True if the plain-text contains `;admin=true;`, False otherwise
    """

    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    plaintext = cipher.decrypt(ciphertext)
    print(f"Plaintext: { plaintext }")

    if b";admin=true;" in plaintext:
        return True

    return False


def test():
    """tests the injection of `;admin=true;` into the cipher-text
    """

    # send two blocks of just A's
    input_string = b'A' * AES.block_size * 2
    print(AES.block_size)  # 16
    ciphertext = cbc_encrypt(input_string)
    print(len(ciphertext))  # 112
    # replace first block of A's with the `required` plain-text
    required = pad(b";admin=true;", AES.block_size)
    # xor each byte of the required with each byte of second block i.e, with 'A'
    inject = bytes([r ^ ord('A') for r in required])  # one block of input
    print(len(inject))  # 16
    # extra = length of ciphertext - length of injected text - length of prefix
    # = one block of input + suffix
    extra = len(ciphertext) - len(inject) - len(prepend)
    # print(extra)
    # keep `inject` fill either side with 0's to match length with original ciphertext
    # xor with 0 does not change value
    # this replaces the first block of input with `required` while the rest is unchanged
    # 0*len(prefix)+infect(A^AES(A)^target)+0*len(suffix+padding)
    inject = bytes(2 * AES.block_size) + inject + bytes(extra)

    crafted = bytes([x ^ y for x, y in zip(ciphertext, inject)])

    if check(crafted):
        print("Admin Found")
    else:
        print("Admin Not Found")
if __name__ == "__main__":
    test()
