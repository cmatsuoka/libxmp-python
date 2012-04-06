'''Wrapper for xmp.h

Generated with:
ctypesgen/ctypesgen.py -lxmp ../include/xmp.h -o xmp.py --insert-file=interface.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # FIXME / TODO return '.' and os.path.dirname(__file__)
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")
        dirs.append(os.path.dirname(__file__))

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")
        directories.append(os.path.dirname(__file__))

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["xmp"] = load_library("xmp")

# 1 libraries
# End libraries

# No modules

class struct_xmp_channel(Structure):
    pass

struct_xmp_channel.__slots__ = [
    'pan',
    'vol',
    'flg',
]
struct_xmp_channel._fields_ = [
    ('pan', c_int),
    ('vol', c_int),
    ('flg', c_int),
]

class struct_xmp_pattern(Structure):
    pass

struct_xmp_pattern.__slots__ = [
    'rows',
    'index',
]
struct_xmp_pattern._fields_ = [
    ('rows', c_int),
    ('index', c_int * 256),
]

class struct_xmp_event(Structure):
    pass

struct_xmp_event.__slots__ = [
    'note',
    'ins',
    'vol',
    'fxt',
    'fxp',
    'f2t',
    'f2p',
    'flag',
]
struct_xmp_event._fields_ = [
    ('note', c_ubyte),
    ('ins', c_ubyte),
    ('vol', c_ubyte),
    ('fxt', c_ubyte),
    ('fxp', c_ubyte),
    ('f2t', c_ubyte),
    ('f2p', c_ubyte),
    ('flag', c_ubyte),
]

class struct_xmp_track(Structure):
    pass

struct_xmp_track.__slots__ = [
    'rows',
    'event',
]
struct_xmp_track._fields_ = [
    ('rows', c_int),
    ('event', struct_xmp_event * 256),
]

class struct_xmp_envelope(Structure):
    pass

struct_xmp_envelope.__slots__ = [
    'flg',
    'npt',
    'scl',
    'sus',
    'sue',
    'lps',
    'lpe',
    'data',
]
struct_xmp_envelope._fields_ = [
    ('flg', c_int),
    ('npt', c_int),
    ('scl', c_int),
    ('sus', c_int),
    ('sue', c_int),
    ('lps', c_int),
    ('lpe', c_int),
    ('data', c_short * (32 * 2)),
]

class struct_anon_1(Structure):
    pass

struct_anon_1.__slots__ = [
    'ins',
    'xpo',
]
struct_anon_1._fields_ = [
    ('ins', c_ubyte),
    ('xpo', c_char),
]

class struct_xmp_subinstrument(Structure):
    pass

struct_xmp_subinstrument.__slots__ = [
    'vol',
    'gvl',
    'pan',
    'xpo',
    'fin',
    'vwf',
    'vde',
    'vra',
    'vsw',
    'rvv',
    'sid',
    'nna',
    'dct',
    'dca',
    'ifc',
    'ifr',
    'hld',
]
struct_xmp_subinstrument._fields_ = [
    ('vol', c_int),
    ('gvl', c_int),
    ('pan', c_int),
    ('xpo', c_int),
    ('fin', c_int),
    ('vwf', c_int),
    ('vde', c_int),
    ('vra', c_int),
    ('vsw', c_int),
    ('rvv', c_int),
    ('sid', c_int),
    ('nna', c_int),
    ('dct', c_int),
    ('dca', c_int),
    ('ifc', c_int),
    ('ifr', c_int),
    ('hld', c_int),
]

class struct_xmp_instrument(Structure):
    pass

struct_xmp_instrument.__slots__ = [
    'name',
    'vol',
    'nsm',
    'rls',
    'aei',
    'pei',
    'fei',
    'vts',
    'wts',
    'map',
    'sub',
]
struct_xmp_instrument._fields_ = [
    ('name', c_char * 32),
    ('vol', c_int),
    ('nsm', c_int),
    ('rls', c_int),
    ('aei', struct_xmp_envelope),
    ('pei', struct_xmp_envelope),
    ('fei', struct_xmp_envelope),
    ('vts', c_int),
    ('wts', c_int),
    ('map', struct_anon_1 * 121),
    ('sub', POINTER(struct_xmp_subinstrument)),
]

class struct_xmp_sample(Structure):
    pass

struct_xmp_sample.__slots__ = [
    'name',
    'len',
    'lps',
    'lpe',
    'flg',
    'data',
]
struct_xmp_sample._fields_ = [
    ('name', c_char * 32),
    ('len', c_int),
    ('lps', c_int),
    ('lpe', c_int),
    ('flg', c_int),
    ('data', POINTER(c_ubyte)),
]

class struct_xmp_sequence(Structure):
    pass

struct_xmp_sequence.__slots__ = [
    'entry_point',
    'duration',
]
struct_xmp_sequence._fields_ = [
    ('entry_point', c_int),
    ('duration', c_int),
]

class struct_xmp_module(Structure):
    pass

struct_xmp_module.__slots__ = [
    'name',
    'type',
    'pat',
    'trk',
    'chn',
    'ins',
    'smp',
    'spd',
    'bpm',
    'len',
    'rst',
    'gvl',
    'xxp',
    'xxt',
    'xxi',
    'xxs',
    'xxc',
    'xxo',
]
struct_xmp_module._fields_ = [
    ('name', c_char * 64),
    ('type', c_char * 64),
    ('pat', c_int),
    ('trk', c_int),
    ('chn', c_int),
    ('ins', c_int),
    ('smp', c_int),
    ('spd', c_int),
    ('bpm', c_int),
    ('len', c_int),
    ('rst', c_int),
    ('gvl', c_int),
    ('xxp', POINTER(POINTER(struct_xmp_pattern))),
    ('xxt', POINTER(POINTER(struct_xmp_track))),
    ('xxi', POINTER(struct_xmp_instrument)),
    ('xxs', POINTER(struct_xmp_sample)),
    ('xxc', struct_xmp_channel * 64),
    ('xxo', c_ubyte * 256),
]

class struct_xmp_test_info(Structure):
    pass

struct_xmp_test_info.__slots__ = [
    'name',
    'type',
]
struct_xmp_test_info._fields_ = [
    ('name', c_char * 64),
    ('type', c_char * 64),
]

class struct_xmp_channel_info(Structure):
    pass

struct_xmp_channel_info.__slots__ = [
    'period',
    'position',
    'pitchbend',
    'note',
    'instrument',
    'sample',
    'volume',
    'pan',
    'reserved',
    'event',
]
struct_xmp_channel_info._fields_ = [
    ('period', c_uint),
    ('position', c_uint),
    ('pitchbend', c_short),
    ('note', c_ubyte),
    ('instrument', c_ubyte),
    ('sample', c_ubyte),
    ('volume', c_ubyte),
    ('pan', c_ubyte),
    ('reserved', c_ubyte),
    ('event', struct_xmp_event),
]

class struct_xmp_module_info(Structure):
    pass

struct_xmp_module_info.__slots__ = [
    'order',
    'pattern',
    'row',
    'num_rows',
    'frame',
    'speed',
    'bpm',
    'time',
    'frame_time',
    'total_time',
    'buffer',
    'buffer_size',
    'total_size',
    'volume',
    'loop_count',
    'virt_channels',
    'virt_used',
    'vol_base',
    'channel_info',
    'mod',
    'comment',
    'sequence',
    'num_sequences',
    'seq_data',
]
struct_xmp_module_info._fields_ = [
    ('order', c_int),
    ('pattern', c_int),
    ('row', c_int),
    ('num_rows', c_int),
    ('frame', c_int),
    ('speed', c_int),
    ('bpm', c_int),
    ('time', c_int),
    ('frame_time', c_int),
    ('total_time', c_int),
    ('buffer', POINTER(None)),
    ('buffer_size', c_int),
    ('total_size', c_int),
    ('volume', c_int),
    ('loop_count', c_int),
    ('virt_channels', c_int),
    ('virt_used', c_int),
    ('vol_base', c_int),
    ('channel_info', struct_xmp_channel_info * 64),
    ('mod', POINTER(struct_xmp_module)),
    ('comment', String),
    ('sequence', c_int),
    ('num_sequences', c_int),
    ('seq_data', POINTER(struct_xmp_sequence)),
]

xmp_context = c_long

try:
    xmp_version = (c_uint).in_dll(_libs['xmp'], 'xmp_version')
except:
    pass

if hasattr(_libs['xmp'], 'xmp_create_context'):
    xmp_create_context = _libs['xmp'].xmp_create_context
    xmp_create_context.argtypes = []
    xmp_create_context.restype = xmp_context

if hasattr(_libs['xmp'], 'xmp_test_module'):
    xmp_test_module = _libs['xmp'].xmp_test_module
    xmp_test_module.argtypes = [String, POINTER(struct_xmp_test_info)]
    xmp_test_module.restype = c_int

if hasattr(_libs['xmp'], 'xmp_free_context'):
    xmp_free_context = _libs['xmp'].xmp_free_context
    xmp_free_context.argtypes = [xmp_context]
    xmp_free_context.restype = None

if hasattr(_libs['xmp'], 'xmp_load_module'):
    xmp_load_module = _libs['xmp'].xmp_load_module
    xmp_load_module.argtypes = [xmp_context, String]
    xmp_load_module.restype = c_int

if hasattr(_libs['xmp'], 'xmp_release_module'):
    xmp_release_module = _libs['xmp'].xmp_release_module
    xmp_release_module.argtypes = [xmp_context]
    xmp_release_module.restype = None

if hasattr(_libs['xmp'], '_xmp_ctl'):
    _func = _libs['xmp']._xmp_ctl
    _restype = c_int
    _argtypes = [xmp_context, c_int]
    _xmp_ctl = _variadic_function(_func,_restype,_argtypes)

if hasattr(_libs['xmp'], 'xmp_player_start'):
    xmp_player_start = _libs['xmp'].xmp_player_start
    xmp_player_start.argtypes = [xmp_context, c_int, c_int]
    xmp_player_start.restype = c_int

if hasattr(_libs['xmp'], 'xmp_player_frame'):
    xmp_player_frame = _libs['xmp'].xmp_player_frame
    xmp_player_frame.argtypes = [xmp_context]
    xmp_player_frame.restype = c_int

if hasattr(_libs['xmp'], 'xmp_player_get_info'):
    xmp_player_get_info = _libs['xmp'].xmp_player_get_info
    xmp_player_get_info.argtypes = [xmp_context, POINTER(struct_xmp_module_info)]
    xmp_player_get_info.restype = None

if hasattr(_libs['xmp'], 'xmp_player_end'):
    xmp_player_end = _libs['xmp'].xmp_player_end
    xmp_player_end.argtypes = [xmp_context]
    xmp_player_end.restype = None

if hasattr(_libs['xmp'], 'xmp_inject_event'):
    xmp_inject_event = _libs['xmp'].xmp_inject_event
    xmp_inject_event.argtypes = [xmp_context, c_int, POINTER(struct_xmp_event)]
    xmp_inject_event.restype = None

if hasattr(_libs['xmp'], 'xmp_get_format_list'):
    xmp_get_format_list = _libs['xmp'].xmp_get_format_list
    xmp_get_format_list.argtypes = []
    xmp_get_format_list.restype = POINTER(POINTER(c_char))

try:
    XMP_NAME_SIZE = 64
except:
    pass

try:
    XMP_KEY_OFF = 129
except:
    pass

try:
    XMP_KEY_CUT = 130
except:
    pass

try:
    XMP_KEY_FADE = 131
except:
    pass

try:
    XMP_CTL_POS_NEXT = 0
except:
    pass

try:
    XMP_CTL_POS_PREV = 1
except:
    pass

try:
    XMP_CTL_POS_SET = 2
except:
    pass

try:
    XMP_CTL_MOD_STOP = 3
except:
    pass

try:
    XMP_CTL_MOD_RESTART = 4
except:
    pass

try:
    XMP_CTL_SEEK_TIME = 7
except:
    pass

try:
    XMP_CTL_CH_MUTE = 8
except:
    pass

try:
    XMP_CTL_MIXER_AMP = 9
except:
    pass

try:
    XMP_CTL_MIXER_MIX = 16
except:
    pass

try:
    XMP_CTL_QUIRK_FX9 = 17
except:
    pass

try:
    XMP_CTL_QUIRK_FXEF = 18
except:
    pass

try:
    XMP_FORMAT_8BIT = (1 << 0)
except:
    pass

try:
    XMP_FORMAT_UNSIGNED = (1 << 1)
except:
    pass

try:
    XMP_FORMAT_MONO = (1 << 2)
except:
    pass

try:
    XMP_MAX_KEYS = 121
except:
    pass

try:
    XMP_MAX_ENV_POINTS = 32
except:
    pass

try:
    XMP_MAX_MOD_LENGTH = 256
except:
    pass

try:
    XMP_MAX_CHANNELS = 64
except:
    pass

try:
    XMP_ERROR_FORMAT = 28837
except:
    pass

try:
    XMP_ERROR_LOAD = 28838
except:
    pass

try:
    XMP_ERROR_DEPACK = 28839
except:
    pass

try:
    XMP_CHANNEL_SYNTH = (1 << 0)
except:
    pass

try:
    XMP_CHANNEL_MUTE = (1 << 1)
except:
    pass

try:
    XMP_ENVELOPE_ON = (1 << 0)
except:
    pass

try:
    XMP_ENVELOPE_SUS = (1 << 1)
except:
    pass

try:
    XMP_ENVELOPE_LOOP = (1 << 2)
except:
    pass

try:
    XMP_ENVELOPE_FLT = (1 << 3)
except:
    pass

try:
    XMP_ENVELOPE_SLOOP = (1 << 4)
except:
    pass

try:
    XMP_ENVELOPE_CARRY = (1 << 5)
except:
    pass

try:
    XMP_INST_NNA_CUT = 0
except:
    pass

try:
    XMP_INST_NNA_CONT = 1
except:
    pass

try:
    XMP_INST_NNA_OFF = 2
except:
    pass

try:
    XMP_INST_NNA_FADE = 3
except:
    pass

try:
    XMP_INST_DCT_OFF = 0
except:
    pass

try:
    XMP_INST_DCT_NOTE = 1
except:
    pass

try:
    XMP_INST_DCT_SMP = 2
except:
    pass

try:
    XMP_INST_DCT_INST = 3
except:
    pass

try:
    XMP_INST_DCA_CUT = XMP_INST_NNA_CUT
except:
    pass

try:
    XMP_INST_DCA_OFF = XMP_INST_NNA_OFF
except:
    pass

try:
    XMP_INST_DCA_FADE = XMP_INST_NNA_FADE
except:
    pass

try:
    XMP_SAMPLE_16BIT = (1 << 0)
except:
    pass

try:
    XMP_SAMPLE_LOOP = (1 << 1)
except:
    pass

try:
    XMP_SAMPLE_LOOP_BIDIR = (1 << 2)
except:
    pass

try:
    XMP_SAMPLE_LOOP_REVERSE = (1 << 3)
except:
    pass

try:
    XMP_SAMPLE_LOOP_FULL = (1 << 4)
except:
    pass

try:
    XMP_SAMPLE_SYNTH = (1 << 15)
except:
    pass

try:
    XMP_PERIOD_BASE = 6847
except:
    pass

def xmp_next_position(p):
    return (_xmp_ctl (p, XMP_CTL_POS_NEXT))

def xmp_prev_position(p):
    return (_xmp_ctl (p, XMP_CTL_POS_PREV))

def xmp_set_position(p, x):
    return (_xmp_ctl (p, XMP_CTL_POS_SET, x))

def xmp_stop_module(p):
    return (_xmp_ctl (p, XMP_CTL_MOD_STOP))

def xmp_restart_module(p):
    return (_xmp_ctl (p, XMP_CTL_MOD_RESTART))

def xmp_seek_time(p, x):
    return (_xmp_ctl (p, XMP_CTL_SEEK_TIME, x))

def xmp_channel_mute(p, x, y):
    return (_xmp_ctl (p, XMP_CTL_CH_MUTE, x, y))

def xmp_mixer_amp(p, x):
    return (_xmp_ctl (p, XMP_CTL_MIXER_AMP, x))

def xmp_mixer_mix(p, x):
    return (_xmp_ctl (p, XMP_CTL_MIXER_MIX, x))

def xmp_quirk_fx9(p, x):
    return (_xmp_ctl (p, XMP_CTL_QUIRK_FX9, x))

def xmp_quirk_fxef(p, x):
    return (_xmp_ctl (p, XMP_CTL_QUIRK_FXEF, x))

xmp_channel = struct_xmp_channel

xmp_pattern = struct_xmp_pattern

xmp_event = struct_xmp_event

xmp_track = struct_xmp_track

xmp_envelope = struct_xmp_envelope

xmp_subinstrument = struct_xmp_subinstrument

xmp_instrument = struct_xmp_instrument

xmp_sample = struct_xmp_sample

xmp_sequence = struct_xmp_sequence

xmp_module = struct_xmp_module

xmp_test_info = struct_xmp_test_info

xmp_channel_info = struct_xmp_channel_info

xmp_module_info = struct_xmp_module_info

# Begin inserted files

# Begin "interface.py"


class Xmp:
	def __init__(self):
		self._ctx = xmp_create_context()

	def __del__(self):
		if self._ctx != None:
			self.free()

	def free(self):
		xmp_free_context(self._ctx)
		self._ctx = None

	def testModule(self, path, info):
		code = xmp_test_module(path, pointer(info))
		return (code == 0)

	def loadModule(self, path):
		code = xmp_load_module(self._ctx, path)
		if (code < 0):
			code = -code
			raise IOError(code, os.strerror(code))
	
	def releaseModule(self):
		xmp_release_module(self._ctx)

	def playerStart(self, freq, mode):
		return xmp_player_start(self._ctx, freq, mode)

	def getInfo(self, info):
		return xmp_player_get_info(self._ctx, pointer(info))

	def getBuffer(self, info):
		buf = ctypes.cast(info.buffer, POINTER(c_int8))
		return ctypes.string_at(buf, info.buffer_size);

	def playerFrame(self):
		return xmp_player_frame(self._ctx) == 0

	def playerEnd(self):
		xmp_player_end(self._ctx)

	def getSample(self, mod, num):
		sample = mod.xxs[num]
		buf = ctypes.cast(sample.data, POINTER(c_int8))

		if sample.flg & XMP_SAMPLE_16BIT:
			width = 2
		else:
			width = 1

		return ctypes.string_at(buf, sample.len * width)


# End "interface.py"

# 1 inserted files
# End inserted files

