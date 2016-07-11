#include <stdlib.h>

#include "core_common.h"

static PyObject *
core_list_files(PyObject *self, PyObject *args)
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
core_read_file(PyObject *self, PyObject *args)
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
