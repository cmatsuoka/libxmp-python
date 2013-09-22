#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
Identify module files
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import *

if len(sys.argv) < 2:
    print 'Usage: {0} <module>'.format(os.path.basename(sys.argv[0]))
    sys.exit(1)

for name in sys.argv[1:]:
    try:
        info = Module.test(name)
        print '{0:25.25} {1.type:25.25} {1.name}'.format(name, info)
    except:
        pass


