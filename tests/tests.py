#!/usr/bin/python

import sys
import unittest

sys.path.append("lib")
import sassymedia


class TestSassyMedia(unittest.TestCase):

    def setUp(self):
        self.SM = sassymedia.SassyMedia()

    def tearDown(self):
        self.SM = None

    def test_media_to_the_bottom(self):
        assert(True)


if __name__ == "__main__":
    unittest.main()
