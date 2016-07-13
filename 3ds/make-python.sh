#!/bin/sh

set -x
set -e

export PATH=$PATH:$HOME/pkg/devkitPro/devkitARM/bin

./configure && make Parser/pgen Include/graminit.h Python/graminit.c clean

patch -p1 <<EOF
make Makefile
--- Python-2.7.12/configure	2016-06-25 23:49:32.000000000 +0200
+++ Python-2.7.12-3ds/configure	2016-07-11 16:03:58.000000000 +0200
@@ -3213,7 +3213,7 @@
        # \`define_xopen_source' in the case statement below. For the
        # current supported cross builds, this macro is not adjusted.
 	case "\$host" in
-	*-*-linux*)
+	*-*-linux*|arm-none-eabi)
 		ac_sys_system=Linux
 		;;
 	*-*-cygwin*)
@@ -3253,7 +3253,7 @@
 
 if test "\$cross_compiling" = yes; then
 	case "\$host" in
-	*-*-linux*)
+	*-*-linux*|arm-none-eabi)
 		case "\$host_cpu" in
 		arm*)
 			_host_cpu=arm
EOF

cat >config.site <<EOF
ac_cv_file__dev_ptmx=no
ac_cv_file__dev_ptc=no
ac_cv_lib_dl_dlopen=no
EOF

# Do not build in any modules
rm -f Modules/Setup Modules/Setup.dist
touch Modules/Setup.dist

env CFLAGS="-march=armv6k -mtune=mpcore -mfloat-abi=hard -mtp=soft -fomit-frame-pointer -ffunction-sections -DARM11 -D_3DS" \
    LDFLAGS="-march=armv6k -mtune=mpcore -mfloat-abi=hard -mtp=soft" \
    CONFIG_SITE=config.site \
    ./configure --without-doc-strings --without-threads --disable-shared --host=arm-none-eabi --build=`./config.guess`

make libpython2.7.a
