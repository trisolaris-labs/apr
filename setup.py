#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup  # type: ignore

extras_require = {
    "types": ["types-requests==2.27.30", "types-retry==0.9.7"],
    "test": [  # `test` GitHub Action jobs uses this
        "pytest>=6.0,<7.0",  # Core testing package
        "pytest-xdist",  # multi-process runner
        "pytest-cov",  # Coverage analyzer plugin
        "hypothesis>=6.2.0,<7.0",  # Strategy-based fuzzer
        "eth-hash[pysha3]",  # For eth-utils address checksumming
    ],
    "lint": [
        "black>=22.3.0,<23.0",  # auto-formatter and linter
        "mypy>=0.960,<1.0",  # Static type analyzer
        "flake8>=4.0.1,<5.0",  # Style linter
        "isort>=5.10.1,<6.0",  # Import sorting linter
    ],
    "dev": [
        "commitizen",  # Manage commits and publishing releases
        "pre-commit",  # Ensure that linters are run prior to commiting
        "pytest-watch",  # `ptw` test watcher/runner
        "IPython",  # Console for interacting
        "ipdb",  # Debugger (Must use `export PYTHONBREAKPOINT=ipdb.set_trace`)
    ],
}

# NOTE: `pip install -e .[dev]` to install package
extras_require["dev"] = (
    extras_require["test"]
    + extras_require["lint"]
    + extras_require["dev"]
    + extras_require["types"]
)

extras_require["lint"] = extras_require["lint"] + extras_require["types"]

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="apr",
    version="0.0.0",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="""apr: Trisolaris APR calculating serverless functions""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Trisolaris DAO",
    author_email="0xchain@trisolaris.io",
    url="https://github.com/trisolaris-labs/apr",
    include_package_data=True,
    install_requires=[
        "importlib-metadata ; python_version<'3.8'",
        "pydantic>=1.9.0,<2.0",
        "hexbytes>=0.2.2,<1.0.0",
        "eth-utils>=1.10.0",
        "APScheduler==3.8.1",
        "eth_account==0.5.6",
        "google-cloud-storage==1.43.0",
        "protobuf==3.19.1",
        "web3==5.25.0",
        "retry==0.9.2",
    ],  # NOTE: Add 3rd party libraries here
    python_requires=">=3.7.2,<4",
    extras_require=extras_require,
    py_modules=[""],
    license="Apache-2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"apr": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
