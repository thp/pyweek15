#include "core_common.h"

#include <SDL_mixer.h>

typedef struct {
    PyObject_HEAD

    Mix_Chunk *chunk;
} SoundObject;

static void
Sound_dealloc(SoundObject *self)
{
    Mix_FreeChunk(self->chunk);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Sound_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    SoundObject *self = (SoundObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->chunk = NULL;
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

    static int sound_inited = 0;
    if (!sound_inited) {
        Mix_Init(0);
        Mix_OpenAudio(MIX_DEFAULT_FREQUENCY, AUDIO_S16LSB, 2, 1024);
        sound_inited = 1;
    }

    int len;
    char *buf = read_file(filename, &len);
    self->chunk = Mix_LoadWAV_RW(SDL_RWFromConstMem(buf, len), 1);
    free(buf);

    return 0;
}

static PyObject *
Sound_play(SoundObject *self)
{
    Mix_PlayChannel(-1, self->chunk, 0);

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
