import ConfigParser
from os.path import dirname, realpath

class Config(object):
    def __init__(self):
        config_file = dirname(realpath(__file__)) + '/evernotecli.cfg'
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        self.use_sandbox = self.config.get('testing', 'use_sandbox')

    def get(self, section, option):
        if self.use_sandbox == 'True':
            option = 'sandbox_' + option

        return self.config.get(section, option)
