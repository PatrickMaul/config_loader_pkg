import unittest
from src.config_loader import ConfigLoader

config_dir = './test/tests/fixtures/configs'
yaml_config_path = f'{config_dir}/config.yaml'
yml_config_path = f'{config_dir}/config.yml'
json_config_path = f'{config_dir}/config.json'
invalid_config_path = f'{config_dir}/config.ini'
expected_full_result_single = [{
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
}]
expected_full_result_dir = [
    {
        'key-1': {
            'child-key-1': {
                'grandchild-key-1': 'value-1'
            }
        },
        'key-2': {
            'child-key-2': {
                'grandchild-key-2': 'value-2'
            }
        },
        'path': './test/tests/assets/config_loader_test_config.json'
    },
    {
            'key-1': {
                'child-key-1': {
                    'grandchild-key-1': 'value-1'
                }
            },
            'key-2': {
                'child-key-2': {
                    'grandchild-key-2': 'value-2'
                }
            },
            'path': './test/tests/assets/config_loader_test_config.yaml'
    },
    {
            'key-1': {
                'child-key-1': {
                    'grandchild-key-1': 'value-1'
                }
            },
            'key-2': {
                'child-key-2': {
                    'grandchild-key-2': 'value-2'
                }
            },
            'path': './test/tests/assets/config_loader_test_config.yml'
    }
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

    def test_init_raises_with_is_file_and_is_dir_false(self):
        with self.assertRaises(AttributeError) as exc:
            config_loader = ConfigLoader(path='foo')

    # def test_config_loader_loads_yaml_files(self):
        # self.init_config_loader_yaml()
        # config = self.config_loader.load()
        # self.assertEqual(config, [{'path': yaml_config_path, **expected_full_result_single[0]}])

    # def test_config_loader_loads_yml_files(self):
        # self.init_config_loader_yml()
        # config = self.config_loader.load()
        # self.assertEqual(config, [{'path': yml_config_path, **expected_full_result_single[0]}])

    # def test_config_loader_loads_json_files(self):
        # self.init_config_loader_json()
        # config = self.config_loader.load()
        # self.assertEqual(config, [{'path': json_config_path, **expected_full_result_single[0]}])

    # def test_config_loader_raises_attribute_error_with_invalid_file_type(self):
        # with self.assertRaises(AttributeError):
            # ConfigLoader(path='invalid_config_path').load()

    # def test_config_loader_raises_value_error_with_invalid_file_type(self):
        # with self.assertRaises(ValueError):
            # ConfigLoader(path=invalid_config_path).load()