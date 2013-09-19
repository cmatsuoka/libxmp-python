# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

def _check_range(parm, val, lower, upper):
    upper = upper - 1
    if val < lower or val > upper:
        raise LookupError(
            'Invalid {0} #{1}, valid {0} range is {2} to {3}'
            .format(parm, val ,lower, upper))

class TestInfo(struct_xmp_test_info):
    pass

class FrameInfo(struct_xmp_frame_info):
    def get_buffer(self):
        buf = ctypes.cast(self.buffer, POINTER(c_int8))
        return ctypes.string_at(buf, self.buffer_size);

class ModuleInfo(struct_xmp_module_info):
    pass

class Sample(object):
    """A sound sample

    A module sample contains raw PCM data and metadata such as word size,
    length or loop points.

    """
    def __init__(self, xxs):
        self._xxs = xxs

    def __getattr__(self, n):
        return getattr(self._xxs, n)

    def get_data(self):
        buf = ctypes.cast(self.data, POINTER(c_int8))
        if self.flg & XMP_SAMPLE_16BIT:
            return ctypes.string_at(buf, self.len * 2)
        else:
            return ctypes.string_at(buf, self.len)

class SubInstrument(object):
    """A sub-instrument

    Each instrument has one or more sub-instruments that can be mapped
    to different keys.

    """
    def __init__(self, sub):
        self._sub = sub

    def __getattr__(self, n):
        return getattr(self._sub, n)

class Envelope(object):
    """An envelope 

    Each instrument has amplitude, frequency and pan envelopes.

    """
    def __init__(self, env):
        self._env = env 

    def __getattr__(self, n):
        return getattr(self._env, n)

    def get_point(self, num):
        _check_range('envelope point', num, 0, self._env.npt)
        return (self._env.data[num * 2], self._env.data[num * 2 + 1]) 

class Instrument(object):
    """An instrument

    A module instrument contains envelope data, subinstruments and
    subinstrument mapping.

    """
    def __init__(self, xxi):
        self._xxi = xxi

    def __getattr__(self, n):
        return getattr(self._xxi, n)

    def get_envelope(self, num):
        _check_range('envelope', num, 0, 3)
        if num == Xmp.VOL_ENVELOPE:
            return Envelope(self._xxi.aei)
        elif num == Xmp.FREQ_ENVELOPE:
            return Envelope(self._xxi.fei)
        elif num == Xmp.PAN_ENVELOPE:
            return Envelope(self._xxi.pei)

    def get_subinstrument(self, num):
        _check_range('sub-instrument', num, 0, self._xxi.nsm)
        return SubInstrument(self._xxi.sub[num])

    def map_subinstrument(self, key):
        _check_range('key', key, 0, XMP_MAX_KEYS)
        return self._xxi.map[key].ins

class Player(object):

    def __init__(self, freq = 44100, mode = 0):
        self._freq = freq
        self._mode = mode
        self._ctx = xmp_create_context()

    def __del__(self):
        xmp_free_context(self._ctx)

    def get_context(self):
        return self._ctx

    def start(self, freq = -1, mode = -1):
        """Start playing the currently loaded module."""

        if freq < 0:
            freq = self._freq

        if mode < 0:
            mode = self._mode

        code = xmp_start_player(self._ctx, freq, mode)
        if code < 0:
            if code == -XMP_ERROR_INTERNAL:
                raise RuntimeError(Xmp._error[-code])
            elif code == -XMP_ERROR_INVALID:
                raise ValueError(
                    'Invalid sampling rate {0}Hz'.format(freq))
            elif code == -XMP_ERROR_SYSTEM:
                errno = get_errno()
                raise OSError(-code,
                    '{0}: {1}'.format(Xmp._error[-code], os.strerror(errno)))

    def end(self):
        """End module replay and release player memory."""
        xmp_end_player(self._ctx)

    def set(self, param, value):
        code = xmp_set_player(self._ctx, param, value)
        if code < 0:
            if code == XMP_ERROR_INVALID:
                raise ValueError('Invalid value {0}'.format(value))

    def get(self, param):
        return xmp_get_player(self._ctx, param)

    def inject_event(self, chn, event):
        xmp_inject_event(self._ctx, chn, event)

    @staticmethod
    def get_format_list():
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

    def set_instrument_path(self, path):
        return xmp_set_instrument_path(self._ctx, path)
    
    
