
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

	def test_module(self, path, info):
		code = xmp_test_module(path, pointer(info))
		return (code == 0)

	def load_module(self, path):
		code = xmp_load_module(self._ctx, path)
		if (code < 0):
			code = -code
			raise IOError(code, os.strerror(code))
	
	def release_module(self):
		xmp_release_module(self._ctx)

	def start_player(self, freq, mode):
		return xmp_start_player(self._ctx, freq, mode)

	def get_frame_info(self, info):
		return xmp_get_frame_info(self._ctx, pointer(info))

	def get_module_info(self, info):
		return xmp_get_module_info(self._ctx, pointer(info))

	def get_buffer(self, info):
		buf = ctypes.cast(info.buffer, POINTER(c_int8))
		return ctypes.string_at(buf, info.buffer_size);

	def play_frame(self):
		return xmp_play_frame(self._ctx) == 0

	def end_player(self):
		xmp_end_player(self._ctx)

	def get_sample(self, mod, num):
		sample = mod.xxs[num]
		buf = ctypes.cast(sample.data, POINTER(c_int8))

		if sample.flg & XMP_SAMPLE_16BIT:
			width = 2
		else:
			width = 1

		return ctypes.string_at(buf, sample.len * width)

