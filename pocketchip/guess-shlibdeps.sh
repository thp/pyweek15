#!/bin/sh
# Guess shared library dependencies

objdump -x onewhaletrip | \
    awk '/^\s*NEEDED/ { print "*/" $2 }' | \
    xargs -n1 dpkg -S | \
    cut -d: -f1 | \
    sort -u | \
    paste -d, -s | \
    sed -e 's/,/, /g'
