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

    def _run_match_test(self, test_folder, message=None):
        # Get CSS input
        fh = open("tests/%s/input.css" % test_folder, "r")
        input_ = fh.read()
        fh.close()
        # Get expected output
        fh = open("tests/%s/expected.css" % test_folder, "r")
        expected = fh.read()
        fh.close()
        # Run input through Sassy Media
        self.SM.contents = input_
        self.SM.run()
        # Test against expected output
        try:
            self.assertEqual(self.SM.contents, expected, message)
        except AssertionError, e:
            print self.SM.contents
            raise e

    def test_is_class(self):
        self.assertIsInstance(self.SM, sassymedia.SassyMedia,
            "Instance does not match class.")

    def test_no_media_query(self):
        self._run_match_test("no_media_query")

    def test_single_query_at_end(self):
        self._run_match_test("single_query_at_end")

    def test_single_query_at_beginning(self):
        self._run_match_test("single_query_at_beginning")


if __name__ == "__main__":
    unittest.main()
