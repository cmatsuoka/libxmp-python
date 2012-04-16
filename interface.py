
class Xmp:
	"""A multi format module player

	Xmp implements a full-featured module player that supports
	many different module formats including Protracker MOD, Scream
	Tracker III S3M, Fast Tracker II XM and Impulse Tracker IT modules.

	"""
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

