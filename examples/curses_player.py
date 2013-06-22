#!/usr/bin/python
"""
A simple modplayer in python (callback version)
"""

import sys
import os
import time
import pyaudio
import curses
from threading import Lock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Xmp

CHANNELS = 2
WORD_SIZE = 2
SAMPLE_RATE = 44100
VOL_DECAY = 1


def cb_callback(in_data, frame_count, time_info, status):
    """Pyaudio callback function."""
    size = frame_count * CHANNELS * WORD_SIZE
    lock.acquire()
    data = xmp.play_buffer(size)
    lock.release()
    return (data, pyaudio.paContinue)

def show_info(minfo, finfo, vols):
    mod = minfo.mod[0]

    # header
    stdscr.addstr(0, 0, 'Name: {0.name:<30} Type: {0.type:<30}'.format(mod),
                  curses.A_REVERSE)
    stdscr.addstr(1, 0, 'Ins: {1.ins}   Smp: {1.smp}   Pos: {0.pos:>3}'
                  '/{1.len:>3}   Row: {0.row:>3}/{0.num_rows:>3}'.
                  format(finfo, mod))

    # channel list
    for i in range(mod.chn):
        cinfo = finfo.channel_info[i]
        ins = cinfo.instrument
        event = cinfo.event

        if event.vol != 0:
            vols[i] = (cinfo.volume * 16 / minfo.vol_base)
        vols[i] -= VOL_DECAY
        if vols[i] < 0:
            vols[i] = 0
        if event.note > 0 and event.note < Xmp.KEY_OFF:
            vols[i] = 16

        if ins < 255:
            if cinfo.volume > 0:
                ins_text = mod.xxi[ins].name
            else:
                ins_text = '' 
        else:
            ins_text = '<unused>'

        stdscr.addstr(3 + i, 0, ' {0:>2}: {1:<22} {2:<16}'.format(i + 1,
                      ins_text, '=' * vols[i]))
    stdscr.refresh()
    
def play(filename):
    """Load and play the module file."""
    try:
        xmp.load_module(filename)
    except IOError, error:
        sys.stderr.write('{0}: {1}\n'.format(filename, error.strerror))
        sys.exit(1)
    
    minfo = xmp.get_module_info()
    vols = [ 0 for i in range(minfo.mod[0].chn) ]

    audio = pyaudio.PyAudio()
    stream = audio.open(format = audio.get_format_from_width(WORD_SIZE),
                    channels = CHANNELS, rate = SAMPLE_RATE,
                    output = True, stream_callback = cb_callback)
    
    xmp.start_player(SAMPLE_RATE)
    stream.start_stream()
    finfo = Xmp.frame_info()

    while stream.is_active():
        lock.acquire()
        xmp.get_frame_info(finfo)
        lock.release()
        show_info(minfo, finfo, vols)
        sys.stdout.flush()
        time.sleep(0.05)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    xmp.end_player()
    xmp.release_module()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: {0} <module>".format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    stdscr = curses.initscr()
    (height, width) = stdscr.getmaxyx() 
    #curses.start_color()
    curses.noecho()
    #curses.cbreak()
    #stdscr.keypad(1)

    stdscr.clear()
    curses.endwin()

    xmp = Xmp()
    lock = Lock()
    play(sys.argv[1])

    #curses.nocbreak();
    #stdscr.keypad(0);
    curses.echo()
    #curses.end_color()
