#include "core_common.h"

#include <stdlib.h>

typedef struct {
    PyObject_HEAD
} randomObject;

static void
random_request_seed()
{
    static int inited = 0;
    if (!inited) {
        srand((uint32_t)time(NULL));
        inited = 1;
    }
}

static void
random_dealloc(randomObject *self)
{
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
random_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    return type->tp_alloc(type, 0);
}

static int
random_init(randomObject *self, PyObject *args, PyObject *kwargs)
{
    return 0;
}

static PyObject *
random_randint(PyObject *self, PyObject *args)
{
    long long a, b;
    if (!PyArg_ParseTuple(args, "LL", &a, &b)) {
        return NULL;
    }

    random_request_seed();
    long long result = a + (b - a) * (long long)rand() / (long long)RAND_MAX;
    return Py_BuildValue("L", result);
}

static PyObject *
random_uniform(PyObject *self, PyObject *args)
{
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }

    random_request_seed();
    double result = a + (b - a) * (double)rand() / (double)RAND_MAX;
    return Py_BuildValue("d", result);
}


static PyMemberDef
random_members[] = {
    {NULL}
};

static PyMethodDef
random_methods[] = {
    {"randint", (PyCFunction)random_randint, METH_VARARGS | METH_STATIC, "random integer"},
    {"uniform", (PyCFunction)random_uniform, METH_VARARGS | METH_STATIC, "random uniform"},
    {NULL}
};

DEFINE_TYPE(random);
