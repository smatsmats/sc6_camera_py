import yaml
import errno
import pprint

import logging
import logging.config


class Config:

    def __init__(self, config_in=None,
                 config_file="/usr/local/cam/conf/config.yml",
                 mode="prod"):

        try:
            config_root = yaml.load(file(config_file))
            self.config = config_root[mode]
        except IOError as e:
            raise IOError(errno.ENOENT, 'No config file found', config_file)
        except KeyError as e:
            raise KeyError('No config stanza for', mode)

        if 'Config' in self.config and 'Template' in self.config['Config']:
            if self.config['Config']['Template']:
                if self.config['Config']['Template'] != mode:
                    if not self.config['Config']['Template'] in config_root:
                        print("Asked to load config template of {} that doesn't exist.".format(
                            self.config['Config']['Template']))
                        exit(1)
                    else:
                        merged_config = config_root[
                            self.config['Config']['Template']].copy()
                        merged_config.update(self.config)
                        self.config = merged_config

        logger = self.getLogger()
        logger.info("Loaded config from %s" % config_file)

        if 'Debug' in self.config:
            debug = self.config['Debug']['Level']
            if debug >= self.config['Debug']['DumpConfig']:
#                pprint.pprint(self.config)
                logging.debug(pprint.pformat(config))

    def getConfig(self):
        return self.config

    def getDebug(self):
        return self.config['Debug']['Level']

    def getLogger(self, log_name="SC6_Camera"):
        with open(self.config['Logging']['LogConfig'], 'rt') as f:
            lconfig = yaml.load(f.read())
        logging.config.dictConfig(lconfig)

        # create logger
        self.logger = logging.getLogger(log_name)
        return self.logger
