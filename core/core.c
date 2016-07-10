#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <Python.h>
#include "structmember.h"

#include <OpenGL/GL.h>

static PyObject *
core_sin(PyObject *self, PyObject *args)
{
    float arg;
    if (!PyArg_ParseTuple(args, "f", &arg)) {
        return NULL;
    }
    return Py_BuildValue("f", sinf(arg));
}

static PyObject *
core_cos(PyObject *self, PyObject *args)
{
    float arg;
    if (!PyArg_ParseTuple(args, "f", &arg)) {
        return NULL;
    }
    return Py_BuildValue("f", cosf(arg));
}

static PyObject *
core_sqrt(PyObject *self, PyObject *args)
{
    float arg;
    if (!PyArg_ParseTuple(args, "f", &arg)) {
        return NULL;
    }
    return Py_BuildValue("f", sqrtf(arg));
}

static PyObject *
core_time_seconds(PyObject *self)
{
    struct timeval tv;
    double result = 0.0;
    if (gettimeofday(&tv, NULL) == 0) {
        result = tv.tv_sec + tv.tv_usec / (1000.0 * 1000.0);
    }
    return Py_BuildValue("d", result);
}

static PyObject *
core_randint(PyObject *self, PyObject *args)
{
    long long a, b;
    if (!PyArg_ParseTuple(args, "LL", &a, &b)) {
        return NULL;
    }

    long long result = a + (b - a) * (long long)rand() / (long long)RAND_MAX;
    return Py_BuildValue("L", result);
}

static PyObject *
core_randuniform(PyObject *self, PyObject *args)
{
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }

    double result = a + (b - a) * (double)rand() / (double)RAND_MAX;
    return Py_BuildValue("d", result);
}

static PyObject *
core_draw_init(PyObject *self)
{
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    glEnableVertexAttribArray(0);
    glEnableVertexAttribArray(1);

    Py_RETURN_NONE;
}

static PyObject *
core_draw_clear(PyObject *self)
{
    glClear(GL_COLOR_BUFFER_BIT);

    Py_RETURN_NONE;
}

static PyObject *
core_draw_quad(PyObject *self)
{
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

    Py_RETURN_NONE;
}


typedef struct {
    PyObject_HEAD

    int w;
    int h;
    GLuint texture_id;
} TextureObject;

static void
Texture_dealloc(TextureObject *self)
{
    glDeleteTextures(1, &self->texture_id);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Texture_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    TextureObject *self = (TextureObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->w = 0;
        self->h = 0;
        self->texture_id = 0;
    }

    return (PyObject *)self;
}

static int
Texture_init(TextureObject *self, PyObject *args, PyObject *kwargs)
{
    const char *rgba;
    int rgba_len;

    if (!PyArg_ParseTuple(args, "iiz#", &self->w, &self->h, &rgba, &rgba_len)) {
        return -1;
    }

    assert(rgba_len == (self->w * self->h * 4));

    glGenTextures(1, &self->texture_id);
    glBindTexture(GL_TEXTURE_2D, self->texture_id);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self->w, self->h, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgba);

    return 0;
}

static PyObject *
Texture_bind(TextureObject *self)
{
    glBindTexture(GL_TEXTURE_2D, self->texture_id);

    Py_RETURN_NONE;
}

static PyMemberDef
Texture_members[] = {
    {"w", T_INT, offsetof(TextureObject, w), 0, "width"},
    {"h", T_INT, offsetof(TextureObject, h), 0, "height"},
    {"texture_id", T_INT, offsetof(TextureObject, texture_id), 0, "GL texture name"},
    {NULL}
};

static PyMethodDef
Texture_methods[] = {
    {"bind", (PyCFunction)Texture_bind, METH_NOARGS, "Bind the texture for use"},
    {NULL}
};

static PyTypeObject
TextureType = {
    PyObject_HEAD_INIT(NULL)
    .tp_name = "core.Texture",
    .tp_basicsize = sizeof(TextureObject),
    .tp_dealloc = (destructor)Texture_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "GL texture",
    .tp_methods = Texture_methods,
    .tp_members = Texture_members,
    .tp_init = (initproc)Texture_init,
    .tp_new = Texture_new,
};

static PyMethodDef CoreMethods[] = {
    {"sin", core_sin, METH_VARARGS, "sine"},
    {"cos", core_cos, METH_VARARGS, "cosine"},
    {"sqrt", core_sqrt, METH_VARARGS, "square root"},
    {"time_seconds", (PyCFunction)core_time_seconds, METH_NOARGS, "current time"},
    {"randint", core_randint, METH_VARARGS, "random integer"},
    {"randuniform", core_randuniform, METH_VARARGS, "random uniform"},
    {"draw_init", (PyCFunction)core_draw_init, METH_NOARGS, "init opengl"},
    {"draw_clear", (PyCFunction)core_draw_clear, METH_NOARGS, "clear screen"},
    {"draw_quad", (PyCFunction)core_draw_quad, METH_NOARGS, "draw a quad"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initcore(void)
{
    srand((uint32_t)time(NULL));

    TextureType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&TextureType) < 0)
        return;

    PyObject *m = Py_InitModule("core", CoreMethods);

    Py_INCREF(&TextureType);
    PyModule_AddObject(m, "Texture", (PyObject *)&TextureType);
}
