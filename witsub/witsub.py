#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Witsub
# Where Is The (fuck...) Subtitle
#
# A simple command line to search and retrieve subtitles of video files
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

__appname__ = "witsub"
__version__ = "1.0"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__licence__ = "LGPL"
# TODO: Register a dedicated user agent:
# http://trac.opensubtitles.org/projects/opensubtitles/wiki/DevReadFirst
__useragent__ = "OS Test User Agent"
__doc__ = '''\
Usage: witsub [options] -f <path>

WitSub is a command line software to automaticaly download subtitles
from the Opensubtitles.org database.


It can work with file (video file) or path (recursive to video files).

    -f <path>: Path can be video file or folder

Options:
    -v: Display version and exit
    -V: Switch on debug mode (verbose)
    -l <lang>: Set the subtitle language search (default is 'eng' for English)
               Use the ISO 639-2 standard (example 'fre' for French)
    -w: Force download and overwrite of existing subtitle
'''

# Import lib
import struct
import sys
import os
import getopt
import logging
import gzip
import base64
try:
    # Python 2
    import xmlrpclib
except:
    # Python 3
    import xmlrpc.client
try:
    # Python 2
    import StringIO
except:
    # Python 3
    import io

# Global variables
HASH_SIZE_ERROR = "HashSizeError"
GET_SUB_ERROR = "RequestError"
GET_DWNL_ERROR = "DownloadError"
GET_SUB_UNKNOWN = "None"
SUB_ALREADY_EXIST = "SubAlreadyExist"
NOT_VIDEO_FILE = "NotVideoFile"

# Video extensions list
VIDEO_EXT = ('.3g2', '.3gp', '.3gp2', '.3gpp', '.60d', '.ajp', '.asf',
             '.asx', '.avchd', '.avi', '.bik', '.bix', '.box', '.cam',
             '.dat', '.divx', '.dmf', '.dv', '.dvr-ms', '.evo', '.flc',
             '.fli', '.flic', '.flv', '.flx', '.gvi', '.gvp', '.h264',
             '.m1v', '.m2p', '.m2ts', '.m2v', '.m4e', '.m4v', '.mjp',
             '.mjpeg', '.mjpg', '.mkv', '.moov', '.mov', '.movhd',
             '.movie', '.movx', '.mp4', '.mpe', '.mpeg', '.mpg', '.mpv',
             '.mpv2', '.mxf', '.nsv', '.nut', '.ogg', '.ogm', '.omf',
             '.ps', '.qt', '.ram', '.rm', '.rmvb', '.swf', '.ts', '.vfw',
             '.vid', '.video', '.viv', '.vivo', '.vob', '.vro', '.wm',
             '.wmv', '.wmx', '.wrap', '.wvx', '.wx', '.x264', '.xvid')


# Classes
class subDatabase(object):
    """
    Class used to configure the access to the subtitle database
    """

    def __init__(self, language="eng"):
        self.lang = language
        self.rpc_server = None
        self.rpc_login = None
        self.connect()
        self.login()

    def __del__(self):
        self.logout()

    def open(self):
        if self.rpc_server is None:
            self.connect()
        if self.rpc_login is None:
            self.login()

    def close(self):
        self.logout()
        self.rpc_server = None
        self.rpc_login = None

    def connect(self):
        # Connect to the Opensubtitles XML/RPC API
        XMLRPC_SERVER = "http://api.opensubtitles.org/xml-rpc"
        logging.debug("Connect to XML-RPC server %s" % XMLRPC_SERVER)
        try:
            if sys.version_info > (3, 0):
                rpc_server = xmlrpc.client.Server(XMLRPC_SERVER)
            else:
                rpc_server = xmlrpclib.Server(XMLRPC_SERVER)
        except Exception as msg:
            logging.error("%s" % msg)
            return None

        self.rpc_server = rpc_server
        return rpc_server

    def login(self):
        # Check if you are connected/loggedin
        if (self.rpc_server is None):
            logging.error("Should be connected before login")
            return None

        # Login to Opensubtitles XML/RPC API
        logging.debug("Login to XML-RPC server %s" % self.rpc_server)
        try:
            self.rpc_login = self.rpc_server.LogIn("", "",
                                                   self.lang,
                                                   __useragent__)
        except Exception as msg:
            logging.error("%s" % msg)
            return None
        else:
            if (self.rpc_login["status"] != "200 OK"):
                # Login Error
                logging.error("Can not login to XML-RPC server (error: %s)"
                              % self.rpc_login["status"])
                return None

        # Login OK
        logging.debug("Login successfull with status %s"
                      % self.rpc_login["status"])

        return self.rpc_login

    def search(self, searchlist):
        # Check if you are connected/loggedin
        if (self.rpc_login is None):
            logging.error("Should be loggedin before searching")
            return None

        # Search in the subtitles database
        logging.debug("Search subtitle in the database")
        try:
            rpc = self.rpc_server.SearchSubtitles(self.rpc_login["token"],
                                                  searchlist)
        except Exception as msg:
            logging.error("%s" % msg)
            return None

        if (rpc["status"] != "200 OK"):
            # Search error
            logging.error("Search return an error (error: %s)"
                          % rpc["status"])
            return None

        logging.debug("Search done in %s seconds" % rpc["seconds"])

        return rpc

    def download(self, winner):

        winner_url = winner["SubDownloadLink"]
        winner_id = winner["IDSubtitleFile"]

        logging.debug("Download the compressed subtitle file (id %s): %s"
                      % (winner_id, winner_url))
        try:
            rpc = self.rpc_server.DownloadSubtitles(self.rpc_login["token"],
                                                    [winner_id])
        except Exception as msg:
            logging.error("%s" % msg)
            return GET_DWNL_ERROR

        if not rpc["status"].startswith("20") or rpc["data"] == '':
            # Download error
            logging.error("Download error (error: %s)"
                          % rpc["status"])
            return GET_DWNL_ERROR

        logging.debug("Download processed in %s seconds"
                      % (rpc["seconds"]))

        return rpc

    def logout(self):
        # Logout from Opensubtitles XML/RPC API
        try:
            logging.debug("Logout from XML-RPC server %s" % self.rpc_server)
            rpc = self.rpc_server.LogOut(self.rpc_login["token"])
        except Exception as msg:
            logging.error("%s" % msg)
            return None

        if (rpc["status"] != "200 OK"):
            # Logout Error
            logging.error("Can not logout from XML-RPC server (error: %s)"
                          % rpc["status"])
            return None

        # Logout OK
        logging.debug("Logout successfull with status %s"
                      % rpc["status"])


