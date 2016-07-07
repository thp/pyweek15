One Whale Trip
==============
Our repo needs a readme, right?!

Requirements
------------
* pygame
* docopt

To convert assets to the right size
-----------------------------------

Use: "make convert"

This requires:

* ImageMatick's "convert" utility


Building packages for MeeGo
---------------------------

First, shrink down the data in size:

* make crunch-files

Then, enter the Platform SDK using:

* scratchbox

Then cd into the right directory, and:

* dpkg-buildpackage -rfakeroot -b

After building the package, clean up:

* make undo-crunch

The "make crunch-files" step is optional, but it does help
keep the package size small:

Without crunch-files:

    ~/sdk/pyweek1209% l ../onewhaletrip_1.0.0_all.deb
    -rw-r--r-- 1 thp thp 2229646 Sep 17 10:29 ../onewhaletrip_1.0.0_all.deb

With crunch-files:

    ~/sdk/pyweek1209% l ../onewhaletrip_1.0.0_all.deb
    -rw-r--r-- 1 thp thp 990596 Sep 17 11:00 ../onewhaletrip_1.0.0_all.deb

So we got from 2.2 MB to 0.9 MB without noticeable degredation :)


TODO
====
* lepton particle engine
* many things
