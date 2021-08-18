# A generic blank Python project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://travis-ci.com/volpatto/blank-python-project.svg?branch=master)](https://travis-ci.com/volpatto/blank-python-project)
![](https://github.com/volpatto/blank-python-project/workflows/linux/badge.svg?branch=master)
![](https://github.com/volpatto/blank-python-project/workflows/osx/badge.svg?branch=master)
![](https://github.com/volpatto/blank-python-project/workflows/windows/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/volpatto/blank-python-project/branch/master/graph/badge.svg)](https://codecov.io/gh/volpatto/blank-python-project)
[![Documentation Status](https://readthedocs.org/projects/blank-python-project/badge/?version=latest)](https://blank-python-project.readthedocs.io/en/latest/?badge=latest)

This repo provides a scratch of a Python project. Its purpose is to serve as starting point for
the development of a Python project based on a minimal working structure.

## Covered features

* A preconfigured setup.py file following the suggestions from [here](https://github.com/kennethreitz/setup.py);
* [Sphinx](http://www.sphinx-doc.org/en/master/) autodocumentation with [autodoc](https://docs-python2readthedocs.readthedocs.io/en/master/code-doc.html);
* [Travis CI](https://travis-ci.com) minimal configuration;
* [GitHub Actions](https://github.com/features/actions) workflows with minimal configurations for latest Ubuntu, macOS and Windows;
* Tests with [pytest](https://docs.pytest.org/en/latest/);
* Development environment with two options:
    * The classic [virtualenv](https://virtualenv.pypa.io/en/latest/)
    * A [conda](https://conda.io/en/latest/) environment with [conda-devenv](https://github.com/ESSS/conda-devenv) extension
* Hierarchical structure to a python package as suggested by ["The Hitchhiker’s Guide to Python"](https://docs.python-guide.org/) (highly recommended reading);
* A [Read The Docs](https://readthedocs.org/) configuration scratch;
* [pre-commit](https://pre-commit.com/) to perform git hooks before commits. The following plugins are being used:
    - trailing-whitespace
    - end-of-file-fixer
    - black (default options combined with customized line length to 100 chars per line)
    - blacken-docs
* Coverage of the package with [Codecov](https://codecov.io/).

## Contributions

Contributions are VERY welcome. But please be aware of the purpose of the repo: **A minimal working structure.** If you want to add a feature which is very particular to your needs, please analyse if it fits the objective.

Suggestions and advices are welcome, feel free to open an Issue or send me an email.

## Contact

My name is Diego. Feel free to contact me through the email <volpatto@lncc.br>.
