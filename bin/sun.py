#!/usr/bin/python

import sys
import paths
import pprint
import datetime
from SC6_Camera import Sky
from SC6_Camera import Config
from SC6_Camera import Logger

config_file = "/usr/local/cam/conf/config_test.yml"
mode = "test"
debug = 0

c = Config.Config(
    config_file=config_file,
     mode=mode,
     config_in=None)
config = c.getConfig()
print config['Logging']['LogConfig']

debug = c.getDebug()

l = Logger.Logger(config)
logger = l.getLogger("sun.py")
logger.info("getting started mode: %s" % mode)

dt = datetime.datetime.now()
sky = Sky.Sky(config)
print sky.sky_message
print "is_sun: %d" % sky.is_sun()
print "is_hour_after_dusk: %d" % sky.is_hour_after_dusk()

print "is_after_sunrise: %d" % sky.is_after_sunrise()
print "is_after_noon: %d" % sky.is_after_noon()
print "is_after_sunset: %d" % sky.is_after_sunset()
