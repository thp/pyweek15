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

    Py_TYPE(self)->tp_free((PyObject *)self);
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
    // (event_type, value)

    SDL_Event e;
    while (SDL_PollEvent(&e)) {
        switch (e.type) {
            case SDL_QUIT:
                return Py_BuildValue("i(O)", 1, Py_None);
            case SDL_KEYDOWN:
                return Py_BuildValue("i(ON)", 2, Py_True, PyUnicode_FromString(keysym_from_sdl_event(&e)));
            case SDL_KEYUP:
                return Py_BuildValue("i(ON)", 2, Py_False, PyUnicode_FromString(keysym_from_sdl_event(&e)));
            case SDL_MOUSEBUTTONDOWN:
                return Py_BuildValue("i(iffi)", 3, 0, (float)e.button.x, (float)e.button.y, 0);
            case SDL_MOUSEMOTION:
                if (e.motion.state) {
                    return Py_BuildValue("i(iffi)", 3, 1, (float)e.motion.x, (float)e.motion.y, 0);
                }
                break;
            case SDL_MOUSEBUTTONUP:
                return Py_BuildValue("i(iffi)", 3, 2, (float)e.button.x, (float)e.button.y, 0);
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