class subTitle(object):
    """
    Main class to manage subtitle
    """

    def __init__(self, subdatabase, videofilename, overwrite=False):
        self.videofilename = videofilename
        if (not videofilename.endswith(VIDEO_EXT)):
            # Only manage video file
            logging.debug("%s is not a video file", videofilename)
            self.subtitle = NOT_VIDEO_FILE
            return None
        self.videofilesize = os.path.getsize(videofilename)
        self.subtitlefilename = self.__fileBase__(videofilename)
        # Test if subtitle already exist...
        if os.path.exists(self.subtitlefilename) and not overwrite:
            logging.info("Subtitle already exist: %s", self.subtitlefilename)
            self.subtitle = SUB_ALREADY_EXIST
        else:
            # No file detected, can start working
            self.hash = self.__hashFile__()
            if self.hash != HASH_SIZE_ERROR:
                self.subdatabase = subdatabase
                self.searchlist = [({'sublanguageid': self.subdatabase.lang,
                                    'moviehash': self.hash,
                                    'moviebytesize': str(self.videofilesize)})]
                self.subtitle = self.__getSubTitle__()
            else:
                self.subtitle = HASH_SIZE_ERROR

    def getVideoFileName(self):
        return self.videofilename

    def getHashFile(self):
        try:
            self.hash
        except:
            return HASH_SIZE_ERROR
        else:
            return self.hash

    def getSubtitleFileName(self):
        if type(self.subtitle) == type(dict()):
            return self.subtitlefilename
        else:
            return ""

    def __hashFile__(self):
        """
        Return the Opensubtitles hash code
        """

        logging.debug("Compute hash tag for file %s" % self.videofilename)

        longlongformat = 'q'
        bytesize = struct.calcsize(longlongformat)

        f = open(self.videofilename, "rb")

        filesize = os.path.getsize(self.videofilename)
        hash = filesize

        if filesize < 65536 * 2:
            logging.error("Bad file size for %s (%s bytes), can't compute hash"
                          % (self.videofilename, filesize))
            return HASH_SIZE_ERROR

        for x in range(int(65536 / bytesize)):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
        hash = hash & 0xFFFFFFFFFFFFFFFF

        f.seek(max(0, filesize - 65536), 0)
        for x in range(int(65536 / bytesize)):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash = "%016x" % hash

        logging.debug("Hash tag for file %s is %s" % (self.videofilename,
                                                      hex(hash)))

        return returnedhash

    def __getSubTitle__(self):
        """
        Get the subtitle from the Opensubtitles database
        """

        # Search in the subtitles database
        rpc_search = self.subdatabase.search(self.searchlist)

        # Analyse and download the best subtitle
        ret_subtitle = self.__chooseSubTitle__(rpc_search["data"])
        if ret_subtitle != GET_SUB_UNKNOWN:
            # Download the subtitle
            ret_subtitle = self.__downloadSubtitle__(ret_subtitle)

        # Return the subtitle candidate
        return ret_subtitle

    def __chooseSubTitle__(self, rpcdata):
        """
        Internal algo to choose "best" subtitle
        """

        # No subtitle found with the first method
        if not rpcdata:
            logging.debug("No subtitle found")
            # TODO: If not find, try the 2e method: http://alturl.com/kef8a
            return GET_SUB_UNKNOWN

        # One subtitle match: Easy !
        if len(rpcdata) == 1:
            logging.debug("One subtitle found (%s): %s"
                          % (rpcdata[0]["LanguageName"],
                             rpcdata[0]["SubFileName"]))
        else:
            # More than one subtitles match
            logging.debug("%s subtitles found" % (len(rpcdata)))

            # Display all subtitle (for debug purpose)
            for i in range(len(rpcdata)):
                logging.debug("Subtitle %s/%s (%s - Dwnl: %s): %s"
                              % (i + 1, len(rpcdata),
                                 rpcdata[i]["LanguageName"],
                                 rpcdata[i]["SubDownloadsCnt"],
                                 rpcdata[i]["SubFileName"]))

            # Return the most downloaded (default sort)
            logging.debug("Select the first one (most downloaded): %s"
                          % (rpcdata[0]["SubFileName"]))

        # Return the winner
        return rpcdata[0]

    def __downloadSubtitle__(self, rpcwinner):
        """
        Download the subtitle
        """

        # Download the subtitle file (compressed in gz)
        rpc_dwnl = self.subdatabase.download(rpcwinner)
        try:
            rpc_dwnl["data"][0]["data"]
        except:
            logging.error("Download error")
            return GET_DWNL_ERROR

        # Unzip the downloaded file
        logging.debug("Unzip the compressed subtitle file")
        subt_str = self.__gunzip__(rpc_dwnl["data"][0]["data"])

        # Put the result in the .str file
        logging.debug("Write the subtitle to %s"
                      % self.subtitlefilename)
        try:
            open(self.subtitlefilename, 'wb').write(subt_str)
        except Exception as msg:
            logging.error("Can not write to %s (error: %s)"
                          % (self.subtitlefilename, msg))
            return GET_DWNL_ERROR

        # Done
        logging.info("Download completed: %s"
                     % self.subtitlefilename)

        return rpcwinner

    def __gunzip__(self, data):
        data = base64.decodestring(data.encode('ascii'))
        if sys.version_info > (3, 0):
            # Python 3
            ret = gzip.GzipFile(fileobj=io.BytesIO(data)).read()
        else:
            # Python 2
            ret = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
        return ret

    def __fileBase__(self, filename, newext="srt"):
        return filename[:filename.rfind('.')] + "." + newext


