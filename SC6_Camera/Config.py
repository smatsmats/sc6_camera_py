import yaml
import errno
import pprint

import logging
import logging.config

from SC6_Camera import Logger


class Config:

    def __init__(self, config_in=None,
                 config_file="/usr/local/cam/conf/config.yml",
                 mode="prod"):

        # read in config file and load initial config
        try:
            config_root = yaml.load(file(config_file))
            self.config = config_root[mode]
        except IOError as e:
            raise IOError(errno.ENOENT, 'No config file found', config_file)
        except KeyError as e:
            raise KeyError('No config stanza for', mode)

        # see if config is based on a template (should this recurse?)
        if 'Config' in self.config and 'Template' in self.config['Config']:
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

        l = Logger.Logger(self.config)
        logger = l.getLogger("Config")
        logger.info("Loaded config from %s" % config_file)

        if 'Debug' in self.config:
            debug = self.getDebug()
            if debug >= self.config['Debug']['DumpConfig']:
                logger.debug("Dumping config")
                logger.debug(pprint.pformat(self.config))

    def getConfig(self):
        return self.config

    def getDebug(self):
        return self.config['Debug']['Level']

    def writeConfig(self, old):
        return "no implemented"
