#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform
import io
import os
import sys

from setuptools import find_packages, setup, Extension

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

if platform.processor() in ["arm", "aarch64"]:
    target = "aarch64"

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
        extra_compile_args=["-std=c++11"],
    ),
]

# ---------------- setup --------------------

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

# Where the magic happens:
setup(
    name="lido-sdk",
    version="2.6.0",
    description="This library consolidates various functions to efficiently load network data for Lido,"
                " validate node  operator keys and find key duplicates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lido",
    author_email="info@lido.fi",
    python_requires=">=3.7,<4",
    url="https://github.com/lidofinance/lido-python-sdk",
    package_dir={"": "."},
    packages=find_packages(exclude=("tests",)),
    package_data={"lido_sdk.contract": ["abi/*.json"]},
    install_requires=[
        "multicall>=0.1.2,<0.5.0",
        "web3>=5.23.1,<6",
        "ssz>=0.2.4,<1",
    ],
    tests_require=["pytest==6.2.4"],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        # Supported Python versions
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    ext_modules=ext_modules,
    dependency_links=[],
)
