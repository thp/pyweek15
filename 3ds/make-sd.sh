#!/bin/sh

APP="onewhaletrip_3ds"
DATADIR="onewhaletrip"
OUTDIR="sdcontent"

FILES="$APP.3dsx $APP.smdh"
OUTPUT="$OUTDIR.zip"
HERE=$(pwd)

VIRTUAL_SDMC="$HOME/.local/share/citra-emu/sdmc/"

rm -rvf $OUTDIR $OUTPUT
mkdir -pv $OUTDIR/3ds/$APP $OUTDIR/$DATADIR
cp -rpv ../data ../engine $OUTDIR/$DATADIR/
find $OUTDIR/$DATADIR -name .DS_Store -exec rm -v {} +
find $OUTDIR/$DATADIR/engine -name '*.pyc' -exec rm -v {} +
find $OUTDIR/$DATADIR/data \( -name '*.png' -o -name '*.jpg' \) -print -exec convert {} -resize '50%x50%' {} \;
find $OUTDIR/$DATADIR/data -name '*.wav' -print | while read file; do
    echo $file
    sox $file -b 16 -c 1 -r 22050 -t raw $file.raw
    mv $file.raw $file
done
make $FILES
cp $FILES $OUTDIR/3ds/$APP/
(cd $OUTDIR && zip -r ../$OUTDIR *)
rm -rvf $VIRTUAL_SDMC/$DATADIR $VIRTUAL_SDMC/3ds/$APP
(cd $VIRTUAL_SDMC && unzip "$HERE/$OUTPUT")
