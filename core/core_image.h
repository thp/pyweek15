#include "core_common.h"

#define STB_IMAGE_IMPLEMENTATION
#define STBI_ONLY_PNG
#define STBI_ONLY_JPEG
#include "stb_image.h"

typedef struct {
    PyObject_HEAD
} ImageObject;

static void
Image_dealloc(ImageObject *self)
{
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Image_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    return type->tp_alloc(type, 0);
}

static int
Image_init(ImageObject *self, PyObject *args, PyObject *kwargs)
{
    return 0;
}

static PyObject *
Image_load(PyObject *self, PyObject *args)
{
    const char *filename;
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }

    int len;
    unsigned char *buf = (unsigned char *)read_file(filename, &len);

#if defined(CORE_FORCE_RGBA_TEXTURES)
    int reqcomp = 4;
#else
    int reqcomp = 0;
#endif /* defined(CORE_FORCE_RGBA_TEXTURES) */

    int width, height, comp;
    stbi_uc *pixels = stbi_load_from_memory(buf, len, &width, &height, &comp, reqcomp);
    if (reqcomp != 0) {
        comp = reqcomp;
    }
    free(buf);
    PyObject *rgba = PyString_FromStringAndSize((const char *)pixels, width * height * comp);
    stbi_image_free(pixels);

    PyObject *textureArgs = Py_BuildValue("iiNi", width, height, rgba, comp);
    PyObject *result = PyObject_CallObject((PyObject *)&TextureType, textureArgs);
    Py_DECREF(textureArgs);

    return result;
}

static PyMemberDef
Image_members[] = {
    {NULL}
};

static PyMethodDef
Image_methods[] = {
    {"load", Image_load, METH_VARARGS | METH_STATIC, "Load image data from a file"},
    {NULL}
};

DEFINE_TYPE(Image);
