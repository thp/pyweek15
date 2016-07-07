#!/usr/bin/env python
import os
import sys

pfm = sys.platform
cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cwd)

name = "OneWhaleTrip"

# build
path2build = {}
path2build["darwin"] = "~/bin/pyinstaller/utils/"
path2build["win32"] = "Y:\\bin\\pyinstaller\\utils\\"

command = "python %sBuild.py --noconfirm %s.spec" % (path2build[pfm], pfm)

os.system(command)

# # prepare
# d = os.path.join("..", 'dist')
# if not os.path.exists(d):
#     os.makedirs(d)

# # distribute
# if pfm == 'darwin':
#     os.system("rm -rf ../dist/%s.app" % name)
#     os.system("mv dist/%s.app ../dist/" % name)
# else:
#     os.system("rm -rf ../dist/%s" % name)
#     os.system("mv dist/%s ../dist/" % name)
