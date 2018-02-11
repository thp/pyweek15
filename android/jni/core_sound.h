#include "core_common.h"

#include "main.h"

typedef struct {
    PyObject_HEAD
    int id;
} SoundObject;

static void
Sound_dealloc(SoundObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
Sound_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    SoundObject *self = (SoundObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->id = -1;
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

    self->id = androidsound_load(filename);
    return 0;
}

static PyObject *
Sound_play(SoundObject *self)
{
    androidsound_play(self->id);
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
