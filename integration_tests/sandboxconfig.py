from evernoteconfig import Config
import logging

class SandboxConfig(Config):
    def __init__(self):
        super(Config, self).__init__()
        self.use_sandbox = True
        logging.debug('Instantiated sandbox config')
