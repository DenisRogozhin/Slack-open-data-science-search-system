import bitstring
import sys
sys.path.append('../../src/search_index')
import varbyte_encoding


def test_add_byte():
    bs = bitstring.BitStream()
    varbyte_encoding.add_byte(bs, 1)
    assert bs == '0b1'
    bs = bitstring.BitStream('0b010')
    varbyte_encoding.add_byte(bs, 0)
    assert bs == '0b0100'
    varbyte_encoding.add_byte(bs, 1)
    assert bs == '0b01001'


def test_compress():
    compressed_arr = '0b10000000010000001000000001000000'
    assert varbyte_encoding.compress([1, 3, 4, 6])\
        == bytes([int(compressed_arr[2:10], 2),
                  int(compressed_arr[10:18], 2),
                  int(compressed_arr[18:26], 2),
                  int(compressed_arr[26:34], 2)])
    assert varbyte_encoding.decompress(
        varbyte_encoding.compress([1000000])) == [1000000]
    assert varbyte_encoding.decompress(
        varbyte_encoding.compress([1, 3, 4, 6])) == [1, 3, 4, 6]
    assert varbyte_encoding.decompress(
        varbyte_encoding.compress([1, 100, 102, 217])) == [1, 100, 102, 217]