def printSyntax():
    """
    Display the syntax of the command line
    """
    print(__doc__)


def printVersion():
    """
    Display the current software version
    """
    print(__appname__ + " version " + __version__)


def main():
    """
    Main function: manage CLI
    """

    global _DEBUG_
    _DEBUG_ = False

    # Manage args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhVwf:l:")
    except getopt.GetoptError as err:
        # Print help information and exit:
        print("Error: " + str(err))
        printSyntax()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-v"):
            printVersion()
            sys.exit(0)
        elif opt in ("-h"):
            printVersion()
            printSyntax()
            sys.exit(0)
        elif opt in ("-V"):
            _DEBUG_ = True
            # Verbose mode is ON
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s - %(message)s',
                datefmt='%d/%m/%Y %H:%M:%S',
            )
        elif opt in ("-w"):
            arg_overwrite = True
        elif opt in ("-f"):
            arg_file = arg
        elif opt in ("-l"):
            arg_lang = arg
        else:
            printSyntax()
            sys.exit(0)

    # By default verbose mode is OFF
    if not _DEBUG_:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
        )
    logging.debug("Running %s version %s" % (__appname__, __version__))
    logging.debug("Debug mode is ON")

    # Test args
    try:
        # Test overwrite
        arg_overwrite
    except:
        arg_overwrite = False

    logging.debug("Force overwrite if file exist: %s" % arg_overwrite)

    try:
        # Test language
        arg_lang
    except:
        arg_lang = "eng"
        logging.debug("No language define. Default is %s" % arg_lang)

    logging.debug("Subtitle language search set to %s" % arg_lang)

    try:
        # Test input video file or folder
        arg_file
    except:
        logging.critical("Need an input file or folder (use the -f <path>)")
        printSyntax()
        sys.exit(2)

    # Create the connection with the subtitle database
    # Only one connection for all the request
    subdatabase = subDatabase(arg_lang)

    # Get the subtitle for each video file
    arg_file = os.path.normpath(arg_file)
    if os.path.isdir(arg_file):
        # User provides a folder
        logging.debug("%s is a folder. Scan into." % arg_file)

        # Recursive scan
        for root, dirs, files in os.walk(arg_file):
            for input_file in files:
                input_file = root + os.sep + input_file
                # Let's go...
                subTitle(subdatabase, input_file, overwrite=arg_overwrite)
    else:
        # User provides a single file
        try:
            with open(arg_file):
                pass
        except IOError:
            logging.critical("Can not read input file or folder %s" % arg_file)
            sys.exit(2)

        # Let's go...
        subTitle(subdatabase, arg_file, overwrite=arg_overwrite)

# Main
#=====

if __name__ == "__main__":
    main()

# The end...
