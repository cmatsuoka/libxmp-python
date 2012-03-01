
libxmp.py:
	ctypesgen/ctypesgen.py -lxmp ../include/xmp.h -o libxmp.py
	sed -i 's/^xmp_context = String/xmp_context = c_long/' $@
