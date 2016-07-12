#!/bin/sh

set -e
set -x

export SDL2_PREFIX=$(pwd)/sdl2-install

test -f SDL2-2.0.4.tar.gz || wget https://www.libsdl.org/release/SDL2-2.0.4.tar.gz
rm -rf SDL2-2.0.4
tar xvf SDL2-2.0.4.tar.gz
cd SDL2-2.0.4
./configure --enable-static --disable-shared \
    --disable-joystick \
    --disable-haptic \
    --disable-power \
    --disable-loadso \
    --disable-cpuinfo \
    --disable-video-x11 \
    --disable-video-dummy \
    --disable-diskaudio \
    --disable-dummyaudio \
    --disable-render \
    --prefix=$SDL2_PREFIX
make install
cd ..

test -f SDL2_mixer-2.0.1.tar.gz || wget https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.1.tar.gz
rm -rf SDL2_mixer-2.0.1
tar xvf SDL2_mixer-2.0.1.tar.gz
cd SDL2_mixer-2.0.1
./configure --enable-static --disable-shared \
    --disable-music-cmd \
    --disable-music-mod \
    --disable-music-midi \
    --disable-music-ogg \
    --disable-music-mp3 \
    --prefix=$SDL2_PREFIX --with-sdl-prefix=$SDL2_PREFIX
make install
cd ..
