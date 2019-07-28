import yaml
import os

class Config:
    _instance = None
    pyspedas_config = {}
    filepath = ''

    def __init__(self):
        self._create_pyspedas_config()


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def get_filepath(self):
        return self.filepath

    def get_config(self):
        return self.pyspedas_config

    def _create_pyspedas_config(self):
        if os.environ.get('PYSPEDAS_CONFIG_PATH'):
            config_path = os.environ.get('PYSPEDAS_CONFIG_PATH')
        else:
            os.path.abspath(os.path.dirname(__file__))
            dir_path = os.path.abspath(os.path.dirname(__file__))
            config_path = os.path.join(dir_path, 'default_configs.yml')

        self.filepath = config_path

        with open(config_path, 'r') as f:
            self.pyspedas_config = yaml.load(f, Loader=yaml.SafeLoader)
