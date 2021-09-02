# <img src="https://docs.lido.fi/img/logo.svg" alt="Lido" width="46"/> Lido Python SDK 

[![codecov](https://codecov.io/gh/lidofinance/lido-python-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/lidofinance/lido-python-sdk)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repo provides a scratch of a Python project. Its purpose is to serve as starting point for
the development of a Python project based on a minimal working structure.

## Installation
This library is available on PyPi:

```bash
pip install lido-sdk
```

## Fast start

1. Create Web3 provider. One of fast options to start is INFURA.
```python
from web3 import Web3
# 
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'))
```

2. Create Lido instance and provide web3 provider
```python
from lido_sdk import Lido

lido = Lido(w3)
```

3. Call one 
```python
response = lido.fetch_all_keys_and_validate()

if response['invalid_keys'] or response['duplicated_keys']:
    # This is not cool
    print('There is invalid or duplicated keys\n')
    print(response)
else:
    print('Everything is good!')
```

## Params for Lido
| Param name             | Default value | Description |
| -------------          | ---------     | ----------- |
| w3                     | required      | Web3 provider |
| MULTICALL_MAX_BUNCH    | 275           | Count of calls in one multicall (not recommended to increase) |
| MULTICALL_MAX_WORKERS  | 6             | Count of requests in parallel (not recommended to have more than 12) |
| MULTICALL_MAX_RETRIES  | 5             | Count of retries before exception will be raised |

Settings example if timeout exception was raised:
```python
Lido(w3=w3, MULTICALL_MAX_BUNCH=100, MULTICALL_MAX_WORKERS=3)
```

## Base methods
Everything you need is in Lido class.

- `Lido.get_operators_indexes(self) -> List[int]`  
Returns: Node operators indexes in contract.
```
>>> lido.get_operators_indexes()

[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
```

- `Lido.get_operators_data(self, operators_indexes: Optional[List[int]] = None) -> List[Operator]`  
Receives: List of operators indexes. If nothing provided will take previous return from `get_operators_indexes` method.  
Returns: List of operators details.  
```
>>> lido.get_operators_data([1])

[{'active': True, 'name': 'Certus One', 'rewardAddress': '0x8d689476eb446a1fb0065bffac32398ed7f89165', 'stakingLimit': 1000, 'stoppedValidators': 0, 'totalSigningKeys': 1000, 'usedSigningKeys': 1000, 'index': 1}]```
```

- `Lido.get_operators_keys(self, operators: Optional[List[Operator]] = None) -> List[OperatorKey]`
Receives: List of operators details. If nothing provided will take previous return from `get_operators_data` method.  
Returns: List of keys in contract.
```
>>> lido.get_operators_keys(operators_data)

[{'key': b'...', 'depositSignature': b'...', 'used': False, 'index': 6921, 'operator_index': 8}, ...]
```

- `Lido.validate_keys(self, keys: Optional[List[OperatorKey]] = None) -> List[OperatorKey]`  
Receives: List of keys to validate. If nothing provided will take previous return from `get_operators_keys` method.  
Returns: List of invalid keys.
```
>>> lido.validate_keys()

[{'key': b'...', 'depositSignature': b'...', 'used': False, 'index': 6521, 'operator_index': 5}]
```

- `Lido.find_duplicated_keys(self, keys: Optional[List[OperatorKey]] = None) -> List[Tuple[OperatorKey, OperatorKey]]`  
Receives: List of keys to compare. If nothing provided will take previous return from `get_operators_keys` method.  
Returns: List of same pairs keys.  
```
>>> lido.find_duplicated_keys()

[
    (
        {'key': b'abc...', 'index': 222, 'operator_index': 5, ...}, 
        {'key': b'abc...', 'index': 111, 'operator_index': 5, ...}
    )
]
```

- `Lido.get_status(self) -> dict`  
Returns dict with Lido current state.
```
>>> lido.get_status()

{
    'isStopped': False, 
    'totalPooledEther': 1045230979275869331637351, 
    'withdrawalCredentials': b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb9\xd7\x93Hx\xb4\xfb\x96\x10\xb3\xfe\x8a^D\x1e\x8f\xad~)?', 
    'bufferedEther': 76467538672788331637351, 
    'feeBasisPoints': 1000, 
    'treasuryFeeBasisPoints': 0, 
    'insuranceFeeBasisPoints': 5000, 
    'operatorsFeeBasisPoints': 5000, 
    'depositedValidators': 29800, 
    'beaconValidators': 29800, 
    'beaconBalance': 968763440603081000000000, 
    'last_block': 13110151, 
    'last_blocktime': 1630103538,
}
```

- `Lido.fetch_all_keys_and_validate(self) -> Dict[str, list]`  
Makes all steps below except `get_status`.  
Returns all invalid and duplicated keys.
```
>>> lido.fetch_all_keys_and_validate()

{
    'invalid_keys': [...],
    'duplicated_keys': [...],
}
```

## Main Features

### Multicall Function Calls

- Instead of making network requests one-by-one, this library combines many requests into one RPC call. It uses [banteg/multicall.py](https://github.com/banteg/multicall.py), a Python wrapper for [makerdao/multicall](https://github.com/makerdao/multicall).
- Fast validation system powered by [blst](https://github.com/supranational/blst)

### Automatic Testnet / Mainnet Switching

Depending on which network is configured in web3 object, a set of contracts will be used.
Available networks:
- Mainnet
- Görli
- Ropsten

## Development

Clone project:
```bash
git clone git@github.com:lidofinance/lido-python-sdk.git
cd lido-python-sdk
```
Create virtual env:
```bash
virtualenv .env --python=python3
source .env/bin/activate
```
Install all dependencies:
```bash
  pip install -r requirements.txt
  pip install -r requirements-dev.txt
```
Build blst locally (linux):
```bash
  cd blst/
  ./build.sh
  cd ..
  mkdir -p ./blst-lib/linux/
  cp ./blst/libblst.a           ./blst-lib/linux/
  cp ./blst/bindings/blst.h     ./blst-lib/
  cp ./blst/bindings/blst.hpp   ./blst-lib/
  cp ./blst/bindings/blst_aux.h ./blst-lib/
  python setup.py build_ext --inplace
```
Build blst locally (osx):
```bash
  cd blst/
  ./build.sh
  cd ..
  mkdir -p ./blst-lib/darwin/
  cp ./blst/libblst.a           ./blst-lib/darwin/
  cp ./blst/bindings/blst.h     ./blst-lib/
  cp ./blst/bindings/blst.hpp   ./blst-lib/
  cp ./blst/bindings/blst_aux.h ./blst-lib/
  python setup.py build_ext --inplace
```

## How to test
Simply run in project root directory:
```bash
pytest .
```
