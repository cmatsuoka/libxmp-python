#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
A simple modplayer in python (callback version)
"""

import sys
import os
import time
import pyaudio
import curses
import atexit
from threading import Lock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Xmp

CHANNELS = 2
WORD_SIZE = 2
SAMPLE_RATE = 44100
VOL_DECAY = 1

def reset():
    """Reset terminal settings."""
    curses.endwin()
    print "Reset terminal settings"

def cb_callback(in_data, frame_count, time_info, status):
    """Pyaudio callback function."""
    size = frame_count * CHANNELS * WORD_SIZE
    lock.acquire()
    data = xmp.play_buffer(size)
    lock.release()
    return (data, pyaudio.paContinue)

def show_event(event):
    """Display a single event"""
    notes = [ 'C ', 'C#', 'D ', 'D#', 'E ', 'F ',
              'F#', 'G ', 'G#', 'A ', 'A#', 'B ' ]

    if event.ins > 0:
        ins = event.ins
    else:
        ins = '--'

    if event.vol > 0:
        vol = event.vol
    else:
        vol = '--'

    if event.note == 0:
        note = '--- -- --|'
    elif event.note < 128:
        note = '{0}{1} {2:>2} {3:>2}|'.format(notes[event.note % 12],
                                         event.note / 12, ins, vol)
    else:
        note = '=== -- --|'

    return '{0:3}'.format(note)
    
def header_info(height, width, finfo, mod):
    """Display basic module data on top pane."""
    p_h = 2
    p_w = width - 2

    win1 = curses.newwin(p_h + 2, width, 0, 0)
    win1.box()
    pad1 = curses.newpad(p_h, p_w)

    pad1.addstr(0, 0, 'Name: {0.name:<30} Type: {0.type}'
                  .format(mod).ljust(p_w), curses.A_REVERSE)
    pad1.addstr(1, 0, 'Ins: {1.ins}   Smp: {1.smp}   Chn: {1.chn}   '
                  'Pos:{0.pos:>3}/{1.len:>3}   Row:{0.row:>3}/{0.num_rows:>3}'
                  .format(finfo, mod))

    win1.noutrefresh()
    pad1.noutrefresh(0, 0,  1, 1,  p_h, p_w)        # 1 + p_h - 1

def channel_info(height, width, minfo, finfo, vols):
    """Display instrument and volume bars in middle pane."""
    p_h = (height - 4) / 2 - 2
    p_w = width - 2
    win2 = curses.newwin(p_h + 2, width, 4, 0)
    win2.box()
    pad2 = curses.newpad(p_h, p_w)

    mod = minfo.mod[0]

    for i in range(mod.chn):
        if i >= p_h * 2:
            break

        cinfo = finfo.channel_info[i]
        ins = cinfo.instrument
        event = cinfo.event

        if event.vol != 0:
            vols[i] = (cinfo.volume * 12 / minfo.vol_base)
        elif event.note > 0 and event.note < Xmp.KEY_OFF and ins < 255:
            vols[i] = (mod.xxi[ins].vol * 12 / minfo.vol_base)

        vols[i] -= VOL_DECAY
        if vols[i] < 0:
            vols[i] = 0

        if ins < 255:
            if cinfo.volume > 0:
                ins_text = mod.xxi[ins].name
            else:
                ins_text = '' 
        else:
            ins_text = '<unused>'

        if i >= p_h:
            col = p_w / 2
            ofs = p_h
        else:
            col = 0
            ofs = 0

        if vols[i] > 12:
            print vols[i]

        pad2.addstr(i - ofs, col, '{0:>2}:{1:<22} {2:<12}'.format(i + 1,
                      ins_text, '=' * vols[i]))
    win2.noutrefresh()
    pad2.noutrefresh(0, 0,  5, 1,  5 - 1 + p_h, p_w)

def track_info(height, width, finfo, mod):
    """Display track data in bottom pane."""
    p_x = (height - 4) / 2 - 2
    p_h = height - p_x - 4
    p_w = width
    pad3 = curses.newpad(p_h, p_w + 10)

    # row numbers
    for j in range(p_h - 1):
        row = finfo.row + j - (p_h - 1) / 2
        if row < 0 or row >= finfo.num_rows:
            row = ''
        if j == (p_h - 1) / 2:
            pad3.addstr(j + 1, 0, '{0:>3}'.format(row), curses.A_BOLD)
        else:
            pad3.addstr(j + 1, 0, '{0:>3}'.format(row))

    # channels
    for chn in range (mod.chn):
        if 4 + chn * 10 >= p_w:
            break
        pad3.addstr(0, 4 + chn * 10, '{0:^10}'
                        .format(chn + 1), curses.A_REVERSE)

        # rows
        for j in range(p_h - 1):
            row = finfo.row + j - (p_h - 1) / 2
            if row < 0 or row >= finfo.num_rows:
                evstr = ''
            else:
                event = xmp.get_event(finfo.pattern, row, chn)
                evstr = show_event(event)
            if j == (p_h - 1) / 2:
                pad3.addstr(j + 1, 4 + chn * 10, evstr, curses.A_BOLD)
            else:
                pad3.addstr(j + 1, 4 + chn * 10, evstr)

    pad3.noutrefresh(0, 0,  p_x + 4 + 2, 0,  height - 1, width - 1) 

def play(filename):
    """Load and play the module file."""
    try:
        xmp.load_module(filename)
    except IOError, error:
        sys.stderr.write('{0}: {1}\n'.format(filename, error.strerror))
        sys.exit(1)
    
    minfo = xmp.get_module_info()
    mod = minfo.mod[0]
    vols = [ 0 ] * mod.chn

    audio = pyaudio.PyAudio()
    stream = audio.open(format = audio.get_format_from_width(WORD_SIZE),
                    channels = CHANNELS, rate = SAMPLE_RATE,
                    output = True, stream_callback = cb_callback)
    
    xmp.start_player(SAMPLE_RATE)
    stream.start_stream()
    finfo = Xmp.frame_info()

    (height, width) = stdscr.getmaxyx() 

    old_row = -1
    while stream.is_active():
        lock.acquire()
        xmp.get_frame_info(finfo)
        lock.release()

        if finfo.row != old_row:
            header_info(height, width, finfo, mod)
            track_info(height, width, finfo, mod)
            old_row = finfo.row
    
        channel_info(height, width, minfo, finfo, vols)
        curses.doupdate()
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
    atexit.register(reset)

    curses.start_color()
    curses.noecho()
    curses.curs_set(0)
    #curses.cbreak()
    #stdscr.keypad(1)

    stdscr.clear()
    curses.endwin()

    xmp = Xmp()
    lock = Lock()
    play(sys.argv[1])

    #curses.nocbreak();
    #stdscr.keypad(0);
    #curses.curs_set(1)
    #curses.echo()
