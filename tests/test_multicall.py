from unittest.mock import PropertyMock

from web3 import Web3

from tests.utils import MockTestCase, get_mainnet_provider
from lido_sdk import config


def _get_broken_endpoint_generator(retries_to_success):
    for i in range(retries_to_success):
        if i == retries_to_success - 1:
            yield (
                13146382,
                (
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r",
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r",
                ),
            )
        else:
            yield ValueError(
                {"code": -32000, "message": "execution aborted (timeout = 5s)"}
            )


class ValidationTest(MockTestCase):
    def setUp(self) -> None:
        self.mocker.patch(
            "web3.eth.Eth.chain_id", return_value=1, new_callable=PropertyMock
        )
        self.w3 = Web3()

    def test_multicall_params(self):
        exception_count = 5

        contract_multicall = self.mocker.patch(
            "multicall.Call.__call__",
            side_effect=_get_broken_endpoint_generator(exception_count),
        )
        self.mocker.patch(
            "web3.eth.Eth.chain_id", return_value=1, new_callable=PropertyMock
        )

        from lido_sdk.contract.load_contract import NodeOpsContract

        w3 = Web3()

        config.MULTICALL_MAX_RETRIES = 3

        with self.assertRaises(ValueError):
            NodeOpsContract.getNodeOperatorsCount_multicall(w3, [[], []])

        config.MULTICALL_MAX_RETRIES = 6

        NodeOpsContract.getNodeOperatorsCount_multicall(w3, [[], []])

        self.assertEqual(contract_multicall._mock_call_count, exception_count)
        self.assertEqual(2, len(contract_multicall.call_args[0][0][0]))
