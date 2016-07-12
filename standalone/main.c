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
            PyObject *self = PyString_FromString(argv[0]);
            PyList_Insert(path, 0, self);
            Py_DECREF(path);
            Py_DECREF(self);
        } else {
            PyErr_Print();
        }
    } else {
        PyErr_Print();
    }
    Py_XDECREF(sys);

    PyObject *core = PyImport_ImportModule("core");
    if (core) {
        PyObject *VFS = PyObject_GetAttrString(core, "VFS");
        if (VFS) {
            PyObject *result = PyObject_CallMethod(VFS, "set_zipfile", "s", argv[0]);
            Py_DECREF(result);
            Py_DECREF(VFS);
        } else {
            PyErr_Print();
        }
    } else {
        PyErr_Print();
    }
    Py_XDECREF(core);

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
