#include "core_common.h"

#define STB_IMAGE_IMPLEMENTATION
#define STBI_ONLY_PNG
#define STBI_ONLY_JPEG
#include "stb_image.h"

static PyObject *
core_load_image(PyObject *self, PyObject *args)
{
    const char *filename;
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }

    int len;
    unsigned char *buf = (unsigned char *)read_file(filename, &len);

    int width, height, comp;
    stbi_uc *pixels = stbi_load_from_memory(buf, len, &width, &height, &comp, 0);
    free(buf);
    PyObject *rgba = PyString_FromStringAndSize((const char *)pixels, width * height * comp);
    stbi_image_free(pixels);

    PyObject *textureArgs = Py_BuildValue("iiNi", width, height, rgba, comp);
    PyObject *result = PyObject_CallObject((PyObject *)&TextureType, textureArgs);
    Py_DECREF(textureArgs);

    return result;
}
