import logging
import time
from unittest.mock import PropertyMock

from web3 import Web3

from lido_sdk.methods import validate_keys
from tests.fixtures import OPERATORS_KEYS
from tests.utils import MockTestCase


class ValidationTest(MockTestCase):
    def setUp(self) -> None:
        self.mocker.patch(
            "web3.eth.Eth.chain_id", return_value=1, new_callable=PropertyMock
        )
        self.w3 = Web3()

        self.mocker.patch(
            "lido_sdk.contract.load_contract.LidoContract.getWithdrawalCredentials",
            return_value={
                "": b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb9\xd7\x93Hx\xb5\xfb\x96\x10\xb3\xfe\x8a^D\x1e\x8f\xad~)?"
            },
        )

        self.logger = logging.Logger("tests")

    def test_validation_performance(self):
        keys = OPERATORS_KEYS * 2000  # 10.000 keys

        t0 = time.time()
        validate_keys(self.w3, keys, True)
        t1 = time.time()

        total = t1 - t0

        self.assertGreater(22, total)

    def test_strict_validation_performance(self):
        keys = OPERATORS_KEYS * 2000  # 10.000 keys

        t0 = time.time()
        validate_keys(self.w3, keys, False)
        t1 = time.time()

        total = t1 - t0

        self.assertGreater(42, total)
