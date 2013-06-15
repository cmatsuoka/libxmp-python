import subprocess

header_path = subprocess.check_output(
    ['pkg-config', '--cflags', 'libxmp']).strip()[2:]

args = [
    'ctypesgen/ctypesgen.py',
    '-lxmp',
    '{include}/xmp.h'.format(include=header_path),
    '-o', 'pyxmp.py',
    '--insert-file=interface.py'
]

subprocess.call(args)

args = [
    'sed',
    # BSD sed *requires* an extension argument to -i
    '-i', '.bak',
    's/^xmp_context = String/xmp_context = c_long/',
    'pyxmp.py'
]

subprocess.call(args)

args = [
    'sed',
    '-i', '.bak',
    '/^# \/.*\/include\/xmp.h: \d*/d;s/\s*# \/.*\/include\/xmp.h: \d*.*//;s/ \* 1)/ * 256)/',
    'pyxmp.py'
]

subprocess.call(args)
