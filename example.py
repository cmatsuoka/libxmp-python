#!/usr/bin/python
#
# A simple modplayer in python using xmp and pyaudio

import sys, os, xmp
import pyaudio

class sound:
	def __init__(self):
		self._p = p = pyaudio.PyAudio()
		self._stream = p.open(format = pyaudio.paInt16,
				channels = 2, rate = 44100, output = True)

	def write(self, buf):
		self._stream.write(buf)

	def close(self):
		self._stream.close()
		self._p.terminate()


def show_info(mod):
	print "Name: %s" % (mod.name)
	print "Type: %s" % (mod.type)
	print "Instruments: %d   Samples: %d" % (mod.ins, mod.smp)
	for i in range (mod.ins):
		ins = mod.xxi[i]
		if len(ins.name.rstrip()) > 0:
			print(" %2d %-32.32s  " % (i, mod.xxi[i].name))
	

if len(sys.argv) < 2:
	print "Usage: %s <module>" % (os.path.basename(sys.argv[0]))
	sys.exit(1)

info = xmp.struct_xmp_module_info()

x = xmp.Xmp()
try:
	x.loadModule(sys.argv[1])
except IOError as (errno, strerror):
	sys.stderr.write("%s: %s\n" % (sys.argv[1], strerror))
	sys.exit(1)

s = sound()

x.playerStart(0, 44100, 0)
x.getInfo(info)

mod = info.mod[0];
show_info(mod)

while x.playerFrame():
	x.getInfo(info)
	if info.loop_count > 0:
		break

	if info.frame == 0:
		sys.stdout.write(" %3d/%3d  %3d/%3d\r" %
			(info.order, mod.len, info.row, info.num_rows))
		sys.stdout.flush();

	buf = x.getBuffer(info)
	s.write(buf);	

x.playerEnd()
s.close()
x.releaseModule()
