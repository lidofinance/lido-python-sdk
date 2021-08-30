from typing import Dict, List
from unittest.mock import PropertyMock

from web3 import Web3

from lido.contract.contract import Contract
from lido.contract.load_contract import _get_contract_abi
from tests.utils import MockTestCase


class ContractTest(MockTestCase):
    def test_load_contract(self):
        from lido.contract.load_contract import LidoContract, NodeOpsContract

        lido_abi = _get_contract_abi("Lido.json")

        self._check_all_methods_exists(LidoContract, lido_abi)

        node_abi = _get_contract_abi("NodeOperatorsRegistry.json")
        self._check_all_methods_exists(NodeOpsContract, node_abi)

    def _check_all_methods_exists(self, contract: Contract, contract_abi: List[Dict]):
        for element in contract_abi:
            if element["type"] == "function":
                self.assertTrue(getattr(contract, element["name"], None))
                self.assertTrue(getattr(contract, element["name"] + "_multicall", None))

    def test_contract_call_function(self):
        call = self.mocker.patch(
            "lido.contract.execute_contract.execute_contract_call", return_value=2
        )
        contract_multicall = self.mocker.patch(
            "multicall.Call.__call__",
            return_value=(
                2,
                [
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r",
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\r",
                ],
            ),
        )
        self.mocker.patch(
            "web3.eth.Eth.chain_id", return_value=1, new_callable=PropertyMock
        )

        from lido.contract.load_contract import NodeOpsContract

        w3 = Web3()

        NodeOpsContract.getNodeOperatorsCount(w3)
        call.assert_called_once()

        NodeOpsContract.getNodeOperatorsCount_multicall(w3, [[], []])

        contract_multicall.assert_called_once()
        self.assertEquals(2, len(contract_multicall.call_args[0][0][0]))
