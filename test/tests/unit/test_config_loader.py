import os
import unittest
from unittest import mock
from pm_config_loader import ConfigLoader

config_dir = './test/tests/fixtures/configs'
yaml_config_path = f'{config_dir}/config.yaml'
yml_config_path = f'{config_dir}/config.yml'
json_config_path = f'{config_dir}/config.json'
invalid_config_path = f'{config_dir.replace("/configs", "/invalid_configs")}/config.ini'

expected_config = {
    'key-1': {
        'child-key-1': {
            'grandchild-key-1': 'value-1'
        }
    },
    'key-2': {
        'child-key-2': {
            'grandchild-key-2': 'value-2'
        }
    }
}
expected_full_result_dir = [
    {**expected_config, 'path': './test/tests/fixtures/configs/config.json'},
    {**expected_config, 'path': './test/tests/fixtures/configs/config.yaml'},
    {**expected_config, 'path': './test/tests/fixtures/configs/config.yml'}
]


class TestConfigLoader(unittest.TestCase):
    def test_init_returns_correct_instance_with_config_file(self):
        expected_instance: dict = {
            'possible_codecs': ['json', 'yml', 'yaml'],
            'is_file': True,
            'is_dir': False,
            'target_path': yaml_config_path,
            'env_replace': False,
        }

        config_loader = ConfigLoader(path=expected_instance.get('target_path'))

        self.assertEqual(expected_instance.get('possible_codecs'), config_loader.possible_codecs)
        self.assertEqual(expected_instance.get('is_file'), config_loader.is_file)
        self.assertEqual(expected_instance.get('is_dir'), config_loader.is_dir)
        self.assertEqual(expected_instance.get('target_path'), config_loader.target_path)
        self.assertEqual(expected_instance.get('env_replace'), config_loader.env_replace)

    def test_init_returns_correct_instance_with_config_dir(self):
        expected_instance: dict = {
            'possible_codecs': ['json', 'yml', 'yaml'],
            'is_file': False,
            'is_dir': True,
            'target_path': config_dir,
            'env_replace': False,
        }

        config_loader = ConfigLoader(path=expected_instance.get('target_path'))

        self.assertEqual(expected_instance.get('possible_codecs'), config_loader.possible_codecs)
        self.assertEqual(expected_instance.get('is_file'), config_loader.is_file)
        self.assertEqual(expected_instance.get('is_dir'), config_loader.is_dir)
        self.assertEqual(expected_instance.get('target_path'), config_loader.target_path)
        self.assertEqual(expected_instance.get('env_replace'), config_loader.env_replace)

    def test_init_raises_with_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            ConfigLoader(path='foo')

    def test_validate_file_returns_correct_codec(self):
        config_loader = ConfigLoader(path=yaml_config_path)
        codec = config_loader._validate_file(file_path=yaml_config_path)
        self.assertEqual('yaml', codec)

    def test_validate_file_raises_type_error_with_incorrect_codec(self):
        config_loader = ConfigLoader(path=invalid_config_path)
        with self.assertRaises(TypeError):
            config_loader._validate_file(file_path=invalid_config_path)

    def test_load_config_loads_yaml_files(self):
        config_loader = ConfigLoader(path=yaml_config_path)
        config_loader._validate_file = mock.MagicMock(return_value='yaml')

        config = config_loader._load_config(path=yaml_config_path)
        self.assertEqual(expected_config, config)

    def test_load_config_loads_yml_files(self):
        config_loader = ConfigLoader(path=yml_config_path)
        config_loader._validate_file = mock.MagicMock(return_value='yml')

        config = config_loader._load_config(path=yml_config_path)
        self.assertEqual(expected_config, config)

    def test_load_config_loads_json_files(self):
        config_loader = ConfigLoader(path=json_config_path)
        config_loader._validate_file = mock.MagicMock(return_value='json')

        config = config_loader._load_config(path=json_config_path)
        self.assertEqual(expected_config, config)

    def test_generate_update_dict_returns_correct_update_dict(self):
        value: str = 'foo'
        keys: list = 'key-1'
        expected_update_dict: dict = {
            'key-1': 'foo'
        }

        config_loader = ConfigLoader(path=json_config_path)
        update_dict = config_loader._generate_update_dict(value=value, keys=keys)

        self.assertEqual(expected_update_dict, update_dict)

    def test_generate_update_dict_returns_correct_nested_update_dict(self):
        value: str = 'foo'
        keys: list = 'key-1.child-key-1.grandchild-key-1'
        expected_update_dict: dict = {
            'key-1': {
                'child-key-1': {
                    'grandchild-key-1': 'foo'
                }
            }
        }

        config_loader = ConfigLoader(path=json_config_path)
        update_dict = config_loader._generate_update_dict(value=value, keys=keys)

        self.assertEqual(expected_update_dict, update_dict)

    def test_update_returns_correct_updated_dict(self):
        update_dict: dict = {
            'key-1': 'foo'
        }
        expected_updated_dict: dict = {
            'key-1': 'foo',
            'key-2': {
                'child-key-2': {
                    'grandchild-key-2': 'value-2'
                }
            }
        }

        config_loader = ConfigLoader(path=json_config_path)
        updated_dict = config_loader._update(config=expected_config, update=update_dict)

        self.assertEqual(expected_updated_dict, updated_dict)

    def test_update_returns_correct_nested_updated_dict(self):
        update_dict: dict = {
            'key-1': {
                'child-key-1': {
                    'grandchild-key-1': 'foo'
                }
            }
        }
        expected_updated_dict: dict = {
            'key-1': {
                'child-key-1': {
                    'grandchild-key-1': 'foo'
                }
            },
            'key-2': {
                'child-key-2': {
                    'grandchild-key-2': 'value-2'
                }
            }
        }

        config_loader = ConfigLoader(path=json_config_path)
        updated_dict = config_loader._update(config=expected_config, update=update_dict)

        self.assertEqual(expected_updated_dict, updated_dict)

    def test_env_replace_calls_generate_update_dict_with_nested_keys(self):
        os.environ['KEY_1___CHILD_KEY_1___GRANDCHILD_KEY_1'] = 'foo'
        config_loader = ConfigLoader(path=json_config_path)

        config_loader._generate_update_dict = mock.MagicMock()
        config_loader._env_replace(config=expected_config)

        config_loader._generate_update_dict.assert_called_once_with(value='foo', keys='key-1.child-key-1.grandchild-key-1')
        os.environ.pop('KEY_1___CHILD_KEY_1___GRANDCHILD_KEY_1')

    def test_env_replace_calls_generate_update_dict_with_single_key(self):
        os.environ['KEY_1___'] = 'foo'
        config_loader = ConfigLoader(path=json_config_path)

        config_loader._generate_update_dict = mock.MagicMock()
        config_loader._env_replace(config=expected_config)

        config_loader._generate_update_dict.assert_called_once_with(value='foo', keys='key-1')
        os.environ.pop('KEY_1___')

    def test_load_correctly_returns_single_file(self):
        config_loader = ConfigLoader(path=yaml_config_path)

        configs = config_loader.load()
        self.assertEqual([{'path': yaml_config_path, **expected_config}], configs)

    def test_load_correctly_returns_dir(self):
        config_loader = ConfigLoader(path=config_dir)

        configs = config_loader.load()
        self.maxDiff = None
        self.assertEqual(expected_full_result_dir, configs)

    def test_load_calls_env_replace(self):
        config_loader = ConfigLoader(path=yml_config_path, env_replace=True)

        config_loader._env_replace = mock.MagicMock()
        config_loader.load()

        config_loader._env_replace.assert_called_once()
