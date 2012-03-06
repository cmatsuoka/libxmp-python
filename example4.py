#!/usr/bin/python
#
# Example 4: display pattern data

import sys, os, xmp

def display_pattern(mod, num):
	notes = [ 'C ', 'C#', 'D ', 'D#', 'E ', 'F ',
		  'F#', 'G ', 'G#', 'A ', 'A#', 'B ' ]

	print "PATTERN %02x" % (num)

	rows = mod.xxp[num][0].rows
	channels = mod.chn;

	for i in range(rows):
		sys.stdout.write("%02x|" % (i))

		for j in range(channels):
			track = mod.xxp[num][0].index[j]
			track_rows = mod.xxt[track][0].rows
			event = mod.xxt[track][0].event[i]
			
			if event.note == 0:
				sys.stdout.write("---")
			elif event.note > 128:
				sys.stdout.write("===")
			else:
				n = event.note % 12
				o = event.note / 12
				sys.stdout.write("%s%d" % (notes[n], o))

			sys.stdout.write(" ")

			if event.ins == 0:
				sys.stdout.write("--")
			else:
				sys.stdout.write("%02x" % (event.ins - 1))

			sys.stdout.write("|")

		sys.stdout.write("\n")

if len(sys.argv) < 3:
	print "Usage: %s <module> <patnum>" % (os.path.basename(sys.argv[0]))
	sys.exit(1)

info = xmp.struct_xmp_module_info()

x = xmp.Xmp()

try:
	x.loadModule(sys.argv[1])
except IOError as (errno, strerror):
	sys.stderr.write("%s: %s\n" % (sys.argv[1], strerror))
	sys.exit(1)

x.playerStart(0, 44100, 0)
x.getInfo(info)

display_pattern(info.mod[0], int(sys.argv[2]))
