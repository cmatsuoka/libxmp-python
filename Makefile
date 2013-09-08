
pyxmp.py: ../libxmp/include/xmp.h interface.py Makefile
	ctypesgen/ctypesgen.py -x 'XMP_VER.*' -lxmp ../libxmp/include/xmp.h -o $@ --insert-file=interface.py
	sed -i.bak 's/^xmp_context = String/xmp_context = c_long/;s/ \* 1)/ * 256)/;s/'\''xpo'\'', c_char/'\''xpo'\'', c_byte/' $@

