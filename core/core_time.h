#include "core_common.h"

#include <time.h>

typedef struct {
    PyObject_HEAD
} timeObject;

static void
time_dealloc(timeObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
time_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    return type->tp_alloc(type, 0);
}

static int
time_init(timeObject *self, PyObject *args, PyObject *kwargs)
{
    return 0;
}

static PyObject *
time_time(timeObject *self)
{
    struct timeval tv;
    double result = 0.0;
    if (gettimeofday(&tv, NULL) == 0) {
        result = tv.tv_sec + tv.tv_usec / (1000.0 * 1000.0);
    }
    return Py_BuildValue("d", result);
}

static PyMemberDef
time_members[] = {
    {NULL}
};

static PyMethodDef
time_methods[] = {
    {"time", (PyCFunction)time_time, METH_NOARGS | METH_STATIC, "Get the current time in seconds"},
    {NULL}
};

DEFINE_TYPE(time);
