"""
Utilities for fetching a list of node operators from a registry
"""

from chunks import chunks_multithread_execute, get_chunks, Chunk
from constants.workers import MAX_WORKERS_FOR_OPERATORS
from constants.multicall import DEFAULT_MULTICALL_BATCH_OPERATORS, GET_OPERATOR_INTERFACE
from constants.contracts import get_registry_contract
from typing import TypedDict, List, Dict
from multicall import Call, Multicall
from calldata import unzip_call_data
from web3 import Web3


class Operator(TypedDict):
    active: bool
    name: str
    rewardAddress: str
    stakingLimit: int
    stoppedValidators: int
    totalSigningKeys: int
    usedSigningKeys: int


class OperatorIndexed(Operator):
    index: int


def get_operators(
    w3: Web3,
    registry_address: str,
    start_index: int = 0,
    end_index: int = -1,
    chunk_size: int = DEFAULT_MULTICALL_BATCH_OPERATORS,
    max_workers: int = MAX_WORKERS_FOR_OPERATORS
) -> List[OperatorIndexed]:
    """Returns node operators from registry"""

    registry_contract = get_registry_contract(w3, registry_address)
    total_operators = registry_contract.functions.getNodeOperatorsCount().call()
    end_index = (total_operators - 1) if end_index == -1 else end_index

    assert start_index <= total_operators
    assert end_index < total_operators

    chunks = get_chunks(start_index, end_index, chunk_size)
    operators = chunks_multithread_execute(
        max_workers,
        chunks,
        lambda chunk:
            lambda: get_operators_chunked(
                w3,
                registry_address,
                chunk
            )
    )

    return operators


def get_operators_chunked(
    w3: Web3,
    registry_address: str,
    chunk: Chunk
) -> List[OperatorIndexed]:
    """Returns node operators in the chunk range"""

    operators: Dict[int, Operator] = {index: {} for index in chunk}
    operator_fields = list(Operator.__annotations__.keys())

    Multicall([
        Call(
            registry_address,
            [GET_OPERATOR_INTERFACE, index, True],
            unzip_call_data(
                index,
                operators[index],
                operator_fields
            ), w3
        ) for index in chunk
    ], w3)()

    operators_indexed = index_operators(operators).values()
    return operators_indexed


def index_operators(operators: Dict[int, Operator]) -> Dict[int, OperatorIndexed]:
    """Adds index to operator's dict"""

    assert isinstance(operators, Dict)

    return {
        operator_index: {'index': operator_index, **operator_data}
        for (operator_index, operator_data) in operators.items()
    }
