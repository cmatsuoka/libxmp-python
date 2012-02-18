#!/usr/bin/python
#
# A simple modplayer in python using xmp and pyaudio

import sys, os, xmp
import pyaudio

def show_info(mod):
	print "Name: %s" % (mod.name)
	print "Type: %s" % (mod.type)
	print "Instruments: %d" % (mod.ins)
	for i in range (mod.ins):
		ins = mod.xxi[i]
		print " %2d %s" % (i, ins.name)
	

if len(sys.argv) < 2:
	print "Usage: %s <module>" % (os.path.basename(sys.argv[0]))
	sys.exit(1)

info = xmp.struct_xmp_module_info()

x = xmp.Xmp()
x.loadModule(sys.argv[1])

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, channels = 2, rate = 44100,
		output = True)

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
	stream.write(buf);	

x.playerEnd()

stream.close()
p.terminate()

x.releaseModule()
