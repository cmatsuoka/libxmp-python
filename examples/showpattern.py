#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
Display pattern data
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Module


def display_pattern(module, num):
    notes = [ 'C ', 'C#', 'D ', 'D#', 'E ', 'F ',
              'F#', 'G ', 'G#', 'A ', 'A#', 'B ' ]

    pattern = module.get_pattern(num)
    print 'PATTERN {0:02x}'.format(num)

    for i in range(pattern.rows):
        sys.stdout.write('{0:02X}|'.format(i))

        for j in range(module.chn):
            event = module.get_event(num, i, j)
            
            if event.note == 0:
                sys.stdout.write('---')
            elif event.note > 128:
                sys.stdout.write('===')
            else:
                n = (event.note - 1) % 12
                o = (event.note - 1) / 12
                sys.stdout.write('{0}{1}'.format(notes[n], o))

            sys.stdout.write(' ')

            if event.ins == 0:
                sys.stdout.write('--')
            else:
                sys.stdout.write('{0:02x}'.format(event.ins - 1))

            sys.stdout.write('|')
        sys.stdout.write('\n')

if len(sys.argv) < 3:
    print 'Usage: {0} <module> <patnum>'.format(os.path.basename(sys.argv[0]))
    sys.exit(1)

try:
    module = Module(sys.argv[1])
except IOError, error:
    sys.stderr.write('{0}: {1}\n'.format(sys.argv[1], error.strerror))
    sys.exit(1)

display_pattern(module, int(sys.argv[2]))
