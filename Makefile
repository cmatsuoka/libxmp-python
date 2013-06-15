
pyxmp.py: ../libxmp/include/xmp.h interface.py Makefile
	ctypesgen/ctypesgen.py -lxmp ../libxmp/include/xmp.h -o $@ --insert-file=interface.py
	sed -i '.bak' 's/^xmp_context = String/xmp_context = c_long/' $@
	sed -i '.bak' '/^# \/.*\/include\/xmp.h: \d*/d;s/\s*# \/.*\/include\/xmp.h: \d*.*//;s/ \* 1)/ * 256)/' $@

