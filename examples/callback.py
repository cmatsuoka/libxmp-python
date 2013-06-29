#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
A simple modplayer in python (callback version)
"""

import sys
import os
import time
import pyaudio
from threading import Lock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Xmp

CHANNELS = 2
WORD_SIZE = 2
SAMPLE_RATE = 44100


def cb_callback(in_data, frame_count, time_info, status):
    """Pyaudio callback function."""
    size = frame_count * CHANNELS * WORD_SIZE
    lock.acquire()
    data = xmp.play_buffer(size)
    lock.release()
    return (data, pyaudio.paContinue)

def play(filename):
    """Load and play the module file."""
    try:
        mod = xmp.load_module(filename)
    except IOError, error:
        sys.stderr.write('{0}: {1}\n'.format(filename, error.strerror))
        sys.exit(1)
    
    # Display module info
    print 'Name: {0.name}\nType: {0.type}'.format(mod)
    print 'Instruments: {0.ins}   Samples: {0.smp}'.format(mod)
    for i in range (mod.ins):
        inst = mod.get_instrument(i)
        if len(inst.name.rstrip()) > 0:
            print ' {0:>2} {1.name}'.format(i, inst)
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format = audio.get_format_from_width(WORD_SIZE),
                    channels = CHANNELS, rate = SAMPLE_RATE,
                    output = True, stream_callback = cb_callback)
    
    xmp.start_player(SAMPLE_RATE)
    stream.start_stream()
    info = Xmp.frame_info()

    while stream.is_active():
        lock.acquire()
        xmp.get_frame_info(info)
        lock.release()
        sys.stdout.write(' {0.pos:>3}/{1.len:>3} {0.row:>3}/{0.num_rows:>3}\r'
                         .format(info, mod))
        sys.stdout.flush()
        time.sleep(0.1)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    xmp.end_player()
    xmp.release_module()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: {0} <module>".format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    xmp = Xmp()
    lock = Lock()
    play(sys.argv[1])

