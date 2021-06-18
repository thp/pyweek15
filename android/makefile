PACKAGE := at.pyug.onewhaletrip.android
ACTIVITY := $(PACKAGE).GameActivity

GRADLE ?= ./gradlew

all: native
	$(GRADLE) assembleDebug
	adb install -r build/outputs/apk/debug/android-debug.apk
	adb shell am start -n $(PACKAGE)/$(ACTIVITY)

debug: native
	$(GRADLE) assembleDebug

release: native
	$(GRADLE) assembleRelease

native: Python-3.8.10/libpython3.8.a
	ndk-build -C jni

Python-3.8.10/libpython3.8.a:
	sh cross-compile-libpython.sh

clean:
	ndk-build -C jni clean
	$(GRADLE) clean

.PHONY: all release debug native clean

