# ConfigLoader
[![Unittest](https://github.com/PatrickMaul/config_loader_pkg/actions/workflows/unittest.yml/badge.svg)](https://github.com/PatrickMaul/config_loader_pkg/actions/workflows/unittest.yml)
[![codecov](https://codecov.io/gh/PatrickMaul/config_loader_pkg/graph/badge.svg?token=TSJ32TOKBJ)](https://codecov.io/gh/PatrickMaul/config_loader_pkg)

The `ConfigLoader` class enables the loading of configuration files in JSON or YAML format, with the possibility to insert environment variables into the loaded configurations.

## Table of Contents

<!-- TOC -->
* [ConfigLoader](#configloader)
  * [Table of Contents](#table-of-contents)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Import](#import)
    * [Initialization](#initialization)
    * [Loading Configuration](#loading-configuration)
  * [Configuration Formats](#configuration-formats)
  * [Replacing Environment Variables](#replacing-environment-variables)
<!-- TOC -->

**Note**: To see the **Developers documentation** click [here](./DEVELOPERS_README.md).

## Installation

No specific installation is required. The provided code can be directly integrated into your Python project.

## Usage

### Import

Import the `ConfigLoader` class into your Python script:

```python
from pm_config_loader import ConfigLoader
```

### Initialization

Create an instance of the `ConfigLoader` class by specifying the path to the configuration file or configuration directory:

```python
config_path = "path/to/your/config"
config_loader = ConfigLoader(path=config_path, env_replace=True)
```

- `path`: The path to the configuration file or the directory containing configuration files.
- `env_replace`: A boolean value indicating whether environment variables should be replaced in the loaded configurations.

### Loading Configuration

Use the `load` method to load the configurations:

```python
loaded_configs = config_loader.load()
```

The `load` method returns a sorted list of configurations. The list is sorted by paths.

## Configuration Formats

The `ConfigLoader` supports the following configuration formats:

- JSON (`.json`)
- YAML (`.yml` or `.yaml`)

## Replacing Environment Variables

When `env_replace` is set to `True`, the `ConfigLoader` replaces specific environment variables in the loaded configurations. The environment variables should have specific patterns in their names to be replaced. For example:

```bash
DUMMY_1___CFG___FOO="bla"
```

will be converted to

```json
{
    "dummy-1": {
        "cfg": {
            "foo": "bla"
        }
    }
}
```