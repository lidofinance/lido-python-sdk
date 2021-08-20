from os.path import dirname, join
from typing import List, Dict
from json import load

ABI_DIR = join(dirname(__file__), "../abi")


def load_contract_abi(file_name: str) -> List[Dict]:
    """Load an ABI file for contract"""
    return load(open(join(ABI_DIR, file_name)))


def get_lido_abi_path() -> List[Dict]:
    """Load an ABI file for Lido contract"""
    return load_contract_abi("lido.json")


def get_registry_abi_path() -> List[Dict]:
    """Load an ABI file for Node Operators Registry contract"""
    return load_contract_abi("node-operators-registry.json")
