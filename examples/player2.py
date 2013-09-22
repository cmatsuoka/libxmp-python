#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
A simple modplayer in python
"""

import sys
import os
import pyaudio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import *

class Sound:
    """ Sound output manager

    This class uses PyAudio to play sound.

    """
    def __init__(self):
        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(format=pyaudio.paInt16, channels=2,
	                                rate=44100, output=True)

    def write(self, buf):
        """Write to PyAudio sound stream."""
        self._stream.write(buf)

    def close(self):
        """Close stream and free resources."""
        self._stream.close()
        self._audio.terminate()


def show_info(mod):
    """
    Display module information.
    """
    print "Name: %s" % (mod.name)
    print "Type: %s" % (mod.type)
    print "Instruments: %d   Samples: %d" % (mod.ins, mod.smp)
    for i in range (mod.ins):
        ins = mod.xxi[i]
        if len(ins.name.rstrip()) > 0:
            print(" %2d %-32.32s  " % (i, mod.xxi[i].name))
    
def cb_frame(finfo, args):
    """
    This callback is called after each module frame is played.
    """
    mod = args[0]

    if finfo.frame == 0:
        sys.stdout.write(" %3d/%3d  %3d/%3d\r" %
            (finfo.pos, mod.len, finfo.row, finfo.num_rows))
        sys.stdout.flush()

    global sound
    sound.write(finfo.get_buffer())

    return True

def play(filename):
    """
    Our mod player using the play() method and a callback.
    """

    player = Player()

    try:
        mod = Module(filename, player)
    except IOError, error:
        sys.stderr.write('{0}: {1}\n'.format(filename, error.strerror))
        sys.exit(1)
    
    global sound
    sound = Sound()

    show_info(mod)
    player.play(cb_frame, args = [ mod ]) 
    sound.close()
    mod.release()


if len(sys.argv) < 2:
    print "Usage: %s <module>" % (os.path.basename(sys.argv[0]))
    sys.exit(1)

play(sys.argv[1])
