from ctypes import *
from libxmp import *

class Xmp:
	def __init__(self):
		self._ctx = xmp_create_context()

	def __del__(self):
		self.free()

	def free(self):
		xmp_free_context(self._ctx)

	def testModule(self, path):
		code = xmp_test_module(self._ctx, path)
		if (code < 0):
			code = -code
			raise IOError(code, os.strerror(code))

	def loadModule(self, path):
		code = xmp_load_module(self._ctx, path)
		if (code < 0):
			code = -code
			raise IOError(code, os.strerror(code))
	
	def releaseModule(self):
		xmp_release_module(self._ctx)

	def playerStart(self, start, freq, mode):
		return xmp_player_start(self._ctx, start, freq, mode)

	def getInfo(self, info):
		return xmp_player_get_info(self._ctx, pointer(info))

	def getBuffer(self, info):
		buf = ctypes.cast(info.buffer, POINTER(c_int8))
		return ctypes.string_at(buf, info.buffer_size);

	def playerFrame(self):
		return xmp_player_frame(self._ctx) == 0

	def playerEnd(self):
		xmp_player_end(self._ctx)

