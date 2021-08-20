"""
Lido Python SDK
"""

from lido.operators import get_operators
from lido.constants.workers import MAX_WORKERS_FOR_OPERATORS, MAX_WORKERS_FOR_KEYS
from lido.constants.multicall import DEFAULT_MULTICALL_BATCH_OPERATORS, DEFAULT_MULTICALL_BATCH_KEYS
from lido.constants.addresses import get_default_lido_address, get_default_registry_address
from lido.constants.chains import EthChainIds
from lido.w3 import validate_web3
from typing import Optional
from web3 import Web3


class Lido:
    def __init__(
        self,
        w3: Web3,
        lido_address: Optional[str] = None,
        registry_address: Optional[str] = None,
        max_multicall_operators: Optional[int] = DEFAULT_MULTICALL_BATCH_OPERATORS,
        max_multicall_keys: Optional[int] = DEFAULT_MULTICALL_BATCH_KEYS,
        max_workers_operators: Optional[int] = MAX_WORKERS_FOR_OPERATORS,
        max_workers_keys: Optional[int] = MAX_WORKERS_FOR_KEYS,
    ) -> None:
        validate_web3(w3)

        chain = EthChainIds(w3.eth.chain_id)
        default_registry_address = get_default_registry_address(chain)
        default_lido_address = get_default_lido_address(chain)

        self.w3 = w3
        self.chain = chain
        self.max_multicall_operators = max_multicall_operators
        self.max_multicall_keys = max_multicall_keys
        self.max_workers_operators = max_workers_operators
        self.max_workers_keys = max_workers_keys
        self.registry_address = registry_address or default_registry_address
        self.lido_address = lido_address or default_lido_address

    def get_operators(self, start_index: int = 0, end_index: int = -1):
        return get_operators(
            self.w3,
            self.registry_address,
            start_index,
            end_index,
            self.max_multicall_operators,
            self.max_workers_operators
        )
