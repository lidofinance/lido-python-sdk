from typing import List, Tuple

from web3 import Web3

from lido_sdk.contract.load_contract import NodeOpsContract
from lido_sdk.methods.typing import Operator, OperatorKey


def get_operators_indexes(w3: Web3) -> List[int]:
    """
    @param w3: Web3 instance
    @return: Node operators count
    """
    operators_count = NodeOpsContract.getNodeOperatorsCount(w3)[""]
    return [x for x in range(operators_count)]


def get_operators_data(w3: Web3, operators_index_list: List[int]) -> List[Operator]:
    """
    @param w3: Web3 instance
    @param operators_index_list: Operator's indexes to fetch
    @return: List of dictionary with operators details
    """
    if not operators_index_list:
        return []

    operators = NodeOpsContract.getNodeOperator_multicall(
        w3,
        [(i, True) for i in operators_index_list],
    )

    # Add index to each operator
    for index, operator in zip(operators_index_list, operators):
        operator["index"] = index

    return operators


def get_operators_keys(w3: Web3, operators: List[Operator]) -> List[OperatorKey]:
    """
    @param w3: Web3 instance
    @param operators: List of method's details from get_operators_data. But we need only `index` and `totalSigningKeys`.
    @return: List of dicts (OperatorKey)
    """
    args_list = []

    if len(operators) == 0:
        return []

    for args in _index_generator(operators):
        args_list.append(args)

    keys = NodeOpsContract.getSigningKey_multicall(w3, args_list)

    for key, (operator_index, key_index) in zip(keys, _index_generator(operators)):
        key["index"] = key_index
        key["operator_index"] = operator_index

    return keys


def _index_generator(operators):
    for operator in operators:
        for key_index in range(operator["totalSigningKeys"]):
            yield operator["index"], key_index


def get_keys_by_indexes(
    w3: Web3, call_args: List[Tuple[int, int]]
) -> List[OperatorKey]:
    """
    Via this method you can fetch list of keys by operator_index and key_index
    e.g. get_keys_by_index(w3, ((0, 0), (0, 1)) ) -> Will be fetched first two First operator's keys

    @param w3: Web3 instance
    @param call_args: List of operator_index and keys_index
    @return: List of dicts (OperatorKey)
    """
    if not call_args:
        return []

    keys = NodeOpsContract.getSigningKey_multicall(w3, call_args)

    for key, (operator_index, key_index) in zip(keys, call_args):
        key["index"] = key_index
        key["operator_index"] = operator_index

    return keys
