#!/usr/bin/env python

# import os
# import sys
# import glob

from setuptools import setup

data_files = [
    ('share/doc/witsub', ['AUTHORS', 'README.md'])
]

setup(
    name='witsub',
    version='1.2.1',
    description="A command line tool to download movies subtitles",
    long_description=open('README.md').read(),
    author='Nicolas Hennion',
    author_email='nicolas@nicolargo.com',
    url='https://github.com/nicolargo/witsub',
    license="LGPL",
    keywords="cli video subtitle",
    packages=['witsub'],
    include_package_data=True,
    data_files=data_files,
    # test_suite="witsub.test",
    entry_points={"console_scripts": ["witsub=witsub.witsub:main"]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities'
    ]
)
