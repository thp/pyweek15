#include "core.h"
#include "main.h"

#include "at_pyug_onewhaletrip_android_GameActivity.h"

#include <jni.h>
#include <android/input.h>
#include <langinfo.h>
#include <string.h>

char *
nl_langinfo(nl_item item)
{
    return "UTF-8";
}

struct Global {
    char *apk_filename;
    PyObject *engine;
    PyObject *iter;
    JNIEnv *env;
    jobject activity;
    jmethodID activity_load;
    jmethodID activity_play;
} g = { NULL, NULL, NULL, NULL, 0, 0, 0 };

int
androidsound_load(const char *filename)
{
    JNIEnv *env = g.env;

    jobject jfilename = (*env)->NewStringUTF(env, filename);
    jint result = (*env)->CallIntMethod(env, g.activity, g.activity_load, jfilename);
    (*env)->DeleteLocalRef(env, jfilename);

    return result;
}

void
androidsound_play(int id)
{
    JNIEnv *env = g.env;

    (*env)->CallVoidMethod(env, g.activity, g.activity_play, (jint)id);
}

static struct TouchEvent evt;
static int set = 0;

void evt_push(struct TouchEvent *in)
{
    memcpy(&evt, in, sizeof(evt));
    set = 1;
}

int evt_pop(struct TouchEvent *out)
{
    if (set) {
        memcpy(out, &evt, sizeof(evt));
        set = 0;
        return 1;
    }

    return 0;
}

JNIEXPORT void JNICALL Java_at_pyug_onewhaletrip_android_GameActivity_nativeStart
  (JNIEnv *env, jobject self, jstring apkFilename)
{
    g.env = env;
    g.activity = (*env)->NewGlobalRef(env, self);

    jclass cls = (*env)->GetObjectClass(env, g.activity);
    g.activity_load = (*env)->GetMethodID(env, cls, "load", "(Ljava/lang/String;)I");
    g.activity_play = (*env)->GetMethodID(env, cls, "play", "(I)V");
    (*env)->DeleteLocalRef(env, cls);

    const char *tmp = (*env)->GetStringUTFChars(env, apkFilename, NULL);
    g.apk_filename = strdup(tmp);
    (*env)->ReleaseStringUTFChars(env, apkFilename, tmp);

    Py_FrozenFlag = 1;
    Py_NoSiteFlag = 1;

    char *path;
    asprintf(&path, "%s/assets", g.apk_filename);
    setenv("PYTHONPATH", path, 1);
    free(path);

#if 0
    // This can be used to debug import issues (needs android.permission.WRITE_EXTERNAL_STORAGE)

    Py_VerboseFlag = 2;

    stdout = freopen("/sdcard/owt-out.txt", "w", stdout);
    fprintf(stdout, "test [out]\n");
    fflush(stdout);
    stderr = freopen("/sdcard/owt-err.txt", "w", stderr);
    fprintf(stderr, "test [err]\n");
    fflush(stderr);
#endif

    PyImport_AppendInittab("core", PyInit_core);

    Py_Initialize();

    PyObject *core = PyImport_ImportModule("core");
    if (core) {
        PyObject *VFS = PyObject_GetAttrString(core, "VFS");
        if (VFS) {
            PyObject *result = PyObject_CallMethod(VFS, "set_zipfile", "s", g.apk_filename);
            Py_DECREF(result);
            Py_DECREF(VFS);
        } else {
            PyErr_Print();
        }
    } else {
        PyErr_Print();
    }
    Py_XDECREF(core);

    g.engine = PyImport_ImportModule("engine");

    if (g.engine) {
        g.iter = PyObject_CallMethod(g.engine, "frames", NULL);
    } else {
        PyErr_Print();
    }
}

JNIEXPORT jboolean JNICALL Java_at_pyug_onewhaletrip_android_GameActivity_nativeRender
  (JNIEnv *env, jobject self)
{
    if (g.iter != NULL) {
        PyObject *o = PyIter_Next(g.iter);
        if (o != NULL) {
            Py_XDECREF(o);
            return JNI_TRUE;
        }
    }

    return JNI_FALSE;
}

JNIEXPORT void JNICALL Java_at_pyug_onewhaletrip_android_GameActivity_nativeDestroy
  (JNIEnv *env, jobject self)
{
    free(g.apk_filename);
    (*env)->DeleteGlobalRef(env, g.activity);
    Py_XDECREF(g.iter);
    Py_XDECREF(g.engine);
    Py_Finalize();
}

JNIEXPORT void JNICALL Java_at_pyug_onewhaletrip_android_GameActivity_nativeTouch
  (JNIEnv *env, jobject self, jint action, jfloat x, jfloat y, jint finger)
{
    struct TouchEvent evt = { action, x, y, finger };
    evt_push(&evt);
}

#include "core.c"
#include "junzip.c"
