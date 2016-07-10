#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <Python.h>

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
core_time_seconds(PyObject *self, PyObject *args)
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

static PyMethodDef CoreMethods[] = {
    {"sin", core_sin, METH_VARARGS, "sine"},
    {"cos", core_cos, METH_VARARGS, "cosine"},
    {"sqrt", core_sqrt, METH_VARARGS, "square root"},
    {"time_seconds", core_time_seconds, METH_NOARGS, "current time"},
    {"randint", core_randint, METH_VARARGS, "random integer"},
    {"randuniform", core_randuniform, METH_VARARGS, "random uniform"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initcore(void)
{
    srand((uint32_t)time(NULL));
    (void)Py_InitModule("core", CoreMethods);
}
