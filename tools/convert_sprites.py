#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import os
import sys
import subprocess

HERE = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(HERE, '..', 'assets')
OUTPUT_DIR = os.path.join(HERE, '..', 'data', 'sprites')
MAPPING_FILE = os.path.join(HERE, 'convert_sprites.in')

input_files = [
    glob.glob(os.path.join(ASSETS_DIR, '*.jpg')),
    glob.glob(os.path.join(ASSETS_DIR, '*.png')),
]

input_files = [os.path.basename(y) for x in input_files for y in x]

current_resolution = None

for line in open(MAPPING_FILE):
    filename = line.strip()
    if not filename:
        continue

    if filename.endswith(':'):
        current_resolution = int(filename[:-1])
        continue

    if filename in input_files:
        input_files.remove(filename)
        source_filename = os.path.join(ASSETS_DIR, filename)
        target_filename = os.path.join(OUTPUT_DIR, filename)
        target_resolution = '%dx%s' % (current_resolution, current_resolution)

        if not os.path.exists(target_filename):
            print >>sys.stderr, source_filename, '=>', target_filename
            process = subprocess.Popen(['convert', source_filename, '-resize',
                target_resolution, target_filename])
            if process.wait() != 0:
                print >>sys.stderr, '[WARNING] Could not convert:', filename

        continue

    print >>sys.stderr, '[WARNING] File not found:', filename


if input_files:
    print >>sys.stderr, '[WARNING] Unused files found (add them to %s):' % MAPPING_FILE
    for filename in input_files:
        print >>sys.stderr, ' - ', filename

