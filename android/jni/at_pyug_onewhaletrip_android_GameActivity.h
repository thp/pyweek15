#pragma once

// Initially generated via:
// javah -cp $ANDROID_HOME/platforms/android-23/android.jar:build/intermediates/classes/release \
//     at.pyug.onewhaletrip.android.GameActivity

#include <jni.h>

#ifdef __cplusplus
extern "C" {
#endif

JNIEXPORT void JNICALL Java_at_pyug_onewhaletrip_android_GameActivity_nativeStart
  (JNIEnv *, jobject, jstring);

JNIEXPORT jboolean JNICALL Java_at_pyug_onewhaletrip_android_GameActivity_nativeRender
  (JNIEnv *, jobject);

JNIEXPORT void JNICALL Java_at_pyug_onewhaletrip_android_GameActivity_nativeDestroy
  (JNIEnv *, jobject);

JNIEXPORT void JNICALL Java_at_pyug_onewhaletrip_android_GameActivity_nativeTouch
  (JNIEnv *, jobject, jint, jfloat, jfloat, jint);

#ifdef __cplusplus
}
#endif
