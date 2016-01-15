from os.path import join
from os.path import dirname
from os.path import isfile


if isfile(join(dirname(__file__), 'local.py')):
    from local import *
else:
    from defaults import *
