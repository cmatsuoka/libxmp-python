#!/usr/bin/python
"""
Example 1: A simple modplayer in python using xmp and pyaudio
"""

import sys
import os
import pyaudio
import pyxmp

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
    
def play(filename):
    """
    Our mod player.
    """
    info = pyxmp.struct_xmp_module_info()
    
    xmp = pyxmp.Xmp()
    try:
        xmp.loadModule(filename)
    except IOError, error:
        sys.stderr.write('{0}: {1}\n'.format(filename, error.strerror))
        sys.exit(1)
    
    sound = Sound()
    
    xmp.playerStart(44100, 0)
    xmp.getInfo(info)
    
    mymod = info.mod[0]
    show_info(mymod)
    
    while xmp.playerFrame():
        xmp.getInfo(info)
        if info.loop_count > 0:
            break
    
        if info.frame == 0:
            sys.stdout.write(" %3d/%3d  %3d/%3d\r" %
                (info.order, mymod.len, info.row, info.num_rows))
            sys.stdout.flush()
    
        sound_buffer = xmp.getBuffer(info)
        sound.write(sound_buffer)
    
    xmp.playerEnd()
    sound.close()
    xmp.releaseModule()


if len(sys.argv) < 2:
    print "Usage: %s <module>" % (os.path.basename(sys.argv[0]))
    sys.exit(1)

play(sys.argv[1])
