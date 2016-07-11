#include "core_common.h"

#include "fontaine.h"

typedef struct {
    PyObject_HEAD

    struct FontaineFont *font;
    float size;
} FontObject;

static void
Font_dealloc(FontObject *self)
{
    fontaine_free(self->font);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Font_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    FontObject *self = (FontObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->font = NULL;
        self->size = 1.f;
    }

    return (PyObject *)self;
}

static int
Font_init(FontObject *self, PyObject *args, PyObject *kwargs)
{
    if (!PyArg_ParseTuple(args, "f", &self->size)) {
        return -1;
    }

    self->font = fontaine_new(NULL, NULL, NULL);

    return 0;
}

static PyObject *
Font_render(FontObject *self, PyObject *args)
{
    const char *text;
    if (!PyArg_ParseTuple(args, "s", &text)) {
        return NULL;
    }

    int width, height;

    unsigned char *pixels = fontaine_render(self->font, text, &width, &height);
    unsigned char *pixels4 = malloc(width * height * 4);
    int offset = 0;
    for (int i=0; i<width*height; i++) {
        pixels4[offset++] = 0xff;
        pixels4[offset++] = 0xff;
        pixels4[offset++] = 0xff;
        pixels4[offset++] = pixels[i];
    }
    fontaine_free_pixels(self->font, pixels);

    PyObject *rgba = PyString_FromStringAndSize((const char *)pixels4, width * height * 4);
    free(pixels4);

    PyObject *textureArgs = Py_BuildValue("iiNi", width, height, rgba, 4);
    PyObject *result = PyObject_CallObject((PyObject *)&TextureType, textureArgs);
    Py_DECREF(textureArgs);

    const char *attrs[] = {"w", "h"};
    for (int i=0; i<sizeof(attrs)/sizeof(attrs[0]); i++) {
        PyObject *attr = PyObject_GetAttrString(result, attrs[i]);
        if (PyNumber_Check(attr)) {
            PyObject *old_value = PyNumber_Float(attr);
            PyObject *new_value = PyFloat_FromDouble(PyFloat_AsDouble(old_value) * self->size / 2.f);
            PyObject_SetAttrString(result, attrs[i], new_value);
            Py_DECREF(old_value);
            Py_DECREF(new_value);
        }
        Py_DECREF(attr);
    }

    return (PyObject *)result;
}

static PyMemberDef
Font_members[] = {
    {"size", T_FLOAT, offsetof(FontObject, size), 0, "scaling factor"},
    {NULL}
};

static PyMethodDef
Font_methods[] = {
    {"render", (PyCFunction)Font_render, METH_VARARGS, "Render text to a texture"},
    {NULL}
};

DEFINE_TYPE(Font);
