from enum import Enum, IntEnum


class EthChainIds(IntEnum):
    MAINNET = 1
    ROPSTEN = 3
    GOERLI = 5


class Eth2Chains(Enum):
    MAINNET = 'mainnet'
    PYRMONT = 'pyrmont'
    PRATER = 'prater'


def get_eth2_chain(eth_chain_id: int) -> Eth2Chains:
    # Mainnet-Mainnet deployment
    if eth_chain_id == EthChainIds.MAINNET:
        return Eth2Chains.MAINNET

    # Ropsten-Mainnet deployment
    if eth_chain_id == EthChainIds.ROPSTEN:
        return Eth2Chains.MAINNET

    # Goerli-Prater deployment
    if eth_chain_id == EthChainIds.GOERLI:
        return Eth2Chains.PRATER

    raise ValueError(f"Chain {eth_chain_id} is not supported")
