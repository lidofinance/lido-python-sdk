# Lido Python SDK

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/volpatto/blank-python-project/branch/master/graph/badge.svg)](https://github.com/lidofinance/lido-validator-python)

This repo provides a scratch of a Python project. Its purpose is to serve as starting point for
the development of a Python project based on a minimal working structure.

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

## Covered features

* [Sphinx](http://www.sphinx-doc.org/en/master/) autodocumentation with [autodoc](https://docs-python2readthedocs.readthedocs.io/en/master/code-doc.html);
* [GitHub Actions](https://github.com/features/actions) workflows with minimal configurations for latest Ubuntu, macOS and Windows;
* Tests with [pytest](https://docs.pytest.org/en/latest/);
* [virtualenv](https://virtualenv.pypa.io/en/latest/)
* Hierarchical structure to a python package as suggested by ["The Hitchhiker’s Guide to Python"](https://docs.python-guide.org/) (highly recommended reading);
* A [Read The Docs](https://readthedocs.org/) configuration scratch;
* Coverage of the package with [Codecov](https://codecov.io/).
