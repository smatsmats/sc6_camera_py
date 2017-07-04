import yaml
import logging
import logging.config


class Logger:

    def __init__(self, config):

        with open(config['Logging']['LogConfig'], 'rt') as f:
            self.lconfig = yaml.load(f.read())

    def getLogger(self, log_name="SC6_Camera"):
        logging.config.dictConfig(self.lconfig)
        logger = logging.getLogger(log_name)
        logger.debug("Logger started")
        return logger
