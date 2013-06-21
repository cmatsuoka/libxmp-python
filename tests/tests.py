#!/usr/bin/python

import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyxmp import Xmp

class LoadTests(unittest.TestCase):
    def test_test_module(self):
        info = Xmp.test_info()
        ret = Xmp.test_module('test.itz', info)
        self.assertEqual(ret, True)
        self.assertEqual(info.name, 'test')
        self.assertEqual(info.type, 'Impulse Tracker (IT)')

    def test_load_module(self):
        xmp = Xmp()
        xmp.load_module("test.itz")
        mi = xmp.get_module_info()
        mod = mi.mod[0]
        self.assertEqual(mod.name, "test")
        self.assertEqual(mod.len, 3)
        self.assertEqual(mod.pat, 1)
        self.assertEqual(mod.ins, 3)
        self.assertEqual(mod.smp, 2)
        self.assertEqual(mod.chn, 3)
        xmp.release_module()

class PlayerTests(unittest.TestCase):
    def setUp(self):
	self.xmp = Xmp()
        self.xmp.load_module("test.itz")
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

        
if __name__ == '__main__':
    load_suite = unittest.TestLoader().loadTestsFromTestCase(LoadTests)
    play_suite = unittest.TestLoader().loadTestsFromTestCase(PlayerTests)
    all_tests = alltests = unittest.TestSuite([load_suite, play_suite])

    unittest.TextTestRunner(verbosity=2).run(all_tests)
