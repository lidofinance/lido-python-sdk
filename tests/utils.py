from unittest import TestCase

import pytest

from web3 import Web3
from web3.middleware import geth_poa_middleware


class MockTestCase(TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, mocker):
        self.mocker = mocker


def get_mainnet_provider():
    return _get_web3_provider("mainnet")


def _get_web3_provider(net: str):
    w3 = Web3(Web3.HTTPProvider(f"https://{net}.infura.io/v3/b11919ed73094499a35d1b3fa338322a"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3
