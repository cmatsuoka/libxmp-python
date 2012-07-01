#!/usr/bin/python
"""
Example 3: extract samples to wav files
"""

import sys
import os
import wave
import libxmp


def extract_sample(xmp, mod, insnum, num):
    smpnum = mod.xxi[insnum].sub[num].sid
    sample = mod.xxs[smpnum]
    filename = "sample-%02x-%02x.wav" % (insnum, num)
    length = sample.len

    if sample.len == 0:
        print "Skip empty sample %d" % (num)
        return

    if sample.flg & libxmp.XMP_SAMPLE_16BIT:
        sample_width = 2
        length *= 2
    else:
        sample_width = 1

    print "Extract sample %d as %s (%d bytes)" % (num, filename, length)

    w = wave.open(filename, 'w');
    w.setnchannels(1)
    w.setsampwidth(sample_width)
    w.setframerate(16000)
    w.writeframes(xmp.getSample(mod, smpnum))

def extract_instrument(xmp, mod, num):
    inst = mod.xxi[num]
    print 'Instrument %d ("%s") has %d samples' % (num, inst.name, inst.nsm)
    for i in range (inst.nsm):
        extract_sample(xmp, mod, num, i)


if len(sys.argv) < 3:
    print "Usage: %s <module> <insnum>" % (os.path.basename(sys.argv[0]))
    sys.exit(1)

info = libxmp.struct_xmp_module_info()

xmp = libxmp.Xmp()

try:
    xmp.loadModule(sys.argv[1])
except IOError, error:
    sys.stderr.write('{0}: {1}\n'.format(sys.argv[1], error.strerror))
    sys.exit(1)

xmp.playerStart(44100, 0)
xmp.getInfo(info)

extract_instrument(xmp, info.mod[0], int(sys.argv[2]))
