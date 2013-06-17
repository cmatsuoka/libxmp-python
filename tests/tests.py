#!/usr/bin/python

import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pyxmp

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.xmp = pyxmp.Xmp()
        self.mi = pyxmp.struct_xmp_module_info()
        self.fi = pyxmp.struct_xmp_frame_info()

    def tearDown(self):
	pass

    def test_test_module(self):
        info = pyxmp.struct_xmp_test_info()
        ret = self.xmp.test_module('test.itz', info)
        self.assertEqual(ret, True)
        self.assertEqual(info.name, 'test')
        self.assertEqual(info.type, 'Impulse Tracker (IT)')

    def test_load_module(self):
        self.xmp.load_module("test.itz")
        self.xmp.get_module_info(self.mi)
        mod = self.mi.mod[0]
        self.assertEqual(mod.name, "test")
        self.assertEqual(mod.len, 3)
        self.assertEqual(mod.pat, 1)
        self.assertEqual(mod.ins, 3)
        self.assertEqual(mod.smp, 2)
        self.assertEqual(mod.chn, 3)
        self.xmp.release_module()

    def test_play_buffer(self):
        self.xmp.load_module("test.itz")
        self.xmp.start_player(44100, 0)
        self.xmp.play_frame()
        self.xmp.get_frame_info(self.fi)
        buffer = self.xmp.get_buffer(self.fi)
        f = open('buffer.raw', 'rb')
        ref = f.read()
        self.assertEqual(buffer, ref)
        self.xmp.end_player()
        self.xmp.release_module()
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)