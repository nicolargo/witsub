Witsub
======

Where Is The (fuck...) Subtitle

A simple command line software to automaticaly download video subtitle.
It use the [OpenSubtitles.org](http://www.opensubtitles.org/) database and its wonderfull API.

## How it work ?

Before...

	videos
	├── A wonderfull movies.avi
	├── A top serie
	│   ├── A top serie - S1E01.avi
	│   └── A top serie - S1E02.avi
	└── Not a video file.txt

Let's go...

	witsub -f ./videos

After...

	videos
	├── A wonderfull movies.avi
	├── A wonderfull movies.srt
	├── A top serie
	│   ├── A top serie - S1E01.avi
	│   ├── A top serie - S1E01.srt
	│   ├── A top serie - S1E02.avi
	│   └── A top serie - S1E02.srt
	└── Not a video file.txt

Keep it simple...

## How to install

The simple way to install Witsub is to use the PyPI package index:

	pip install witsub

or to upgrade to the latest version

	pip install --upgrade witsub

## How to use it ?

It can work with file (video file) or path (recursive to video files).

    -f <path>: Path can be video file or folder

Options:

    -v: Display version and exit
    -V: Switch on debug mode (verbose)
    -l <lang>: Set the subtitle language search (default is 'eng' for English)
               Use the ISO 639-2 standard (example 'fre' for French)
    -w: Force download and overwrite of existing subtitle
