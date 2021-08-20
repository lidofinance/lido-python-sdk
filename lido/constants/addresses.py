from lido.constants.chains import EthChainIds
from typing import Dict


LIDO_ADDRESSES: Dict[EthChainIds, str] = {
    EthChainIds.MAINNET: "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
    EthChainIds.ROPSTEN: "0xd40EefCFaB888C9159a61221def03bF77773FC19",
    EthChainIds.GOERLI: "0x1643E812aE58766192Cf7D2Cf9567dF2C37e9B7F",
}

NODE_OPS_ADDRESSES: Dict[EthChainIds, str] = {
    EthChainIds.MAINNET: "0x55032650b14df07b85bF18A3a3eC8E0Af2e028d5",
    EthChainIds.ROPSTEN: "0x32c6f34F3920E8c0074241619c02be2fB722a68d",
    EthChainIds.GOERLI: "0x9D4AF1Ee19Dad8857db3a45B0374c81c8A1C6320",
}


def get_default_lido_address(chain: EthChainIds) -> str:
    """Return an appropriate Lido address for current network"""
    return LIDO_ADDRESSES[chain]


def get_default_registry_address(chain: EthChainIds) -> str:
    """Return an appropriate Node Operator (registry) address for current network"""
    return NODE_OPS_ADDRESSES[chain]
