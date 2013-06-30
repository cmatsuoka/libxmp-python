#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Xmp


class TestTests(unittest.TestCase):
    def test_test_module_itz(self):
        info = Xmp.test_info()
        ret = Xmp.test_module('test.itz', info)
        self.assertNotEqual(ret, None)
        self.assertEqual(info.name, 'test')
        self.assertEqual(info.type, 'Impulse Tracker (IT)')

    def test_test_module_xm(self):
        info = Xmp.test_info()
        ret = Xmp.test_module('silent-blinkys.xm', info)
        self.assertNotEqual(ret, None)
        self.assertEqual(info.name, 'Sil_Blinky Intro')
        self.assertEqual(info.type, 'Fast Tracker II (XM)')

    def test_test_module_invalid(self):
        info = Xmp.test_info()
        ret = Xmp.test_module('buffer.raw', info)
        self.assertEqual(ret, None)

class LoadTests(unittest.TestCase):
    def setUp(self):
        self.xmp = Xmp()

    def test_load_module(self):
        self.xmp.load_module('test.itz')
        mod = self.xmp.get_module_info().mod[0]
        self.assertEqual(mod.name, 'test')
        self.assertEqual(mod.len, 3)
        self.assertEqual(mod.pat, 1)
        self.assertEqual(mod.ins, 3)
        self.assertEqual(mod.smp, 2)
        self.assertEqual(mod.chn, 3)
        self.xmp.release_module()

    def test_load_module_invalid(self):
        try:
            self.xmp.load_module('buffer.raw')
        except IOError, e:
            z = e
        self.assertEqual(z.errno, Xmp.ERROR_FORMAT)

class MixerTests(unittest.TestCase):
    def setUp(self):
        self.xmp = Xmp()
        self.xmp.load_module('test.itz')
        self.xmp.start_player(44100, 0)

    def tearDown(self):
        self.xmp.end_player()
        self.xmp.release_module()

    def test_play_buffer(self):
        self.xmp.play_frame()
        fi = self.xmp.get_frame_info()
        buffer = self.xmp.get_buffer(fi)
        f = open('buffer.raw', 'rb')
        ref = f.read()
        self.assertEqual(buffer, ref)

class PlayerTests(unittest.TestCase):
    def setUp(self):
        self.xmp = Xmp()
        self.xmp.load_module('silent-blinkys.xm')
        self.xmp.start_player(44100, 0)

    def tearDown(self):
        self.xmp.end_player()
        self.xmp.release_module()

    def test_start_position(self):
        fi = self.xmp.get_frame_info()
        self.assertEqual(fi.pos, 0)

    def test_set_position(self):
        self.xmp.set_position(3)
        fi = self.xmp.get_frame_info()
        self.assertEqual(fi.pos, 3)

    def test_next_position(self):
        self.xmp.set_position(3)
        self.xmp.next_position()
        fi = self.xmp.get_frame_info()
        self.assertEqual(fi.pos, 4)
 
    def test_prev_position(self):
        self.xmp.set_position(3)
        self.xmp.prev_position()
        fi = self.xmp.get_frame_info()
        self.assertEqual(fi.pos, 2)
 
    def test_restart_module(self):
        self.xmp.set_position(3)
        self.xmp.restart_module()
        fi = self.xmp.get_frame_info()
        self.assertEqual(fi.pos, 0)

    def test_stop_module(self):
        ret = self.xmp.play_frame()
        self.assertEqual(ret, True)
        self.xmp.stop_module()
        ret = self.xmp.play_frame()
        self.assertEqual(ret, False)
 
class ModuleTests(unittest.TestCase):
    def setUp(self):
        self.xmp = Xmp()
        self.xmp.load_module('silent-blinkys.xm')
        self.mod = self.xmp.get_module()

    def tearDown(self):
        self.xmp.release_module()

    def test_get_module(self):
        self.assertEqual(self.mod.chn, 11)
        self.assertEqual(self.mod.ins, 9)
        self.assertEqual(self.mod.smp, 8)

    def test_get_instrument(self):
        inst = self.mod.get_instrument(2)
        self.assertEqual(inst.rls, 128)
        self.assertEqual(inst.aei.flg & Xmp.ENVELOPE_ON, Xmp.ENVELOPE_ON)

    def test_get_instrument_invalid(self):
        try:
            inst = self.mod.get_instrument(20)
        except Xmp.RangeError:
            z = True
        self.assertEqual(z, True)

    def test_get_subinstrument(self):
        inst = self.mod.get_instrument(2)
        sub = inst.get_subinstrument(0)
        self.assertEqual(sub.vol, 55)

    def test_get_subinstrument_invalid(self):
        try:
            inst = self.mod.get_instrument(2)
            sub = inst.get_subinstrument(2)
        except Xmp.RangeError:
            z = True
        self.assertEqual(z, True)

    def test_map_subinstrument(self):
        inst = self.mod.get_instrument(2)
        num = inst.map_subinstrument(60)
        self.assertEqual(num, 0)

    def test_get_sample(self):
        sample = self.mod.get_sample(3)
        self.assertEqual(sample.len, 64)

    def test_get_sample_invalid(self):
        try:
            sample = self.mod.get_sample(30)
        except Xmp.RangeError:
            z = True
        self.assertEqual(z, True)

if __name__ == '__main__':

    tests = [ TestTests, LoadTests, MixerTests, PlayerTests, ModuleTests ]

    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(
        [ unittest.TestLoader().loadTestsFromTestCase(i) for i in tests ]))


