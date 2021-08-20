from lido.w3 import validate_web3
from web3 import Web3, EthereumTesterProvider
from eth_tester import EthereumTester, MockBackend


def test_validate_web3():
    w3 = Web3(EthereumTesterProvider(EthereumTester(backend=MockBackend())))
    validate_web3(w3)
