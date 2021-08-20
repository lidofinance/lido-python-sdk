"""
Utilities for web3 integration
"""

from lido.constants.chains import EthChainIds
from web3 import Web3


def validate_web3(w3: Web3) -> None:
    assert isinstance(w3, Web3)

    chain_id = w3.eth.chain_id

    if chain_id == EthChainIds.GOERLI:
        from web3.middleware import geth_poa_middleware

        injected = geth_poa_middleware in w3.middleware_onion

        assert injected, "PoA middleware isn't injected into Web3 middleware onion"

    return None
