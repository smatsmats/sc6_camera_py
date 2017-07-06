#!/usr/bin/python

import sys
import paths
import pprint
from SC6_Camera import Sky
from SC6_Camera import Config
from SC6_Camera import Logger

config_file = "/usr/local/cam/conf/config_test.yml"
mode = "test"
debug = 0
force = 0

c = Config.Config(
    config_file=config_file,
     mode=mode,
     config_in=None)
config = c.getConfig()
debug = c.getDebug()
l = Logger.Logger(config)
logger = l.getLogger("sun.py")

sky = Sky.Sky(config)

print "Current time: %s" % sky.current_time()

if  force:
    print "We're forced to do this"
else:
    if sky.is_sun():
        print "Sun is up!"
    elif sky.is_hour_after_dusk():
        print "Sun is down, but for less than an hour!"
    else:
        print "Sun is down!"

print sky.sky_message
print "is_sun: %d" % sky.is_sun()
print "is_hour_after_dusk: %d" % sky.is_hour_after_dusk()
print "is_after_sunrise: %d" % sky.is_after_sunrise()
print "is_after_noon: %d" % sky.is_after_noon()
print "is_after_sunset: %d" % sky.is_after_sunset()
