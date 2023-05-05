import bitstring


def add_byte(bs, d):
    b = '0b1' if d == 1 else '0b0'
    bs.append(b)


def compress(id_list):
    bs = bitstring.BitStream()
    for i in range(len(id_list)):
        if i == 0:
            delta = id_list[i]
        else:
            delta = id_list[i] - id_list[i-1]
        rest_bits = 7

        while delta:
            add_byte(bs, delta & 1)
            delta >>= 1
            rest_bits -= 1

            if rest_bits == 0 and delta != 0:
                rest_bits = 7
                add_byte(bs, 1)

        while rest_bits != 0:
            add_byte(bs, 0)
            rest_bits -= 1
        add_byte(bs, 0)
    return bs.tobytes()


def decompress(id_bytes):
    id_list = []
    bs = bitstring.BitStream(id_bytes)

    pos = 0
    b_cnt = 0
    number = 0
    cum_sum = 0

    for b in bs:
        if b_cnt == 7:
            if not b:
                cum_sum += number
                id_list.append(cum_sum)
                pos = 0
                number = 0
            b_cnt = 0
            continue
        
        number += int(b) << pos
        pos += 1
        b_cnt += 1
    return id_list
