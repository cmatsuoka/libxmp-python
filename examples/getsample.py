#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
Extract samples to wav files
"""

import sys
import os
import wave

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Xmp


def extract_sample(xmp, insnum, num):
    sample = xmp.get_sample(insnum, num)
    filename = "sample-%02x-%02x.wav" % (insnum, num)
    length = sample.len

    if sample.len == 0:
        print "Skip empty sample %d" % (num)
        return

    if sample.flg & Xmp.SAMPLE_16BIT:
        sample_width = 2
        length *= 2
    else:
        sample_width = 1

    print "Extract sample %d as %s (%d bytes)" % (num, filename, length)

    w = wave.open(filename, 'w');
    w.setnchannels(1)
    w.setsampwidth(sample_width)
    w.setframerate(16000)
    w.writeframes(Xmp.get_sample_data(sample))

def extract_instrument(xmp, num):
    inst = xmp.get_module().xxi[num]
    print 'Instrument %d ("%s") has %d samples' % (num, inst.name, inst.nsm)
    for i in range (inst.nsm):
        extract_sample(xmp, num, i)


if len(sys.argv) < 3:
    print "Usage: %s <module> <insnum>" % (os.path.basename(sys.argv[0]))
    sys.exit(1)

xmp = Xmp()

try:
    xmp.load_module(sys.argv[1])
except IOError, error:
    sys.stderr.write('{0}: {1}\n'.format(sys.argv[1], error.strerror))
    sys.exit(1)

extract_instrument(xmp, int(sys.argv[2]))
