from typing import List

from web3 import Web3

from lido.contract.load_contract import NodeOpsContract
from lido.methods.typing import Operator, OperatorKey


def get_operators_count(w3: Web3) -> int:
    """
    @param w3: Web3 instance
    @return: Node operators count
    """
    return NodeOpsContract.getNodeOperatorsCount(w3)[""]


def get_operators_data(w3: Web3, operators_count: int) -> List[Operator]:
    """
    @param w3: Web3 instance
    @param operators_count: Operators count
    @return: List of dictionary with operators details
    """
    operators = NodeOpsContract.getNodeOperator_multicall(
        w3,
        [(i, True) for i in range(operators_count)],
    )

    # Add index to each operator
    for index, operator in enumerate(operators):
        operator["index"] = index

    return operators


def get_operators_keys(w3: Web3, operators: List[Operator]) -> List[OperatorKey]:
    """
    @param w3: Web3 instance
    @param operators: List of method's details from get_operators_data. But we need only `index` and `totalSigningKeys`.
    @return: List of dicts (OperatorKey)
    """
    args_list = []

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
