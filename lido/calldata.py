from typing import Callable, TypeVar, Dict, List, Any


T = TypeVar('T')


def get_call_data_setter(
    data: Dict[str, Any],
    field: str
) -> Callable[[T], Dict[str, T]]:
    def assignment(value: T):
        data[field] = value
        return data

    return assignment


def unzip_call_data(
    index: int,
    result_dict: Dict,
    result_dict_fields: List[str]
) -> list[tuple[int, Callable[[T], Dict[str, T]]]]:
    return [
        (index, get_call_data_setter(result_dict, field_name))
        for field_name in result_dict_fields
    ]
