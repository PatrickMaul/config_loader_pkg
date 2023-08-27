# ConfigLoader - Devs docs

[![Unittest](https://github.com/PatrickMaul/config_loader_pkg/actions/workflows/unittest.yml/badge.svg)](https://github.com/PatrickMaul/config_loader_pkg/actions/workflows/unittest.yml)
[![codecov](https://codecov.io/gh/PatrickMaul/config_loader_pkg/graph/badge.svg?token=TSJ32TOKBJ)](https://codecov.io/gh/PatrickMaul/config_loader_pkg)

This is the developer documentation for the `ConfigLoader` module, which is used for loading configurations. You will
also find information here on how to run unit tests, as well as how to build and publish the module.

## Table of Contents

<!-- TOC -->
* [ConfigLoader - Devs docs](#configloader---devs-docs)
  * [Table of Contents](#table-of-contents)
  * [Project Setup](#project-setup)
  * [Running Unit Tests](#running-unit-tests)
  * [Building](#building)
  * [Publishing](#publishing)
  * [Example Usage](#example-usage)
<!-- TOC -->

## Project Setup

To collaborate on the `ConfigLoader` module, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory where you want the project to reside.
3. Execute the following command to clone the repository:
   ```bash
   git clone https://github.com/PatrickMaul/config_loader_pkg
   ```
4. Navigate to the root directory of your project. `cd ./config_loader_pkg`
5. Execute the following command to install dependencies:
   ```bash
   pip install -U pip
   pip install -r requirements.txt
   ```

## Running Unit Tests

To run unit tests for the `ConfigLoader` module, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the root directory of the `ConfigLoader` module.

    - Execute the following command to run unit tests:
       ```bash
       python -m unittest discover test/tests/unit
       ```
      **Note**: You might need to export the `PYTHONPATH`.

    - Execute the following command to run coverage tests:
       ```bash
       coverage run --source=./src -m unittest discover ./test/tests/unit && coverage html -d test/tests/htmlcov
       ```
      **Note**: You might need to export the `PYTHONPATH`.

## Building

To build the `ConfigLoader` module, follow these steps:

1. Navigate to the root directory of the `ConfigLoader` module.
2. Make sure you have `build` installed. If not, you can install it using the following command:
   ```bash
   pip install -U build
   ```

3. Execute the following command to build the module:
   ```bash
   python -m build
   ```

## Publishing

To upload the `ConfigLoader` module using `twine`, follow these steps:

1. Navigate to the root directory of the `ConfigLoader` module.
2. Make sure you have `twine` installed. If not, you can install it using the following command:
   ```bash
   pip install -U twine
   ```
3. Execute the following command to upload the module using `twine`:
   ```bash
   python -m twine upload -r testpypi -u <username> -p <password> dist/*
   ```

## Example Usage

Here is a simple example of how you can use the `ConfigLoader` module:

```python
from configloader import ConfigLoader

config_path = "path/to/config.yml"
config_loader = ConfigLoader(config_path)
configs = config_loader.load()

for config in configs:
    print(config)
```
