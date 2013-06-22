#!/usr/bin/python
"""
Identify module files
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Xmp

if len(sys.argv) < 2:
    print "Usage: %s <module>" % (os.path.basename(sys.argv[0]))
    sys.exit(1)

xmp = Xmp()

info = Xmp.test_info()

for name in sys.argv[1:]:
    if Xmp.test_module(name, info):
        print "%-25.25s %-25.25s %s" % (name, info.type, info.name)


