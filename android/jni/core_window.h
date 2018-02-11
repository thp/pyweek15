#include "core_common.h"

#include "main.h"

#include <android/input.h>

typedef struct {
    PyObject_HEAD
} WindowObject;

static void
Window_dealloc(WindowObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
Window_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    return type->tp_alloc(type, 0);
}

static int
Window_init(WindowObject *self, PyObject *args, PyObject *kwargs)
{
    int width, height;
    const char *title;

    if (!PyArg_ParseTuple(args, "iis", &width, &height, &title)) {
        return -1;
    }

    // Implicit on Android, could use width/height to call setFixedSize()

    draw_init();

    return 0;
}

static PyObject *
Window_swap_buffers(WindowObject *self)
{
    // Implicit on Android

    Py_RETURN_NONE;
}

static PyObject *
Window_next_event(WindowObject *self)
{
    struct TouchEvent evt;
    if (evt_pop(&evt)) {
        if (evt.pressed == AMOTION_EVENT_ACTION_DOWN) {
            return Py_BuildValue("i(iffi)", 3, 0, evt.x, evt.y, evt.finger);
        } else if (evt.pressed == AMOTION_EVENT_ACTION_MOVE) {
            return Py_BuildValue("i(iffi)", 3, 1, evt.x, evt.y, evt.finger);
        } else if (evt.pressed == AMOTION_EVENT_ACTION_UP || evt.pressed == AMOTION_EVENT_ACTION_CANCEL) {
            return Py_BuildValue("i(iffi)", 3, 2, evt.x, evt.y, evt.finger);
        }
    }

    return Py_BuildValue("i()", 0);
}

static PyMemberDef
Window_members[] = {
    {NULL}
};

static PyMethodDef
Window_methods[] = {
    {"swap_buffers", (PyCFunction)Window_swap_buffers, METH_NOARGS, "Display rendering result"},
    {"next_event", (PyCFunction)Window_next_event, METH_NOARGS, "Get next event from queue"},
    {NULL}
};

DEFINE_TYPE(Window);
