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

from witsub.witsub import subDatabase, subTitle
from witsub.witsub import NOT_VIDEO_FILE, GET_SUB_UNKNOWN, SUB_ALREADY_EXIST
import unittest


class TestWitsubStat(unittest.TestCase):

    def setUp(self):
        self.subdatabase = subDatabase(language="eng")

    def test_Witsub_hashFile(self):
        input_file = "./testdata/breakdance.avi"
        hash_file = "8e245d9679d31e12"
        subtitle = subTitle(self.subdatabase,
                            input_file, overwrite=True)
        self.assertTrue(type(subtitle.getHashFile()) == str)
        self.assertTrue(subtitle.getHashFile() == hash_file)

    def test_Witsub_subtitleOk(self):
        input_file = "./testdata/breakdance.avi"
        output_file = "./testdata/breakdance.srt"
        subtitle = subTitle(self.subdatabase,
                            input_file, overwrite=True)
        self.assertTrue(type(subtitle.getSubtitleFileName()) == str)
        self.assertTrue(subtitle.getSubtitleFileName() == output_file)

    def test_Witsub_alreadyExist(self):
        input_file = "./testdata/breakdance.avi"
        output_file = "./testdata/breakdance.srt"
        subtitle = subTitle(self.subdatabase,
                            input_file, overwrite=True)
        subtitle = subTitle(self.subdatabase,
                            input_file, overwrite=False)
        self.assertTrue(type(subtitle.getSubtitleFileName()) == str)
        self.assertTrue(subtitle.getSubtitleFileName() == output_file)
        self.assertTrue(subtitle.subtitle == SUB_ALREADY_EXIST)

    def test_Witsub_notVideoFile(self):
        input_file = "./testdata/notvideofile"
        subtitle = subTitle(self.subdatabase,
                            input_file, overwrite=True)
        self.assertTrue(type(subtitle.subtitle == str))
        self.assertTrue(subtitle.subtitle == NOT_VIDEO_FILE)

    def test_Witsub_nonExisting(self):
        input_file = "./testdata/breakdance.avi"
        self.subdatabase.setLang("fre")
        subtitle = subTitle(self.subdatabase,
                            input_file, overwrite=True)
        self.subdatabase.setLang("eng")
        self.assertTrue(type(subtitle.getSubtitleFileName()) == str)
        self.assertTrue(subtitle.getSubtitleFileName() == "")
        self.assertTrue(subtitle.subtitle == GET_SUB_UNKNOWN)

if __name__ == '__main__':
    unittest.main()
