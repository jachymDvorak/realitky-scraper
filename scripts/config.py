import yaml
import os

class Config():

    def __init__(self):

        self.config = self.read_config()
        self.sreality = self.config['sreality']
        self.breality = self.config['breality']
        self.ireality = self.config['ireality']
        self.preality = self.config['preality']
        self.emails = self.config['emails']

    def read_config(self):

        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))

        with open(filename, 'r') as file:
            config = yaml.safe_load(file)

        return config
