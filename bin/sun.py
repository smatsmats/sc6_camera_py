#!/usr/bin/python

import sys
import paths
from SC6_Camera import Sky
from SC6_Camera import Config

config_file = "/usr/local/cam/conf/config_test.yml"
mode = "test"
debug = 0

c = Config.Config(
    config_file=config_file,
     mode=mode,
     config_in=None)
config=c.getConfig()
debug=c.getDebug()


s = Sky.Sun()
# print c.config
# print c.Logging.LogConfig
print config['Logging']['LogConfig']
