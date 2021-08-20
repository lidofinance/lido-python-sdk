from pytest import raises, mark
from typing import Dict
from lido.operators import index_operators


"""Test arguments"""


@mark.parametrize("arg", [[], 1, None])
def test_index_operators_wrong_arguments(arg):
    with raises(AssertionError):
        index_operators(arg)


def test_index_operators_arguments():
    index_operators({})


"""Test output"""


def test_index_operators_output_instance():
    assert isinstance(index_operators({}), Dict)


def test_index_operators_output_data():
    test_dict = {'name': 'test'}
    output = index_operators({5: test_dict})

    assert len(output) == 1
    assert output[5] == {'index': 5, **test_dict}
