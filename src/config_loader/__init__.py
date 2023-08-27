import os
import yaml
import json
import collections.abc


class ConfigLoader:
    def __init__(self, path: str, env_replace: bool = False) -> None:
        self.possible_codecs: list = ['json', 'yml', 'yaml']
        self.is_file = os.path.isfile(path=path)
        self.is_dir = os.path.isdir(s=path)

        # Check dir or single file
        if not (self.is_file or self.is_dir):
            raise AttributeError(f'Path "{self.target_path}" is neither a directory nor a single file.')

        self.target_path: str = path
        self.env_replace: bool = env_replace

    def _validate_path(self, path: str) -> str:
        # Check path
        if not os.path.exists(path=path):  # Path does not exist
            raise FileNotFoundError(f'Path not found. Please check the path: {path}')

        return path

    def _validate_file(self, file_path: str) -> str:
        if os.path.exists(path=file_path) and os.path.isfile(path=file_path):
            file: str = file_path.rsplit("/", )[-1]
            codec: str = file.rsplit('.', 1)[-1]

            if codec not in self.possible_codecs:  # File codec is wrong
                raise TypeError(f'File "{file}" can not be processed. Please provide a `json` or `yml/yaml` file')

            return codec

    def _load_config(self, path: str = None):
        path: str = path or self.target_path
        # Check file
        file_ending: str = self._validate_file(file_path=path)

        # Read config file
        with open(path, 'r') as config_file:
            if file_ending in ['json']:
                config = json.load(config_file)
            elif file_ending in ['yml', 'yaml']:
                config = yaml.safe_load(config_file)

        return config

    def _env_replace(self, config):
        env_keys = [s for s in os.environ.keys() if "___" in s]  # Filter env variables
        raw_env_key_paths = [s.lower().split('___') for s in env_keys]
        env_key_paths = []

        for raw_env_key_path in raw_env_key_paths:
            env_key_path = []
            for p in raw_env_key_path:
                if not p == '':
                    env_key_path.append(p)
            env_key_paths.append(env_key_path)

        # Replace all `_` with `-`. Otherwise, multiword job names won't match.
        # DUMMY_JOB___CFG___FOO="bla" => ['dummy-job', 'cfg', 'foo']
        for index, env_key_path in enumerate(env_key_paths):
            for sub_index, key in enumerate(env_key_path):
                env_key_paths[index][sub_index] = key.replace('_', '-')

        # Generate a dict which corresponds to the structure of the value to be updated.
        # ['dummy-job', 'cfg', 'foo'] => {"jobs": {"dummy-job": {"cfg": {"foo": "bla"}}
        for index, env_key_path in enumerate(env_key_paths):
            config_update = self._generate_update_dict(os.environ.get(env_keys[index]), '.'.join(env_key_path))
            print(config_update)
            self._update(config, config_update)

    def _generate_update_dict(self, value: any, keys: str):
        if '.' in keys:
            key, _keys = keys.split('.', 1)
            return {key: self._generate_update_dict(value, _keys)}
        else:  # last key
            return {keys: value}

    def _update(self, config: dict, update: dict | collections.abc.Mapping):
        for key, value in update.items():
            if config.get(key) and isinstance(value, collections.abc.Mapping):  # Remove `d.get(k)` to add new jobs
                config[key] = self._update(config.get(key, {}), value)
            else:
                if config.get(key):  # Remove this line to add new keys to config
                    config[key] = value
        return config

    def load(self) -> list:
        configs = []
        self.target_path = self._validate_path(self.target_path)

        if self.is_file:
            configs.append({'path': self.target_path, **self._load_config()})
        elif self.is_dir:
            config_paths = os.listdir(self.target_path)
            # Load and add config
            for file in config_paths:
                config_path = f'{self.target_path}/{file}'
                configs.append({'path': config_path, **self._load_config(path=config_path)})

        if self.env_replace:
            for config in configs:
                self._env_replace(config)

        # Sort files ascending by path
        return sorted(configs, key=lambda d: d['path'])
