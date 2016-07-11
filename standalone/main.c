#include "Python.h"
#include <SDL.h>

int
main(int argc, char **argv)
{
    Py_FrozenFlag = 1;
    Py_NoSiteFlag = 1;

    Py_Initialize();

    PyObject *sys = PyImport_ImportModule("sys");
    if (sys) {
        PyObject *path = PyObject_GetAttrString(sys, "path");
        if (path) {
            PyObject *self = PyString_FromString(argv[0]);
            PyList_Insert(path, 0, self);
            Py_DECREF(self);
            Py_DECREF(path);
        } else {
            PyErr_Print();
        }
    } else {
        PyErr_Print();
    }
    Py_XDECREF(sys);

    PyObject *engine = PyImport_ImportModule("engine");
    if (engine) {
        PyObject_CallMethod(engine, "main", NULL);
    } else {
        PyErr_Print();
    }
    Py_XDECREF(engine);

    Py_Finalize();

    return 0;
}
