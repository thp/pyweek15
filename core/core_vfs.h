#include "core_common.h"

#include <stdlib.h>

typedef struct {
    PyObject_HEAD
} VFSObject;

static void
VFS_dealloc(VFSObject *self)
{
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
VFS_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    return type->tp_alloc(type, 0);
}

static int
VFS_init(VFSObject *self, PyObject *args, PyObject *kwargs)
{
    return 0;
}

static PyObject *
VFS_list_files(PyObject *self, PyObject *args)
{
    const char *dirname;
    if (!PyArg_ParseTuple(args, "s", &dirname)) {
        return NULL;
    }

    int count;
    char **filenames = list_files(dirname, &count);
    PyObject *list = PyList_New(count);
    for (int i=0; i<count; i++) {
        PyList_SET_ITEM(list, i, PyString_FromString(filenames[i]));
    }
    list_files_free(filenames, count);

    return list;
}

static PyObject *
VFS_read_file(PyObject *self, PyObject *args)
{
    const char *filename;
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }

    int len;
    char *buf = read_file(filename, &len);
    PyObject *contents = PyString_FromStringAndSize(buf, len);
    free(buf);

    return contents;
}

static PyMemberDef
VFS_members[] = {
    {NULL}
};

static PyMethodDef
VFS_methods[] = {
    {"list_files", (PyCFunction)VFS_list_files, METH_VARARGS | METH_STATIC, "List files in a directory by extension"},
    {"read_file", (PyCFunction)VFS_read_file, METH_VARARGS | METH_STATIC, "Read a file and return its data as str"},
    {NULL}
};

DEFINE_TYPE(VFS);
