#pragma once

#include <Python.h>
#include "structmember.h"
#include "core_config.h"

#define DEFINE_TYPE(name) \
    static PyTypeObject \
    name##Type = { \
        PyObject_HEAD_INIT(NULL) \
        .tp_name = "core." #name, \
        .tp_basicsize = sizeof(name##Object), \
        .tp_dealloc = (destructor)name##_dealloc, \
        .tp_flags = Py_TPFLAGS_DEFAULT, \
        .tp_doc = #name, \
        .tp_methods = name##_methods, \
        .tp_members = name##_members, \
        .tp_init = (initproc)name##_init, \
        .tp_new = name##_new, \
    }

static PyTypeObject TextureType;

static char *
vfs_read_file(const char *filename, int *length);

static char **
vfs_list_files(const char *dirname, int *count);

static void
vfs_list_files_free(char **result, int count);

static void
draw_init(void);

static void
sound_init(void);
