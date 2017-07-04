import sys
import os

# some scripts expect this attribute to be in this module
#prefix = '/usr/local/cam_py'
prefix = '/home/willey/sc6_camera_py'
exec_prefix = '${prefix}'

# work around a bogus autoconf 2.12 bug
if exec_prefix == '${prefix}':
    exec_prefix = prefix

# maybe put the package somewhere else later
sys.path.insert(0, prefix)

## Include Python's site-packages directory.
#sitedir = os.path.join(sys.prefix, 'lib', 'python'+sys.version[:3],
#                       'site-packages')
#sys.path.append(sitedir)
