PACKAGE := at.pyug.onewhaletrip.android
ACTIVITY := $(PACKAGE).GameActivity

all: native
	gradle build
	adb install -r build/outputs/apk/android-debug.apk
	adb shell am start -n $(PACKAGE)/$(ACTIVITY)

debug: native
	gradle build

release: native
	gradle build

native:
	ndk-build -C jni

clean:
	ndk-build -C jni clean
	gradle clean

.PHONY: all release debug native clean

