#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform
import io
import os
import sys

from setuptools import find_packages, setup, Extension


if sys.version_info < (3, 7):
    raise Exception("Python 3.7 or higher is required")


# Package meta-data.
NAME = "lido-sdk"
DESCRIPTION = (
    "This library consolidates various functions to efficiently load network data for Lido,"
    " validate node operator keys and find key duplicates."
)
URL = "https://github.com/lidofinance/lido-python-sdk"
EMAIL = "info@lido.fi"
AUTHOR = "Lido"
REQUIRES_PYTHON = ">=3.7,<4"
VERSION = "2.2.2"

# Detecting target platform
PLATFORMS = {"windows", "linux", "darwin", "cygwin", "android"}

target = platform.system().lower()

if "pydroid3" in sys.executable.lower():
    target = "android"

for known in PLATFORMS:
    if target.startswith(known):
        target = known

if target not in PLATFORMS:
    target = "linux"

# C/C++ Extensions
LIBRARIES = []
STATIC_LIBRARIES = ["blst"]
STATIC_LIB_DIR = f"blst-lib/{target}"
LIBRARY_DIRS = ["blst-lib/"]
INCLUDE_DIRS = ["blst-lib/"]
SOURCES = [
    "blst-lib/blst_wrap.cpp",
]

DEPENDS = [
    "blst-lib/blst.h",
    "blst-lib/blst.hpp",
    "blst-lib/blst_aux.h",
    "blst-lib/libblst.a",
    "blst-lib/blstlib.dll",
]

LIBRARIES.extend(STATIC_LIBRARIES)
LIBRARY_DIRS.append(STATIC_LIB_DIR)

if target == "windows":
    EXTRA_OBJECTS = [
        "{}/{}.lib".format(STATIC_LIB_DIR, lib_name) for lib_name in STATIC_LIBRARIES
    ]
else:  # POSIX
    EXTRA_OBJECTS = [
        "{}/lib{}.a".format(STATIC_LIB_DIR, lib_name) for lib_name in STATIC_LIBRARIES
    ]

ext_modules = [
    Extension(
        "lido_sdk.blstverify._blst",
        sources=SOURCES,
        depends=DEPENDS,
        include_dirs=INCLUDE_DIRS,
        libraries=LIBRARIES,
        library_dirs=LIBRARY_DIRS,
        extra_objects=EXTRA_OBJECTS,
        py_limited_api=True,
    ),
]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


with open("requirements.txt", "r") as file:
    requirements = [lib.strip() for lib in file.read().split("\n") if lib]


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
    package_dir={"": "."},
    packages=find_packages(exclude=("tests",)),
    package_data={"lido_sdk.contract": ["abi/*.json"]},
    install_requires=requirements,
    tests_require=["pytest==6.2.4"],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        # How mature is this project? Common values are
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Supported Python versions
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    ext_modules=ext_modules,
    dependency_links=[],
)
