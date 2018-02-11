#!/bin/sh

set -x
set -e

USED_PYTHON_MINOR=3.6
USED_PYTHON_PATCH=4
USED_PYTHON_VERSION=$USED_PYTHON_MINOR.$USED_PYTHON_PATCH

if [ ! -f Python-$USED_PYTHON_VERSION.tar.xz ]; then
    wget -c https://www.python.org/ftp/python/$USED_PYTHON_VERSION/Python-$USED_PYTHON_VERSION.tar.xz
fi

tar xvf Python-$USED_PYTHON_VERSION.tar.xz

cd Python-$USED_PYTHON_VERSION

./configure --disable-ipv6 && make -j16 Parser/pgen Include/graminit.h Python/graminit.c && make clean

cat >config.site <<EOF
ac_cv_file__dev_ptmx=no
ac_cv_file__dev_ptc=no
ac_cv_lib_dl_dlopen=no
EOF

cp -fv ../../standalone/Setup.dist Modules/
cp -fv Modules/Setup.dist Modules/Setup

env CONFIG_SITE=config.site \
    ./configure --without-doc-strings --without-threads --disable-shared --disable-ipv6 \
        --host=arm-linux-androideabi \
        --build=`./config.guess`

make -j16 libpython${USED_PYTHON_MINOR}m.a
