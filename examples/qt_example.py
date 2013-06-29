#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
PyQt player example
"""

import sys
import os
import time
import atexit
import struct
import pyaudio
from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import QApplication, QWidget, QPainter
from threading import Lock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Xmp

CHANNELS = 2
WORD_SIZE = 2
SAMPLE_RATE = 44100


def cb_player(in_data, frame_count, time_info, status):
    """Pyaudio callback function."""
    global data, end_flag
    size = frame_count * CHANNELS * WORD_SIZE
    lock.acquire()
    data = xmp.play_buffer(size)
    if data == None:
        end_flag = True
    lock.release()
    return (data, pyaudio.paContinue)

def stop():
    """Exit handler."""
    example.stop()

class AnimationThread(QThread) :
    """Animation update thread

    Emit periodic update signals to refresh the oscilloscope graph.

    """
    def __init__(self):
        QThread.__init__(self) 
        self._run = True

    def stop(self):
        """Stop the signal thread."""
        self._run = False

    def run(self):
        """Emit update signals in a loop."""
        while self._run == True:
            self.emit(SIGNAL("update_request"))
            time.sleep(0.05)

class Example(QWidget):
    """Our oscilloscope view

    Display the module PCM data in a oscilloscope-style graph

    """
    def __init__(self):
        super(Example, self).__init__()
        self.resize(480, 360)
        self.setWindowTitle('Player')
        self._qp = QPainter()
        self._thread = AnimationThread()
        self.connect(self._thread, SIGNAL("update_request"), self.update)
        self._thread.start()
        self.show()

    def paintEvent(self, event):
        """Draw the oscilloscope."""
        lock.acquire()
        if (end_flag):
            self._thread.stop()
            app.quit()
        else:
            self._qp.begin(self)
            #self._qp.setPen(Qt.red)
            width = self.size().width()
            height = self.size().height() / 2
            for i in range(width):
                pos = i * 4
                left = struct.unpack('=h', data[pos:pos + 2])[0]
                right = struct.unpack('=h', data[pos + 2:pos + 4])[0]
                self._qp.drawPoint(i, height + height * (left + right) / 65536)
            self._qp.end()
        lock.release()

    def play(self, filename):
        """Load and play the module file."""
        try:
            mod = xmp.load_module(filename)
        except IOError, error:
            sys.stderr.write('{0}: {1}\n'.format(filename, error.strerror))
            sys.exit(1)
    
        # Display module info
        print 'Name: {0.name}\nType: {0.type}'.format(mod)
    
        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(
                        format = self._audio.get_format_from_width(WORD_SIZE),
                        channels = CHANNELS, rate = SAMPLE_RATE,
                        output = True, stream_callback = cb_player)
        xmp.start_player(SAMPLE_RATE)
        self._stream.start_stream()

    def stop(self):
        """Stop oscilloscope updates and deinitialize the player."""
        self._thread.stop()
        self._stream.stop_stream()
        self._stream.close()
        self._audio.terminate()
        xmp.end_player()
        xmp.release_module()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {0} <module>".format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    app = QApplication(sys.argv)
    example = Example()

    xmp = Xmp()
    lock = Lock()
    end_flag = False
    example.play(sys.argv[1])
    atexit.register(stop)

    sys.exit(app.exec_())

