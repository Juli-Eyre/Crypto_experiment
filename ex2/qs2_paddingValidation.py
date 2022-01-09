def valid_padding(paddedMsg, block_size):
    if len(paddedMsg) % block_size != 0:
        return False
    last_byte = paddedMsg[-1]
    if last_byte >= block_size:
        return False
    padValue = bytes([last_byte]) * last_byte
    if paddedMsg[-last_byte:] != padValue:
        return False
    if not paddedMsg[:-last_byte].decode('ascii').isprintable():
        return False

    return True


def PKCS7_restore(m):
    return m[:-m[-1]]


def test(m, size):
    try:
        if not valid_padding(m, size):
            raise ValueError
    except ValueError:
        print(f"{m} has invaild PKCS#7 padding.")
        return

    print(f"Padding successfully...")
    print(f"Before padding removal: { m }")
    print(f"After padding removal: { PKCS7_restore(m) }")
