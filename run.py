from pm_config_loader import ConfigLoader


config_path: str = './assets/dummy_config_1.yml'
config_loader: ConfigLoader = ConfigLoader(path=config_path)

result: list = config_loader.load()
print(result)
