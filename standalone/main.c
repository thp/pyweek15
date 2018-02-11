#include "core.h"

int
main(int argc, char **argv)
{
    Py_FrozenFlag = 1;
    Py_NoSiteFlag = 1;

    setenv("PYTHONPATH", argv[0], 1);

    PyImport_AppendInittab("core", PyInit_core);

    Py_Initialize();

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
        PyObject *iter = PyObject_CallMethod(engine, "frames", NULL);
        while (iter != NULL) {
            PyObject *o = PyIter_Next(iter);
            if (o == NULL) {
                break;
            }
            Py_XDECREF(o);
        }
        Py_XDECREF(iter);
    } else {
        PyErr_Print();
    }
    Py_XDECREF(engine);

    Py_Finalize();

    return 0;
}
