from lido.methods import (
    get_operators_count,
    get_operators_data,
    get_operators_keys,
    validate_keys,
    find_keys_duplicates,
)
from tests.utils import get_mainnet_provider


def test_get_operators():
    import time
    start = time.perf_counter()
    print(f'Start: {start - start:0.4f}')

    w3 = get_mainnet_provider()

    tick = time.perf_counter()
    print(f'Get mainnet: {start - tick:0.4f}')

    operators_count = get_operators_count(w3)

    tick = time.perf_counter()
    print(f'Get operators count: {start - tick:0.4f}')

    operators_data = get_operators_data(w3, operators_count)

    tick = time.perf_counter()
    print(f'Get operators data: {start - tick:0.4f}')

    keys = get_operators_keys(w3, operators_data)[:100]

    tick = time.perf_counter()
    print(f'Get keys: {start - tick:0.4f}')

    invalid_keys = validate_keys(w3, keys)

    tick = time.perf_counter()
    print(f'Validate keys: {start - tick:0.4f}')

    duplicates = find_keys_duplicates(keys)

    tick = time.perf_counter()
    print(f'Find duplicates keys: {start - tick:0.4f}')

    print(invalid_keys)

    # assert len(keys) == operators_data[0]["totalSigningKeys"]
