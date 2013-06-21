
class Xmp:
	"""A multi format module player

	Xmp implements a full-featured module player that supports
	many different module formats including Protracker MOD, Scream
	Tracker III S3M, Fast Tracker II XM and Impulse Tracker IT modules.

	"""

	# Regular C API calls for libxmp 4.1

	def __init__(self):
		self._ctx = xmp_create_context()

	def __del__(self):
		if self._ctx != None:
			self.free()

	def free(self):
		xmp_free_context(self._ctx)
		self._ctx = None

	def load_module(self, path):
		code = xmp_load_module(self._ctx, path)
		if (code < 0):
			code = -code
			raise IOError(code, os.strerror(code))
	
        @staticmethod
        def test_module(path, info):
                code = xmp_test_module(path, pointer(info))
                return (code == 0)

	def scan_module(self):
		xmp_scan_module(self._ctx)

	def release_module(self):
		xmp_release_module(self._ctx)

	def start_player(self, freq, mode):
		return xmp_start_player(self._ctx, freq, mode)

	def play_frame(self):
		return xmp_play_frame(self._ctx) == 0

	def play_buffer(self, buf, size, loop):
		return xmp_play_buffer(self._ctx, buf, size, loop)

	def get_frame_info(self, info = struct_xmp_frame_info()):
		xmp_get_frame_info(self._ctx, pointer(info))
		return info

	def end_player(self):
		xmp_end_player(self._ctx)

	def inject_event(self, chn, event):
		xmp_inject_event(self._ctx, chn, event)

	def get_module_info(self, info = struct_xmp_module_info()):
		xmp_get_module_info(self._ctx, pointer(info))
		return info

	def get_format_list(self):
		format_list = xmp_get_format_list()
		i = 0
		l = []
		while format_list[i]:
			l.append(ctypes.string_at(format_list[i]))
			i = i + 1
		return l

	def next_position(self):
		return xmp_next_position(self._ctx)

	def prev_position(self):
		return xmp_prev_position(self._ctx)

	def set_position(self, num):
		return xmp_set_position(self._ctx, num)

	def stop_module(self):
		xmp_stop_module(self._ctx)

	def restart_module(self):
		xmp_restart_module(self._ctx)

	def seek_time(self, time):
		return xmp_seek_time(self._ctx, time)

	def channel_mute(self, chn, val):
		return xmp_channel_mute(self._ctx, chn, val)

	def channel_vol(self, chn, val):
		return xmp_channel_vol(self._ctx, chn, val)

	def set_player(self, param, value):
		return xmp_set_player(self._ctx, param, value)

	def get_player(self, param):
		return xmp_get_player(self._ctx, param)

	def set_instrument_path(self, path):
		return xmp_set_instrument_path(self._ctx, path)
	
	# Extra convenience calls

	@staticmethod
	def test_info():
		return struct_xmp_test_info()

	@staticmethod
	def module_info():
		return struct_xmp_module_info()

	@staticmethod
	def frame_info():
		return struct_xmp_frame_info()

	@staticmethod
	def get_buffer(info):
		buf = ctypes.cast(info.buffer, POINTER(c_int8))
		return ctypes.string_at(buf, info.buffer_size);

	def get_sample(self, num):
		mod = self.get_module_info().mod[0]
		sample = mod.xxs[num]
		buf = ctypes.cast(sample.data, POINTER(c_int8))

		if sample.flg & XMP_SAMPLE_16BIT:
			width = 2
		else:
			width = 1

		return ctypes.string_at(buf, sample.len * width)

