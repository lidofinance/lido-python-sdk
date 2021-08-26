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

## Main Features

### Multicall Function Calls

Instead of making network requests one-by-one, this library combines many requests into one RPC call. It uses [banteg/multicall.py](https://github.com/banteg/multicall.py), a Python wrapper for [makerdao/multicall](https://github.com/makerdao/multicall).

### Automatic Testnet / Mainnet Switching

Depending on which network is configured in web3 object, a set of contracts will be used.
Available networks:
- Mainnet
- Görli
- Ropsten

## Helpers Provided

- lido.get_operators_data() -> operator_data - load node operator data
- lido.get_operators_keys(operator_data) -> operator_data - fetches and adds keys to operator_data
- lido.validate_keys(operator_data, strict = False) -> [] - same as validate_keys_multi(), but returns a list of invalid keys  
(IN PROGRESS)
- lido.validate_key(chain_id, key, withdrawal_credentials) -> Boolean - low-level validation function, doesn't check for correct
  chain_id and withdrawal_credentials for a Lido deployment. For most use-cases use validate_keys_multi or validate_key_list_multi instead
- lido.find_duplicates(operator_data) -> operator_data - finds duplicate keys and adds results to operator_data

- lido.fetch_and_validate() -> operator_data - combines fetching operator data and running all validations on it - useful when you would be running all validations on data anyway

- lido.get_stats() -> stats - fetches various constants from Lido contract, but you can even pass a list of functions to fetch eg get_stats(["isStopped"])

You can mix and match these functions, but make sure to use get_operators_data() first.

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

## How to test
Simply run in project root directory:
```bash
pytest .
```
