#!/usr/bin/python
"""
A simple modplayer in python (callback version)
"""

import sys
import os
import time
import pyaudio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Xmp

CHANNELS = 2
WORD_SIZE = 2
SAMPLE_RATE = 44100


def callback(in_data, frame_count, time_info, status):
    cont = pyaudio.paContinue
    size = frame_count * CHANNELS * WORD_SIZE
    data = Xmp.buffer(size)
    if not xmp.play_buffer(data, size):
        cont = pyaudio.paComplete
    return (data, cont)


if len(sys.argv) < 2:
    print "Usage: %s <module>" % (os.path.basename(sys.argv[0]))
    sys.exit(1)

xmp = Xmp()
try:
    xmp.load_module(sys.argv[1])
except IOError, error:
    sys.stderr.write('{0}: {1}\n'.format(sys.argv[1], error.strerror))
    sys.exit(1)

print 'Module name:', xmp.get_module_info().mod[0].name

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WORD_SIZE),
                channels = CHANNELS, rate = SAMPLE_RATE,
                output = True, stream_callback = callback)

xmp.start_player(SAMPLE_RATE)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
p.terminate()

xmp.end_player()
xmp.release_module()

