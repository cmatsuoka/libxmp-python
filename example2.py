#!/usr/bin/python
"""
Example 2: identify module files
"""

import sys
import os
import xmplib

if len(sys.argv) < 2:
    print "Usage: %s <module>" % (os.path.basename(sys.argv[0]))
    sys.exit(1)

info = xmplib.struct_xmp_test_info()

xmp = xmplib.Xmplib()

for name in sys.argv[1:]:
    if xmp.testModule(name, info):
        print "%-25.25s %-25.25s %s" % (name, info.type, info.name)


