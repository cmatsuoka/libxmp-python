#!/usr/bin/python
"""
Example 4: display pattern data
"""

import sys
import os
import libxmp


def display_pattern(mod, num):
    notes = [ 'C ', 'C#', 'D ', 'D#', 'E ', 'F ',
          'F#', 'G ', 'G#', 'A ', 'A#', 'B ' ]

    print "PATTERN %02x" % (num)

    rows = mod.xxp[num][0].rows
    channels = mod.chn;

    for i in range(rows):
        sys.stdout.write("%02X|" % (i))

        for j in range(channels):
            track = mod.xxp[num][0].index[j]
            track_rows = mod.xxt[track][0].rows
            event = mod.xxt[track][0].event[i]
            
            if event.note == 0:
                sys.stdout.write("---")
            elif event.note > 128:
                sys.stdout.write("===")
            else:
                n = (event.note - 1) % 12
                o = (event.note - 1) / 12
                sys.stdout.write("%s%d" % (notes[n], o))

            sys.stdout.write(" ")

            if event.ins == 0:
                sys.stdout.write("--")
            else:
                sys.stdout.write("%02x" % (event.ins - 1))

            sys.stdout.write("|")
        sys.stdout.write("\n")

if len(sys.argv) < 3:
    print "Usage: %s <module> <patnum>" % (os.path.basename(sys.argv[0]))
    sys.exit(1)

info = libxmp.struct_xmp_module_info()

xmp = libxmp.Xmp()

try:
    xmp.loadModule(sys.argv[1])
except IOError, error:
    sys.stderr.write('{0}: {1}\n'.format(filename, error.strerror))
    sys.exit(1)

xmp.playerStart(44100, 0)
xmp.getInfo(info)

display_pattern(info.mod[0], int(sys.argv[2]))
