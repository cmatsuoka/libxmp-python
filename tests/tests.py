#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import *


class SetupTests(unittest.TestCase):
    def test_test_module_itz(self):
        info = Module.test('test.itz')
        self.assertNotEqual(info, None)
        self.assertEqual(info.name, 'test')
        self.assertEqual(info.type, 'Impulse Tracker (IT)')

    def test_test_module_xm(self):
        info = Module.test('silent-blinkys.xm')
        self.assertNotEqual(info, None)
        self.assertEqual(info.name, 'Sil_Blinky Intro')
        self.assertEqual(info.type, 'Fast Tracker II (XM)')

    def test_test_module_invalid(self):
        info = Module.test('buffer.raw')
        self.assertEqual(info, None)

    def test_start_player(self):
        player = Player()
        mod = Module('test.itz', player)
        try:
            player.start(Xmp.MAX_SRATE + 1)
        except ValueError:
            z = True
        self.assertTrue(z)


class LoadTests(unittest.TestCase):

    def test_load_module(self):
        mod = Module('test.itz')
        self.assertEqual(mod.name, 'test')
        self.assertEqual(mod.len, 3)
        self.assertEqual(mod.pat, 1)
        self.assertEqual(mod.ins, 3)
        self.assertEqual(mod.smp, 2)
        self.assertEqual(mod.chn, 3)
        mod.release()

    def test_load_module_invalid(self):
        try:
            mod = Module('buffer.raw')
        except IOError, e:
            z = e
        self.assertEqual(z.errno, Xmp.ERROR_FORMAT)

    def test_load_module_missing(self):
        try:
            mod = Module('not.there')
        except IOError, e:
            z = e
        self.assertEqual(z.errno, Xmp.ERROR_SYSTEM)


class MixerTests(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.mod = Module('test.itz', self.player)
        self.player.start(44100, 0)

    def tearDown(self):
        self.player.end()
        self.mod.release()

    def test_play_buffer(self):
        self.mod.play_frame()
        fi = self.mod.get_frame_info()
        buffer = fi.get_buffer()
        f = open('buffer.raw', 'rb')
        ref = f.read()
        self.assertEqual(buffer, ref)

class PlayerTests(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.mod = Module('silent-blinkys.xm', self.player)
        self.player.start(44100, 0)

    def tearDown(self):
        self.player.end()
        self.mod.release()

    def test_start_position(self):
        fi = self.mod.get_frame_info()
        self.assertEqual(fi.pos, 0)

    def test_set_position(self):
        self.player.set_position(3)
        fi = self.mod.get_frame_info()
        self.assertEqual(fi.pos, 3)

    def test_next_position(self):
        self.player.set_position(3)
        self.player.next_position()
        fi = self.mod.get_frame_info()
        self.assertEqual(fi.pos, 4)
 
    def test_prev_position(self):
        self.player.set_position(3)
        self.player.prev_position()
        fi = self.mod.get_frame_info()
        self.assertEqual(fi.pos, 2)
 
    def test_restart_module(self):
        self.player.set_position(3)
        self.player.restart_module()
        fi = self.mod.get_frame_info()
        self.assertEqual(fi.pos, 0)

    def test_stop_module(self):
        ret = self.mod.play_frame()
        self.assertTrue(ret)
        self.player.stop_module()
        ret = self.mod.play_frame()
        self.assertFalse(ret)
 
class ModuleTests(unittest.TestCase):
    def setUp(self):
        self.mod = Module('silent-blinkys.xm')

    def tearDown(self):
        self.mod.release()

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
        except LookupError:
            z = True
        self.assertTrue(z)

    def test_get_envelope(self):
        inst = self.mod.get_instrument(2)
        env = inst.get_envelope(Xmp.VOL_ENVELOPE)
        self.assertEqual(env.npt, 4)

    def test_get_subinstrument(self):
        inst = self.mod.get_instrument(2)
        sub = inst.get_subinstrument(0)
        self.assertEqual(sub.vol, 55)

    def test_get_subinstrument_invalid(self):
        try:
            inst = self.mod.get_instrument(2)
            sub = inst.get_subinstrument(2)
        except LookupError:
            z = True
        self.assertTrue(z)

    def test_map_subinstrument(self):
        inst = self.mod.get_instrument(2)
        num = inst.map_subinstrument(60)
        self.assertEqual(num, 0)

    def test_map_subinstrument_invalid(self):
        inst = self.mod.get_instrument(2)
        try:
            num = inst.map_subinstrument(Xmp.MAX_KEYS)
        except LookupError:
            z = True
        self.assertTrue(z)

    def test_get_sample(self):
        sample = self.mod.get_sample(3)
        self.assertEqual(sample.len, 64)

    def test_get_sample_invalid(self):
        try:
            sample = self.mod.get_sample(30)
        except LookupError:
            z = True
        self.assertTrue(z)

    def test_get_order(self):
        pos = self.mod.get_order(2)
        self.assertEqual(pos, 2)
        pos = self.mod.get_order(3)
        self.assertEqual(pos, 1)

    def test_get_order_invalid(self):
        try:
            pos = self.mod.get_order(10)
        except LookupError:
            z = True
        self.assertTrue(z)

if __name__ == '__main__':

    tests = [ SetupTests, LoadTests, MixerTests, PlayerTests, ModuleTests ]

    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(
        [ unittest.TestLoader().loadTestsFromTestCase(i) for i in tests ]))


