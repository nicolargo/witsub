#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Witsub unitary test
#
# Copyright (C) 2013 Nicolargo <nicolas@nicolargo.com>
#
# Witsub is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Witsub is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Sample from the OpenSubtitles wiki
# http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes


import unittest
import witsub


class TestWitsubStat(unittest.TestCase):

    def setUp(self):
        self.subdatabase = witsub.subDatabase(language="eng")

    def test_Witsub_hashFile(self):
        input_file = "./testdata/breakdance.avi"
        hash_file = "8e245d9679d31e12"
        subtitle = witsub.subTitle(self.subdatabase,
                                   input_file, overwrite=True)
        self.assertTrue(type(subtitle.getHashFile()) == str)
        self.assertTrue(subtitle.getHashFile() == hash_file)

    def test_Witsub_notVideoFile(self):
        input_file = "./testdata/notvideofile"
        subtitle = witsub.subTitle(self.subdatabase,
                                   input_file, overwrite=True)
        self.assertTrue(type(subtitle.subtitle == str))
        self.assertTrue(subtitle.subtitle == witsub.NOT_VIDEO_FILE)

    def test_Witsub_getSubtitleFileName(self):
        input_file = "./testdata/breakdance.avi"
        output_file = "./testdata/breakdance.srt"
        subtitle = witsub.subTitle(self.subdatabase,
                                   input_file, overwrite=True)
        self.assertTrue(type(subtitle.getSubtitleFileName()) == str)
        self.assertTrue(subtitle.getSubtitleFileName() == output_file)

if __name__ == '__main__':
    unittest.main()
