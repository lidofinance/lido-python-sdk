"""
Utilities for fetching a list of node operators from a registry
"""

from lido.chunks import chunks_multithread_execute, get_chunks, Chunk
from lido.constants.workers import MAX_WORKERS_FOR_OPERATORS
from lido.constants.multicall import DEFAULT_MULTICALL_BATCH_OPERATORS, GET_OPERATOR_INTERFACE
from lido.constants.contracts import get_registry_contract
from lido.calldata import unzip_call_data
from typing import TypedDict, List, Dict
from multicall import Call, Multicall
from web3 import Web3
from logging import getLogger


logger = getLogger(__name__)


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

    logger.info("Start fetching", extra={
        'action': 'fetch',
        'target': 'operators',
        'state': 'start',
        'start_index': start_index,
        'end_index': end_index
    })

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

    logger.info("End fetching", extra={
        'action': 'fetch',
        'target': 'operators',
        'state': 'end',
        'start_index': start_index,
        'end_index': end_index
    })

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

    logger.info("Chunk fetched", extra={
        'action': 'chunk',
        'target': 'operators',
        'state': 'success',
        'start_index': chunk.start_index,
        'end_index': chunk.end_index
    })

    operators_indexed = index_operators(operators).values()
    return operators_indexed


def index_operators(operators: Dict[int, Operator]) -> Dict[int, OperatorIndexed]:
    """Adds index to operator's dict"""

    assert isinstance(operators, Dict)

    return {
        operator_index: {'index': operator_index, **operator_data}
        for (operator_index, operator_data) in operators.items()
    }