class Module(object):
    """

    Our module.

    """
    def __init__(self, path, player = None):

        if player == None:
            player = Player()

        self._player = player
        self._ctx = player.get_context()

        code = xmp_load_module(self._ctx, path)
        if code < 0:
            if code == -XMP_ERROR_SYSTEM:
                errno = get_errno()
                raise IOError(-code, '{0}: {1}'
                    .format(Xmp._error[-code], os.strerror(errno)))
            else:
                raise IOError(-code, Xmp._error[-code])
    
        self._module_info = struct_xmp_module_info()
        xmp_get_module_info(self._ctx, pointer(self._module_info))
        self._mod = self._module_info.mod[0]

    def __del__(self):
        if Xmp.VERCODE >= 0x040000:
            if self._player.get(Xmp.PLAYER_STATE) > Xmp.STATE_UNLOADED:
                self.release()

    def __getattr__(self, n):
        return getattr(self._mod, n)

    @staticmethod
    def test(path, info = struct_xmp_test_info()):
        """Test if a file is a valid module."""
        code = xmp_test_module(path, pointer(info))
        if code == 0:
           return info
        else:
           return None

    def scan(self):
        """Scan the loaded module for sequences and timing."""
        xmp_scan_module(self._ctx)

    def release(self):
        """Release all memory used by the loaded module."""
        xmp_release_module(self._ctx)

    def play_frame(self):
        """Play one frame of the module."""
        return xmp_play_frame(self._ctx) == 0

    def play_buffer(self, size, loop = 1, buf = None):
        if buf == None:
            buf = Xmp.create_buffer(size)
        ret = xmp_play_buffer(self._ctx, buf, size, loop)
        if ret == 0:
	    return buf
	else:
	    return None

    def get_info(self, info = None):
        if info == None:
            return self._module_info
        else:
            info.__dict__.update(self._module_info.__dict__)
            return info

    def get_frame_info(self, info = FrameInfo()):
        """Retrieve current frame information."""
        xmp_get_frame_info(self._ctx, pointer(info))
        return info

    def get_instrument(self, num):
        _check_range('instrument', num, 0, self.ins)
        return Instrument(self._mod.xxi[num])

    def get_sample(self, num):
        _check_range('sample', num, 0, self.smp)
        return Sample(self._mod.xxs[num])

    def get_order(self, num):
        _check_range('position', num, 0, self.len)
        return self.xxo[num]

    def get_pattern(self, num):
        _check_range('pattern', num, 0, self.pat)
        return self.xxp[num][0]

    def get_track(self, num):
        _check_range('track', num, 0, self.trk)
        return self.xxt[num][0]

    def get_event(self, pat, row, chn):
        _check_range('pattern', pat, 0, self.pat)
        _check_range('channel', chn, 0, self.chn)
        _check_range('row', row, 0, self.get_pattern(pat).rows)
        trk = self.get_pattern(pat).index[chn]
        return self.get_track(trk).event[row]

    def get_channel(self, num):
        _check_range('track', num, 0, self.chn)
        return self.xxc[num]

class Xmp(object):
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
    PLAYER_VOLUME       = XMP_PLAYER_VOLUME
    PLAYER_STATE        = XMP_PLAYER_STATE
    PLAYER_SFX_VOLUME   = XMP_PLAYER_SFX_VOLUME

    INTERP_NEAREST      = XMP_INTERP_NEAREST
    INTERP_LINEAR       = XMP_INTERP_LINEAR
    INTERP_SPLINE       = XMP_INTERP_SPLINE

    DSP_LOWPASS         = XMP_DSP_LOWPASS
    DSP_ALL             = XMP_DSP_ALL

    STATE_UNLOADED      = XMP_STATE_UNLOADED
    STATE_LOADED        = XMP_STATE_LOADED
    STATE_PLAYING       = XMP_STATE_PLAYING

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

    VOL_ENVELOPE        = 0
    FREQ_ENVELOPE       = 1
    PAN_ENVELOPE        = 2

    # Error messages
    
    _error = [
        "No error",
        "End of module",
        "Internal error",
        "Unknown module format",
        "Can't load module",
        "Can't decompress module",
        "System error",
        "Invalid parameter"
    ]
    
    VERSION = xmp_version
    VERCODE = xmp_vercode.value
    VER_MAJOR = (VERCODE & 0xff0000) >> 16
    VER_MINOR = (VERCODE & 0x00ff00) >> 8
    VER_RELEASE = VERCODE & 0x0000ff

    # Extra convenience calls

    @staticmethod
    def create_buffer(size):
	return ctypes.create_string_buffer(size)

