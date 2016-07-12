#include "core_common.h"

typedef struct {
    PyObject_HEAD
} WindowObject;

static void
Window_dealloc(WindowObject *self)
{
    sf2d_fini();
    self->ob_type->tp_free((PyObject *)self);
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

    sf2d_init();
    sf2d_set_clear_color(RGBA8(0x00, 0x00, 0x00, 0xFF));
    sf2d_set_3D(0);

    draw_init();
    sound_init();

    return 0;
}

static PyObject *
Window_swap_buffers(WindowObject *self)
{
    sf2d_swapbuffers();

    Py_RETURN_NONE;
}

static PyObject *
Window_next_event(WindowObject *self)
{
    // (quit, is_key_event, pressed, keyval)

    if (!aptMainLoop()) {
        return Py_BuildValue("OOOO", Py_True, Py_False, Py_None, Py_None);
    }

    hidScanInput();

    u32 kDown = hidKeysDown();
    u32 kUp = hidKeysUp();

    if (kDown & KEY_START) {
        // Exit the game with START
        return Py_BuildValue("OOOO", Py_True, Py_False, Py_None, Py_None);
    }

    struct {
        uint32_t hid_key;
        const char *game_key;
    } mapping[] = {
        { KEY_UP, "up" },
        { KEY_LEFT, "left" },
        { KEY_RIGHT, "right" },
        { KEY_A, " " },
        { KEY_B, "s" },
        { KEY_START, "esc" },
    };

    // We just check out the first key that we find and ignore the rest
    for (int i=0; i<sizeof(mapping)/sizeof(mapping[0]); i++) {
        if (kDown & mapping[i].hid_key) {
            return Py_BuildValue("OOON", Py_False, Py_True, Py_True, PyString_FromString(mapping[i].game_key));
        } else if (kUp & mapping[i].hid_key) {
            return Py_BuildValue("OOON", Py_False, Py_True, Py_False, PyString_FromString(mapping[i].game_key));
        }
    }

    return Py_BuildValue("OOOO", Py_False, Py_False, Py_None, Py_None);
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
