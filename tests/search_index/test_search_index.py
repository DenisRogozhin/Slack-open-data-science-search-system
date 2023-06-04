import bitstring
import sys
sys.path.append('src/search_index')
import varbyte_encoding
import query_processing


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


def test_tokenize():
    assert query_processing.tokenize('1 & 2 & 3') == ['1', '&', '2', '&', '3']
    assert query_processing.tokenize('(1 | 2) & (3 | 4)')\
        == ['(', '1', '|', '2', ')', '&', '(', '3', '|', '4', ')']
    assert query_processing.tokenize('((1 | 2) & 3) | 4')\
        == ['(', '(', '1', '|', '2', ')', '&', '3', ')', '|', '4']
    assert query_processing.tokenize('(!(1 | 2) & 3) | 4')\
        == ['(', '!', '(', '1', '|', '2', ')', '&', '3', ')', '|', '4']


def test_to_poliz():
    assert query_processing.tokenized_query_to_poliz(
        ['1', '&', '2', '&', '3']) == ['1', '2', '3', '&', '&']
    assert query_processing.tokenized_query_to_poliz(
        ['(', '1', '|', '2', ')', '&', '(', '3', '|', '4', ')'])\
        == ['1', '2', '|', '3', '4', '|', '&']
    assert query_processing.tokenized_query_to_poliz(
        ['(', '!', '(', '1', '|', '2', ')', '&', '3', ')', '|', '4'])\
        == ['1', '2', '|', '!', '3', '&', '4', '|']


def test_find_doc_ids():
    idx = {
        '1': [1, 2, 3, 4],
        '2': [1, 4, 5, 6],
        '3': [3, 4, 7, 8],
        '4': [7, 8, 9, 10]
    }
    all_docs = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    assert query_processing.find_doc_ids(
        ['1', '2', '3', '&', '&'], idx, all_docs) == {4}
    assert query_processing.find_doc_ids(
        ['1', '2', '|', '3', '4', '|', '&'], idx, all_docs) == {3, 4}
    assert query_processing.find_doc_ids(
        ['1', '2', '|', '!', '3', '&', '4', '|'], idx, all_docs)\
        == {7, 8, 9, 10}
