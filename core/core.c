#include "core_common.h"

#include "core_util.h"
#include "core_image.h"
#include "core_fileio.h"
#include "core_window.h"
#include "core_sound.h"
#include "core_font.h"
#include "core_opengl.h"

static PyMethodDef CoreMethods[] = {
    {"sin", core_sin, METH_VARARGS, "sine"},
    {"cos", core_cos, METH_VARARGS, "cosine"},
    {"sqrt", core_sqrt, METH_VARARGS, "square root"},
    {"time_seconds", (PyCFunction)core_time_seconds, METH_NOARGS, "current time"},
    {"randint", core_randint, METH_VARARGS, "random integer"},
    {"randuniform", core_randuniform, METH_VARARGS, "random uniform"},
    {"draw_init", (PyCFunction)core_draw_init, METH_NOARGS, "init opengl"},
    {"load_image", core_load_image, METH_VARARGS, "Load image data from a file"},
    {"list_files", core_list_files, METH_VARARGS, "List files in a directory by extension"},
    {"read_file", core_read_file, METH_VARARGS, "Read a file and return its data as str"},
    {NULL, NULL, 0, NULL}
};

#define INIT_TYPE(name) \
    name##Type.tp_new = PyType_GenericNew; \
    PyType_Ready(&name##Type); \
    Py_INCREF(&name##Type); \
    PyModule_AddObject(m, #name, (PyObject *)&name##Type)

PyMODINIT_FUNC
initcore(void)
{
    srand((uint32_t)time(NULL));

    PyObject *m = Py_InitModule("core", CoreMethods);

    INIT_TYPE(Texture);
    INIT_TYPE(Framebuffer);
    INIT_TYPE(ShaderProgram);
    INIT_TYPE(Window);
    INIT_TYPE(Sound);
    INIT_TYPE(Font);
}
