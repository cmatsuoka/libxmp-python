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


class AnimationThread(QThread) :
    def __init__(self):
        QThread.__init__(self) 
        self._run = True

    def stop(self):
        self._run = False

    def run(self):
        while self._run == True:
            self.emit(SIGNAL("update_request"))
            time.sleep(0.05)

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.resize(480, 360)
        self.setWindowTitle('Player')
        self._qp = QPainter()
        self._thread = AnimationThread()
        self.connect(self._thread, SIGNAL("update_request"), self.update)
        self._thread.start()
        self.show()

    def paintEvent(self, e):
        lock.acquire()
        self._qp.begin(self)
        #self._qp.setPen(Qt.red)
        width = self.size().width()
        height = self.size().height()
        
        for i in range(width):
            x = struct.unpack('b', data[i * 4 + 1])[0]
            self._qp.drawPoint(i, height / 2 + height / 2 * x / 128)
        lock.release()

        self._qp.end()

    def stop(self):
        self._thread.stop()
        
def cb_player(in_data, frame_count, time_info, status):
    """Pyaudio callback function."""
    global data
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

    audio = pyaudio.PyAudio()
    stream = audio.open(format = audio.get_format_from_width(WORD_SIZE),
                    channels = CHANNELS, rate = SAMPLE_RATE,
                    output = True, stream_callback = cb_player)

    xmp.start_player(SAMPLE_RATE)
    stream.start_stream()

def stop():
    example.stop()
    stream.stop_stream()
    stream.close()
    audio.terminate()
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
    play(sys.argv[1])
    atexit.register(stop)

    sys.exit(app.exec_())

