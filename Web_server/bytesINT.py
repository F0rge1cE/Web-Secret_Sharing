def bytes_to_int(a):
# Transform bytes to int
# Param:
#	a: given input -- bytes-like string
# Return: integer calculated by input 
    b = bytearray()
    b.extend(map(ord,a))
    # print (list(b))
    c = 0
    for num in b:
        c = (c << 8) + num
    # print(c)
    return c

def int_to_bytes(a, length):
# Transform bytes to int
# Param:
#	a: int -- could be very large
# Return: bytes-like string
    if a == 0:
        return ''.join([chr(a)] * length)

    b = []
    mask = 0xff

    while(length > 0):
        # print(b)
        b.append(chr(a & mask))
        a = a >> 8
        length -= 1
    return ''.join(b[::-1])


# '\x12\x00\x22' 1179682
# '\x00\xf4b\xfd' 16016125

# print(int_to_bytes(16016125, 4))
