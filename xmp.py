from ctypes import *
from libxmp import *

XMP_NAME_SIZE = XMP_NAME_SIZE
XMP_PERIOD_BASE = XMP_PERIOD_BASE

# Key constants
XMP_KEY_OFF = XMP_KEY_OFF
XMP_KEY_CUT = XMP_KEY_CUT
XMP_KEY_FADE = XMP_KEY_FADE

# Mixer format
XMP_FORMAT_8BIT = XMP_FORMAT_8BIT
XMP_FORMAT_UNSIGNED = XMP_FORMAT_UNSIGNED
XMP_FORMAT_MONO = XMP_FORMAT_MONO

# Limits
XMP_MAX_KEYS = XMP_MAX_KEYS
XMP_MAX_ENV_POINTS = XMP_MAX_ENV_POINTS
XMP_MAX_MOD_LENGTH = XMP_MAX_MOD_LENGTH
XMP_MAX_CHANNELS = XMP_MAX_CHANNELS

# Channel flags
XMP_CHANNEL_SYNTH = XMP_CHANNEL_SYNTH
XMP_CHANNEL_MUTE = XMP_CHANNEL_MUTE

# Envelope flags
XMP_ENVELOPE_ON = XMP_ENVELOPE_ON
XMP_ENVELOPE_SUS = XMP_ENVELOPE_SUS
XMP_ENVELOPE_LOOP = XMP_ENVELOPE_LOOP
XMP_ENVELOPE_FLT = XMP_ENVELOPE_FLT
XMP_ENVELOPE_SLOOP = XMP_ENVELOPE_SLOOP

# Instrument constants
XMP_INST_NNA_CUT = XMP_INST_NNA_CUT
XMP_INST_NNA_CONT = XMP_INST_NNA_CONT
XMP_INST_NNA_OFF = XMP_INST_NNA_OFF
XMP_INST_NNA_FADE = XMP_INST_NNA_FADE
XMP_INST_DCT_OFF = XMP_INST_DCT_OFF
XMP_INST_DCT_NOTE = XMP_INST_DCT_NOTE
XMP_INST_DCT_SMP = XMP_INST_DCT_SMP
XMP_INST_DCT_INST = XMP_INST_DCT_INST
XMP_INST_DCA_CUT = XMP_INST_DCA_CUT
XMP_INST_DCA_OFF = XMP_INST_DCA_OFF
XMP_INST_DCA_FADE = XMP_INST_DCA_FADE

# Sample flags
XMP_SAMPLE_16BIT = XMP_SAMPLE_16BIT
XMP_SAMPLE_LOOP = XMP_SAMPLE_LOOP
XMP_SAMPLE_LOOP_BIDIR = XMP_SAMPLE_LOOP_BIDIR
XMP_SAMPLE_LOOP_REVERSE = XMP_SAMPLE_LOOP_REVERSE
XMP_SAMPLE_LOOP_FULL = XMP_SAMPLE_LOOP_FULL
XMP_SAMPLE_SYNTH = XMP_SAMPLE_SYNTH

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

	def getSample(self, mod, num):
		sample = mod.xxs[num]
		buf = ctypes.cast(sample.data, POINTER(c_int8))

		if sample.flg & XMP_SAMPLE_16BIT:
			width = 2
		else:
			width = 1

		return ctypes.string_at(buf, sample.len * width)

