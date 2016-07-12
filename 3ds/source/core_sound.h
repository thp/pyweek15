#include "core_common.h"

typedef struct {
    PyObject_HEAD

    char *chunk;
    int len;
} SoundObject;

static void
sound_init()
{
    csndInit();
}

static void
Sound_dealloc(SoundObject *self)
{
    if (self->chunk) linearFree(self->chunk);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Sound_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    SoundObject *self = (SoundObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->chunk = NULL;
        self->len = 0;
    }

    return (PyObject *)self;
}

static int
Sound_init(SoundObject *self, PyObject *args, PyObject *kwargs)
{
    const char *filename;
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return -1;
    }

    int len;
    char *buf = read_file(filename, &len);
    self->chunk = linearAlloc(len);
    self->len = len;
    memcpy(self->chunk, buf, self->len);
    free(buf);

    GSPGPU_FlushDataCache(self->chunk, self->len);

    return 0;
}

static PyObject *
Sound_play(SoundObject *self)
{
    static int last_channel = 0;

    int channel = 8 + (last_channel++) % 4;
    int samplerate = 22050;

    CSND_SetPlayState(channel, 0);
    CSND_UpdateInfo(0);
    csndPlaySound(channel, SOUND_ONE_SHOT | SOUND_FORMAT_16BIT, samplerate, 0.5, 0.0, (u32 *)self->chunk, NULL, self->len);

    Py_RETURN_NONE;
}

static PyMemberDef
Sound_members[] = {
    {NULL}
};

static PyMethodDef
Sound_methods[] = {
    {"play", (PyCFunction)Sound_play, METH_NOARGS, "Play the sound effect"},
    {NULL}
};

DEFINE_TYPE(Sound);
