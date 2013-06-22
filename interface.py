
class Xmp:
    """A multi format module player

    Xmp implements a full-featured module player that supports
    many different module formats including Protracker MOD, Scream
    Tracker III S3M, Fast Tracker II XM and Impulse Tracker IT modules.

    """

    # Constants

    NAME_SIZE           = XMP_NAME_SIZE

    KEY_OFF             = XMP_KEY_OFF
    KEY_CUT             = XMP_KEY_CUT
    KEY_FADE            = XMP_KEY_FADE

    FORMAT_8BIT         = XMP_FORMAT_8BIT
    FORMAT_UNSIGNED     = XMP_FORMAT_UNSIGNED
    FORMAT_MONO         = XMP_FORMAT_MONO

    PLAYER_AMP          = XMP_PLAYER_AMP
    PLAYER_MIX          = XMP_PLAYER_MIX
    PLAYER_INTERP       = XMP_PLAYER_INTERP
    PLAYER_DSP          = XMP_PLAYER_DSP
    PLAYER_FLAGS        = XMP_PLAYER_FLAGS
    PLAYER_CFLAGS       = XMP_PLAYER_CFLAGS 
    PLAYER_SMPCTL       = XMP_PLAYER_SMPCTL

    INTERP_NEAREST      = XMP_INTERP_NEAREST
    INTERP_LINEAR       = XMP_INTERP_LINEAR
    INTERP_SPLINE       = XMP_INTERP_SPLINE

    DSP_LOWPASS         = XMP_DSP_LOWPASS
    DSP_ALL             = XMP_DSP_ALL

    FLAGS_VBLANK        = XMP_FLAGS_VBLANK
    FLAGS_FX9BUG        = XMP_FLAGS_FX9BUG
    FLAGS_FIXLOOP       = XMP_FLAGS_FIXLOOP

    SMPCTL_SKIP         = XMP_SMPCTL_SKIP

    MAX_KEYS            = XMP_MAX_KEYS
    MAX_ENV_POINTS      = XMP_MAX_ENV_POINTS
    MAX_MOD_LENGTH      = XMP_MAX_MOD_LENGTH
    MAX_CHANNELS        = XMP_MAX_CHANNELS
    MAX_SRATE           = XMP_MAX_SRATE
    MIN_SRATE           = XMP_MIN_SRATE
    MIN_BPM             = XMP_MIN_BPM
    MAX_FRAMESIZE       = XMP_MAX_FRAMESIZE

    END                 = XMP_END
    ERROR_INTERNAL      = XMP_ERROR_INTERNAL
    ERROR_FORMAT        = XMP_ERROR_FORMAT
    ERROR_LOAD          = XMP_ERROR_LOAD
    ERROR_DEPACK        = XMP_ERROR_DEPACK
    ERROR_SYSTEM        = XMP_ERROR_SYSTEM
    ERROR_INVALID       = XMP_ERROR_INVALID

    CHANNEL_SYNTH       = XMP_CHANNEL_SYNTH
    CHANNEL_MUTE        = XMP_CHANNEL_MUTE

    ENVELOPE_ON         = XMP_ENVELOPE_ON
    ENVELOPE_SUS        = XMP_ENVELOPE_SUS
    ENVELOPE_LOOP       = XMP_ENVELOPE_LOOP
    ENVELOPE_FLT        = XMP_ENVELOPE_FLT
    ENVELOPE_SLOOP      = XMP_ENVELOPE_SLOOP
    ENVELOPE_CARRY      = XMP_ENVELOPE_CARRY

    INST_NNA_CUT        = XMP_INST_NNA_CUT
    INST_NNA_CONT       = XMP_INST_NNA_CONT
    INST_NNA_OFF        = XMP_INST_NNA_OFF
    INST_NNA_FADE       = XMP_INST_NNA_FADE
    INST_DCT_OFF        = XMP_INST_DCT_OFF
    INST_DCT_NOTE       = XMP_INST_DCT_NOTE
    INST_DCT_SMP        = XMP_INST_DCT_SMP
    INST_DCT_INST       = XMP_INST_DCT_INST
    INST_DCA_CUT        = XMP_INST_DCA_CUT
    INST_DCA_OFF        = XMP_INST_DCA_OFF
    INST_DCA_FADE       = XMP_INST_DCA_FADE

    SAMPLE_16BIT        = XMP_SAMPLE_16BIT
    SAMPLE_LOOP         = XMP_SAMPLE_LOOP
    SAMPLE_LOOP_BIDIR   = XMP_SAMPLE_LOOP_BIDIR
    SAMPLE_LOOP_REVERSE = XMP_SAMPLE_LOOP_REVERSE
    SAMPLE_LOOP_FULL    = XMP_SAMPLE_LOOP_FULL
    SAMPLE_SYNTH        = XMP_SAMPLE_SYNTH

    PERIOD_BASE         = XMP_PERIOD_BASE

    # Error messages

    _error = [
        "No error",
        "End of module",
        "Internal error",
        "Can't load module",
        "Can't decompress module",
        "System error",
        "Invalid parameter"
    ]

    # Regular C API calls for libxmp 4.1

    def __init__(self):
        self._ctx = xmp_create_context()

    def __del__(self):
        xmp_free_context(self._ctx)

    def load_module(self, path):
        """Load a module file."""
        code = xmp_load_module(self._ctx, path)
        if code < 0:
            #raise IOError(code, os.strerror(code))
            raise IOError(-code, self._error[-code])
    
    @staticmethod
    def test_module(path, info):
        """Test if a file is a valid module."""
        code = xmp_test_module(path, pointer(info))
        return (code == 0)

    def scan_module(self):
        """Scan the loaded module for sequences and timing."""
        xmp_scan_module(self._ctx)

    def release_module(self):
        """Release all memory used by the loaded module."""
        xmp_release_module(self._ctx)

    def start_player(self, freq, mode = 0):
        """Start playing the currently loaded module."""
        return xmp_start_player(self._ctx, freq, mode)

    def play_frame(self):
        """Play one frame of the module."""
        return xmp_play_frame(self._ctx) == 0

    def play_buffer(self, size, loop = 1, buf = None):
        if buf == None:
            buf = self.buffer(size)
        ret = xmp_play_buffer(self._ctx, buf, size, loop)
        if ret == 0:
		return buf
	else:
		return None

    def get_frame_info(self, info = struct_xmp_frame_info()):
        """Retrieve current frame information."""
        xmp_get_frame_info(self._ctx, pointer(info))
        return info

    def end_player(self):
        """End module replay and release player memory."""
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
        """Skip replay to the start of the next position."""
        return xmp_next_position(self._ctx)

    def prev_position(self):
        """Skip replay to the start of the previous position."""
        return xmp_prev_position(self._ctx)

    def set_position(self, num):
        """Skip replay to the start of the given position."""
        return xmp_set_position(self._ctx, num)

    def stop_module(self):
        """Stop the currently playing module."""
        xmp_stop_module(self._ctx)

    def restart_module(self):
        """Restart the currently playing module."""
        xmp_restart_module(self._ctx)

    def seek_time(self, time):
        """Skip replay to the specified time."""
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
    def buffer(size):
	return ctypes.create_string_buffer(size)

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

