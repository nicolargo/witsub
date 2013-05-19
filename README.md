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