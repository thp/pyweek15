#include "core_common.h"

#include <SDL.h>

typedef struct {
    PyObject_HEAD

    SDL_Window *window;
    SDL_GLContext gl_context;
} WindowObject;

static void
Window_dealloc(WindowObject *self)
{
    SDL_GL_DeleteContext(self->gl_context);
    SDL_DestroyWindow(self->window);
    SDL_Quit();

    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Window_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    WindowObject *self = (WindowObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->window = NULL;
        memset(&self->gl_context, 0, sizeof(self->gl_context));
    }

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

    SDL_Init(SDL_INIT_AUDIO | SDL_INIT_VIDEO);

    self->window = SDL_CreateWindow(title,
            SDL_WINDOWPOS_CENTERED,
            SDL_WINDOWPOS_CENTERED,
            width, height,
            SDL_WINDOW_SHOWN | SDL_WINDOW_OPENGL);

    self->gl_context = SDL_GL_CreateContext(self->window);

    draw_init();
    sound_init();

    return 0;
}

static PyObject *
Window_swap_buffers(WindowObject *self)
{
    SDL_GL_SwapWindow(self->window);

    Py_RETURN_NONE;
}

static const char *
keysym_from_sdl_event(SDL_Event *e)
{
    switch (e->key.keysym.sym) {
        case SDLK_ESCAPE: return "esc";
        case SDLK_SPACE:  return " ";
        case SDLK_s:      return "s";
        case SDLK_LEFT:   return "left";
        case SDLK_RIGHT:  return "right";
        case SDLK_UP:     return "up";
        default:          break;
    }

    return "";
}

static PyObject *
Window_next_event(WindowObject *self)
{
    // (quit, is_key_event, pressed, keyval)

    SDL_Event e;
    while (SDL_PollEvent(&e)) {
        switch (e.type) {
            case SDL_QUIT:
                return Py_BuildValue("OOOO", Py_True, Py_False, Py_None, Py_None);
            case SDL_KEYDOWN:
                return Py_BuildValue("OOON", Py_False, Py_True, Py_True, PyString_FromString(keysym_from_sdl_event(&e)));
            case SDL_KEYUP:
                return Py_BuildValue("OOON", Py_False, Py_True, Py_False, PyString_FromString(keysym_from_sdl_event(&e)));
            default:
                break;
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
