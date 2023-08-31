import os
import yaml
import json
import collections.abc


class ConfigLoader:
    def __init__(self, path: str, env_replace: bool = False) -> None:
        """
        Initializes the ConfigLoader.

        :param path: The path to the configuration file or configuration directory.
        :param env_replace: A boolean value indicating whether to replace environment variables. Default: False
        """
        # Check if 'path' exists
        if not os.path.exists(path=path):
            raise FileNotFoundError(f'Path "{path}" not found!')

        self._possible_codecs: list = ['json', 'yml', 'yaml']
        self._is_file = os.path.isfile(path=path)
        self._is_dir = os.path.isdir(s=path)
        self._target_path: str = path
        self._env_replace: bool = env_replace

    def _validate_file(self, file_path: str) -> str:
        """
        Checks if the file can be processed and returns the file codec.

        :param file_path: The path to the file to validate.
        :return: The recognized file codec.
        """
        if os.path.exists(path=file_path) and os.path.isfile(path=file_path):
            file: str = file_path.rsplit("/", )[-1]
            codec: str = file.rsplit('.', 1)[-1]

            if codec not in self._possible_codecs:  # Incorrect file codec
                raise TypeError(f'The file "{file}" cannot be processed. Please specify a `json` or `yml/yaml` file.')

            return codec

    def _load_config(self, path: str = None) -> dict:
        """
        Loads the configuration from a file.

        :param path: The path to the configuration file.
        :return: The loaded configuration.
        """
        path: str = path or self._target_path
        # Check file
        file_ending: str = self._validate_file(file_path=path)

        # Read configuration file
        with open(path, 'r') as config_file:
            if file_ending in ['json']:
                config = json.load(config_file)
            elif file_ending in ['yml', 'yaml']:
                config = yaml.safe_load(config_file)

        return config

    def _replace_env(self, config) -> None:
        """
        Replaces configuration values with corresponding environment variables.

        :param config: The configuration in which values should be replaced.
        """
        env_keys = [s for s in os.environ.keys() if "___" in s]  # Filter environment variables
        raw_env_key_paths = [s.lower().split('___') for s in env_keys]
        env_key_paths = []

        for raw_env_key_path in raw_env_key_paths:
            env_key_path = []
            for p in raw_env_key_path:
                if not p == '':
                    env_key_path.append(p)
            env_key_paths.append(env_key_path)

        # Replace all `_` with `-`, otherwise multi-word keys won't match
        # DUMMY_1___CFG___FOO="bla" => ['dummy-1', 'cfg', 'foo']
        for index, env_key_path in enumerate(env_key_paths):
            for sub_index, key in enumerate(env_key_path):
                env_key_paths[index][sub_index] = key.replace('_', '-')

        # Generate a dictionary that matches the structure of the value to update
        # ['dummy-1', 'cfg', 'foo'] => {"dummy-1": {"cfg": {"foo": "bla"}}}
        for index, env_key_path in enumerate(env_key_paths):
            config_update = self._generate_update_dict(value=os.environ.get(env_keys[index]), keys='.'.join(env_key_path))
            self._update(config, config_update)

    def _generate_update_dict(self, value: any, keys: str) -> dict:
        """
        Generates an update dictionary for the environment variable.

        :param value: The value of the environment variable.
        :param keys: The key hierarchy to be updated.
        :return: The generated update dictionary.
        """
        if '.' in keys:
            key, _keys = keys.split('.', 1)
            return {key: self._generate_update_dict(value, _keys)}
        else:  # Last key
            return {keys: value}

    def _update(self, config: dict, update: dict | collections.abc.Mapping) -> dict:
        """
        Updates the configuration with values from the update dictionary.

        :param config: The configuration to be updated.
        :param update: The update dictionary with new values.
        :return: The updated configuration.
        """
        for key, value in update.items():
            if config.get(key) and isinstance(value, collections.abc.Mapping):  # Remove `d.get(k)` to add new entries
                config[key] = self._update(config.get(key, {}), value)
            else:
                if config.get(key):  # Remove this line to add new keys to the configuration
                    config[key] = value
        return config

    def load(self) -> list:
        """
        Loads the configuration(s) based on the specified path.

        :return: A sorted list of loaded configurations.
        """
        configs = []
        self._target_path = self._target_path

        if self._is_file:
            configs.append({'path': self._target_path, **self._load_config()})
        elif self._is_dir:
            config_paths = os.listdir(self._target_path)
            # Load and add configuration
            for file in config_paths:
                config_path = f'{self._target_path}/{file}'
                configs.append({'path': config_path, **self._load_config(path=config_path)})

        if self._env_replace:
            for config in configs:
                self._replace_env(config)

        # Sort files in ascending order by path
        return sorted(configs, key=lambda d: d['path'])
