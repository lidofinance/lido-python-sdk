from typing import Dict, List

from web3 import Web3

from lido.contract.load_contract import NodeOpsContract
from lido.operator.typing import Operator, OperatorKey


def get_operators_count(w3: Web3) -> int:
    """
    @param w3: Web3 instance
    @return: Node operators count
    """
    return NodeOpsContract.getNodeOperatorsCount(w3)['']


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
        operator['index'] = index

    return operators


def get_operator_keys(w3: Web3, operator: Operator) -> List[OperatorKey]:
    """
    @param w3: Web3 instance
    @param operator: Operator details from get_operators_data. But we need only `index` and `totalSigningKeys`
    @return: OperatorKey
    """
    keys = NodeOpsContract.getSigningKey_multicall(
        w3,
        [(operator['index'], index) for index in range(operator['totalSigningKeys'])],
    )

    # Add index to each key
    for index, key in enumerate(keys):
        key['index'] = index

    return keys
