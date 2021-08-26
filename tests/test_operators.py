from lido.methods import (
    get_operators_count,
    get_operators_data,
    get_operators_keys,
    validate_keys,
    find_keys_duplicates,
)
from tests.utils import get_mainnet_provider


def test_get_operators():
    w3 = get_mainnet_provider()
    operators_count = get_operators_count(w3)
    operators_data = get_operators_data(w3, operators_count)
    keys = get_operators_keys(w3, operators_data)
    invalid_keys = validate_keys(w3, keys)
    duplicates = find_keys_duplicates(keys)

    # assert len(keys) == operators_data[0]["totalSigningKeys"]
