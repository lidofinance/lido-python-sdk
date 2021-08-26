#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command


# Package meta-data.
NAME = "lido-sdk"
DESCRIPTION = (
    "This library consolidates various functions to efficiently load network data for Lido,"
    " validate node operator keys and find key duplicates."
)
URL = "https://github.com/lidofinance/lido-validator-python"
EMAIL = "info@lido.fi"
AUTHOR = "Lido"
REQUIRES_PYTHON = ">=3.7,<4"
VERSION = "0.2.3"

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


class UploadCommand(Command):
    """
    Support setup.py upload.
        Note: To use the 'upload' functionality of this file, you must:
        $ pip install twine
    """

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(VERSION))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    # If your package is a single module, use this instead of "packages":
    # py_modules=["mypackage"],
    # entry_points={
    #     "console_scripts": ["mycli=mymodule:cli"],
    # },
    install_requires=[
        "multicall==0.1.2",
        "web3==5.23.0",
        "blspy==1.0.5",
        "eth2deposit==1.2.0",
        "ssz==0.2.4",
    ],
    tests_require=["pytest==6.2.4"],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
    dependency_links=[
        "https://github.com/ethereum/eth2.0-deposit-cli/tarball/v1.2.0#egg=eth2deposit-1.2.0",
    ],
)
