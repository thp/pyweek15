#include "core.h"

int
main(int argc, char **argv)
{
    Py_FrozenFlag = 1;
    Py_NoSiteFlag = 1;

    Py_Initialize();

    initcore();

    PyObject *sys = PyImport_ImportModule("sys");
    if (sys) {
        PyObject *path = PyObject_GetAttrString(sys, "path");
        if (path) {
            //PyObject *self = PyString_FromString(argv[0]);
            PyObject *self = PyString_FromString("onewhaletrip.zip");
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
