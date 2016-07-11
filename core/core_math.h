#include "core_common.h"

#include <math.h>

typedef struct {
    PyObject_HEAD
} mathObject;

static void
math_dealloc(mathObject *self)
{
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
math_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    return type->tp_alloc(type, 0);
}

static int
math_init(mathObject *self, PyObject *args, PyObject *kwargs)
{
    return 0;
}

static PyObject *
math_sin(PyObject *self, PyObject *args)
{
    float arg;
    if (!PyArg_ParseTuple(args, "f", &arg)) {
        return NULL;
    }
    return Py_BuildValue("f", sinf(arg));
}

static PyObject *
math_cos(PyObject *self, PyObject *args)
{
    float arg;
    if (!PyArg_ParseTuple(args, "f", &arg)) {
        return NULL;
    }
    return Py_BuildValue("f", cosf(arg));
}

static PyObject *
math_sqrt(PyObject *self, PyObject *args)
{
    float arg;
    if (!PyArg_ParseTuple(args, "f", &arg)) {
        return NULL;
    }
    return Py_BuildValue("f", sqrtf(arg));
}

static PyMemberDef
math_members[] = {
    {NULL}
};

static PyMethodDef
math_methods[] = {
    {"sin", (PyCFunction)math_sin, METH_VARARGS | METH_STATIC, "sine"},
    {"cos", (PyCFunction)math_cos, METH_VARARGS | METH_STATIC, "cosine"},
    {"sqrt", (PyCFunction)math_sqrt, METH_VARARGS | METH_STATIC, "square root"},
    {NULL}
};

DEFINE_TYPE(math);
