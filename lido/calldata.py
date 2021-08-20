"""
Utilities for processing the Call results
"""

from typing import Callable, TypeVar, Dict, List


A = TypeVar("A")
T = TypeVar("T")


def get_call_data_setter(
    result_dict: Dict[str, A], field: str
) -> Callable[[T], Dict[str, A]]:
    """Returns handler that assign input value to the result_dict[field]"""

    assert isinstance(result_dict, Dict)
    assert isinstance(field, str)

    def call_data_setter(value: T):
        result_dict[field] = value
        return result_dict

    return call_data_setter


def unzip_call_data(
    index: int, result_dict: Dict[str, A], result_dict_fields: List[str]
) -> list[tuple[int, Callable[[T], Dict[str, A]]]]:
    """Generates handlers for the Call which assign data to the result_dict"""

    assert index >= 0
    assert isinstance(result_dict, Dict)
    assert isinstance(result_dict_fields, List)

    return [
        (index, get_call_data_setter(result_dict, field_name))
        for field_name in result_dict_fields
    ]
