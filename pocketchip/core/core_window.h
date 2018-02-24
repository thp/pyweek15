#include "core_common.h"
#include "core_opengl_platform.h"

#include <SDL.h>
#include "eglo.h"
#include <X11/keysym.h>

typedef struct {
    PyObject_HEAD
} WindowObject;

static void
Window_dealloc(WindowObject *self)
{
    eglo_quit();

    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
Window_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    WindowObject *self = (WindowObject *)type->tp_alloc(type, 0);

    return (PyObject *)self;
}

static int
Window_init(WindowObject *self, PyObject *args, PyObject *kwargs)
{
    int width, height;
    const char *title;

    if (!PyArg_ParseTuple(args, "iis", &width, &height, &title)) {
        return -1;
    }

    // We only init SDL for audio output here (mixer)
    SDL_Init(SDL_INIT_AUDIO);

    eglo_init(&width, &height, 2);

    draw_init();
    sound_init();

    return 0;
}

static PyObject *
Window_swap_buffers(WindowObject *self)
{
    eglo_swap_buffers();

    Py_RETURN_NONE;
}

static const char *
keysym_from_eglo_event(EgloEvent *e)
{
    switch (e->key.key) {
        case XK_Escape: return "esc";
        case XK_space: case XK_0: return " ";
        case XK_s: case XK_BackSpace: return "s";
        case XK_Left: return "left";
        case XK_Right: return "right";
        case XK_Up: return "up";
        default: break;
    }

    return "";
}

static PyObject *
Window_next_event(WindowObject *self)
{
    // (event_type, value)

    EgloEvent e;
    while (eglo_next_event(&e)) {
        switch (e.type) {
            case EGLO_QUIT:
                return Py_BuildValue("i(O)", 1, Py_None);
            case EGLO_KEY_DOWN:
                return Py_BuildValue("i(ON)", 2, Py_True, PyUnicode_FromString(keysym_from_eglo_event(&e)));
            case EGLO_KEY_UP:
                return Py_BuildValue("i(ON)", 2, Py_False, PyUnicode_FromString(keysym_from_eglo_event(&e)));
            default:
                break;
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
