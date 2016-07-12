#include "core_common.h"

#include <stdlib.h>

static char *
zipfile_name = NULL;

static char *
resolve_file_path(const char *filename)
{
    char *result;
    asprintf(&result, "%s%s", CORE_DATA_ROOT, filename);
    return result;
}

static char **
list_files_zip(const char *, const char *, int *);

static char *
read_file_zip(const char *, const char *, int *);

static char **
list_files_direct(const char *, int *);

static char *
read_file_direct(const char *, int *);

static char **
vfs_list_files(const char *dirname, int *count)
{
    if (zipfile_name) {
        return list_files_zip(zipfile_name, dirname, count);
    } else {
        return list_files_direct(dirname, count);
    }
}

static char *
vfs_read_file(const char *filename, int *len)
{
    if (zipfile_name) {
        return read_file_zip(zipfile_name, filename, len);
    } else {
        return read_file_direct(filename, len);
    }
}

static void
vfs_list_files_free(char **result, int count)
{
    for (int i=0; i<count; i++) {
        free(result[i]);
    }
    free(result);
}

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
    char **filenames = vfs_list_files(dirname, &count);
    PyObject *list = PyList_New(count);
    for (int i=0; i<count; i++) {
        PyList_SET_ITEM(list, i, PyString_FromString(filenames[i]));
    }
    vfs_list_files_free(filenames, count);

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
    char *buf = vfs_read_file(filename, &len);
    PyObject *contents = PyString_FromStringAndSize(buf, len);
    free(buf);

    return contents;
}

static PyObject *
VFS_set_zipfile(PyObject *self, PyObject *args)
{
    const char *filename;
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }

    free(zipfile_name);
    zipfile_name = strdup(filename);

    Py_RETURN_NONE;
}

static PyMemberDef
VFS_members[] = {
    {NULL}
};

static PyMethodDef
VFS_methods[] = {
    {"list_files", (PyCFunction)VFS_list_files, METH_VARARGS | METH_STATIC, "List files in a directory by extension"},
    {"read_file", (PyCFunction)VFS_read_file, METH_VARARGS | METH_STATIC, "Read a file and return its data as str"},
    {"set_zipfile", (PyCFunction)VFS_set_zipfile, METH_VARARGS | METH_STATIC, "Set the zip file path for reading"},
    {NULL}
};

DEFINE_TYPE(VFS);
