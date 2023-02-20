from wiki_infobox_parser import write_to_file
import pytest


def create_result(test_data):
    for i in test_data:
        write_to_file(i, 'test_tmp_file.txt')

    with open('test_tmp_file.txt', 'r') as f:
        result = f.readlines()
    return result


@pytest.mark.parametrize('test_data', (["Test text\n", "Test test test\n", "Test text 2\n", "Test 2 text"],
                                       ["12345\n", "5555\n", "6666\n", "88888"],
                                       ["value\n", "value2\n", "value3\n", "value4"]))
def test_write_to_file(test_data):
    assert test_data == create_result(test_data)

