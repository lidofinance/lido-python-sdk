from constants.chains import EthChainIds
from web3 import Web3


def validate_web3(w3: Web3) -> None:
    chain_id = w3.eth.chainId

    if chain_id == EthChainIds.GOERLI:
        from web3.middleware import geth_poa_middleware

        if geth_poa_middleware not in w3.middleware_onion:
            raise ValueError(
                "PoA middleware isn't injected into Web3 middleware onion"
            )

    return None
