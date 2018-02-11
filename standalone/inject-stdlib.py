#!/usr/bin/env python3

import zipfile
import os
import argparse

parser = argparse.ArgumentParser(description='Inject a list of files into a ZIP file')
parser.add_argument('filelist', help='List of files to inject')
parser.add_argument('srcdir', help='Source directory from where to copy files')
parser.add_argument('zipfile', help='Zipfile to copy files into')
args = parser.parse_args()

filenames = {filename: os.path.join(args.srcdir, filename) for filename in open(args.filelist).read().split()}

with zipfile.ZipFile(args.zipfile, 'a') as zfp:
    for arcfilename, filename in filenames.items():
        print('  adding:', arcfilename)
        zfp.write(filename, arcfilename)
