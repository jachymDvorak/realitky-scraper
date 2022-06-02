import yaml
import os

class Config():

    def __init__(self, config_name: str = 'config.yaml'):

        self.config_name = config_name
        self.config = self.read_config()
        self.sreality = self.config['sreality']
        self.breality = self.config['breality']
        self.ireality = self.config['ireality']
        self.preality = self.config['preality']
        self.database = self.config['database']
        self.emails = self.config['emails']

    def read_config(self) -> dict:

        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', self.config_name))

        print(f'Reading config from: {filename}')

        with open(filename, 'r') as file:
            config = yaml.safe_load(file)

        return config
