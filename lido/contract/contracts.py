import json
import os
from enum import Enum

from web3 import Web3
from web3.contract import Contract


def _get_contract_abi(contract_name: str):
    script_dir = os.path.dirname(__file__)

    return json.load(
        open(
            os.path.join(script_dir, "abi", contract_name)
        )
    )


class ContractABI(Enum):
    LIDO = _get_contract_abi("abi/Lido.json")
    NODE_OPERATORS_REGISTRY = _get_contract_abi("abi/NodeOperatorsRegistry.json")


def load_contract(w3: Web3, address: str, contract_abi: str) -> Contract:
    return w3.eth.contract(address=address, abi=contract_abi)
