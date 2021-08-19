from constants.abi import get_lido_abi_path, get_registry_abi_path
from web3 import Web3
from web3.contract import Contract


def get_lido_contract(w3: Web3, lido_address: str) -> Contract:
    lido_abi = get_lido_abi_path()
    return w3.eth.contract(lido_address, abi=lido_abi)


def get_registry_contract(w3: Web3, registry_address: str) -> Contract:
    registry_abi = get_registry_abi_path()
    return w3.eth.contract(registry_address, abi=registry_abi)
