#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
Extract samples to wav files
"""

import sys
import os
import wave

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import *


def extract_sample(module, inst, num, filename):
    sample = module.get_sample(inst.get_subinstrument(num).sid)
    length = sample.len

    if sample.len == 0:
        print 'Skip empty sample {0}'.format(num)
        return

    if sample.flg & Xmp.SAMPLE_16BIT:
        sample_width = 2
        length *= 2
    else:
        sample_width = 1

    print 'Extract sample {0} as {1} ({2} bytes)'.format(num, filename, length)

    w = wave.open(filename, 'w');
    w.setnchannels(1)
    w.setsampwidth(sample_width)
    w.setframerate(16000)
    w.writeframes(sample.get_data())

def extract_instrument(module, num):
    inst = module.get_instrument(num)
    print 'Instrument {0} ("{1.name}") has {1.nsm} samples'.format(num, inst)
    for i in range (inst.nsm):
        filename = 'sample-{0:02x}-{1:02x}.wav'.format(num, i)
        extract_sample(module, inst, i, filename)


if len(sys.argv) < 3:
    print 'Usage: {0} <module> <insnum>'.format(os.path.basename(sys.argv[0]))
    sys.exit(1)

try:
    module = Module(sys.argv[1])
except IOError, error:
    sys.stderr.write('{0}: {1}\n'.format(sys.argv[1], error.strerror))
    sys.exit(1)

extract_instrument(module, int(sys.argv[2]))
