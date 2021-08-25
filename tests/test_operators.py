from lido.operator.operator import (
    get_operators_count,
    get_operators_data,
    get_operator_keys,
)
from tests.utils import get_mainnet_provider, get_ropsten_provider


def test_get_operators():
    w3 = get_mainnet_provider()
    operators_count = get_operators_count(w3)
    operators_data = get_operators_data(w3, operators_count)
    keys = get_operator_keys(w3, operators_data[0])

    assert len(keys) == operators_data[0]['totalSigningKeys']
