#!/usr/bin/python

import sys
import paths
import pprint
from SC6_Camera import DataStoreFS
from SC6_Camera import ImageOverlay
from SC6_Camera import Config
from SC6_Camera import Logger
from SC6_Camera import Sky

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
logger = l.getLogger("fetch_one_image.py")

sky = Sky.Sky(config)

print "Current time: %s" % sky.current_time()
