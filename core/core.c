#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <Python.h>
#include "structmember.h"

#include <OpenGL/GL.h>

#define STB_IMAGE_IMPLEMENTATION
#define STBI_ONLY_PNG
#define STBI_ONLY_JPEG
#include "stb_image.h"

#include "fontaine.h"

static PyTypeObject TextureType;

static PyObject *
core_sin(PyObject *self, PyObject *args)
{
    float arg;
    if (!PyArg_ParseTuple(args, "f", &arg)) {
        return NULL;
    }
    return Py_BuildValue("f", sinf(arg));
}

static PyObject *
core_cos(PyObject *self, PyObject *args)
{
    float arg;
    if (!PyArg_ParseTuple(args, "f", &arg)) {
        return NULL;
    }
    return Py_BuildValue("f", cosf(arg));
}

static PyObject *
core_sqrt(PyObject *self, PyObject *args)
{
    float arg;
    if (!PyArg_ParseTuple(args, "f", &arg)) {
        return NULL;
    }
    return Py_BuildValue("f", sqrtf(arg));
}

static PyObject *
core_time_seconds(PyObject *self)
{
    struct timeval tv;
    double result = 0.0;
    if (gettimeofday(&tv, NULL) == 0) {
        result = tv.tv_sec + tv.tv_usec / (1000.0 * 1000.0);
    }
    return Py_BuildValue("d", result);
}

static PyObject *
core_randint(PyObject *self, PyObject *args)
{
    long long a, b;
    if (!PyArg_ParseTuple(args, "LL", &a, &b)) {
        return NULL;
    }

    long long result = a + (b - a) * (long long)rand() / (long long)RAND_MAX;
    return Py_BuildValue("L", result);
}

static PyObject *
core_randuniform(PyObject *self, PyObject *args)
{
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        return NULL;
    }

    double result = a + (b - a) * (double)rand() / (double)RAND_MAX;
    return Py_BuildValue("d", result);
}

static PyObject *
core_draw_init(PyObject *self)
{
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    glEnableVertexAttribArray(0);
    glEnableVertexAttribArray(1);

    Py_RETURN_NONE;
}

static PyObject *
core_draw_clear(PyObject *self)
{
    glClear(GL_COLOR_BUFFER_BIT);

    Py_RETURN_NONE;
}

static PyObject *
core_draw_quad(PyObject *self)
{
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

    Py_RETURN_NONE;
}

static PyObject *
core_load_image(PyObject *self, PyObject *args)
{
    const char *filename;
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }

    FILE *fp = fopen(filename, "rb");
    fseek(fp, 0, SEEK_END);
    int len = (int)ftell(fp);
    fseek(fp, 0, SEEK_SET);
    unsigned char *image_data = malloc(len);
    fread(image_data, len, 1, fp);
    int width, height, comp;
    stbi_uc *pixels = stbi_load_from_memory(image_data, len, &width, &height, &comp, 0);
    free(image_data);
    PyObject *rgba = PyString_FromStringAndSize((const char *)pixels, width * height * comp);
    stbi_image_free(pixels);

    PyObject *textureArgs = Py_BuildValue("iiNi", width, height, rgba, comp);
    PyObject *result = PyObject_CallObject((PyObject *)&TextureType, textureArgs);
    Py_DECREF(textureArgs);

    return result;
}

static PyObject *
core_render_text(PyObject *self, PyObject *args)
{
    const char *text;
    if (!PyArg_ParseTuple(args, "s", &text)) {
        return NULL;
    }

    int width, height;

    struct FontaineFont *font = fontaine_new(NULL, NULL, NULL);
    unsigned char *pixels = fontaine_render(font, text, &width, &height);
    unsigned char *pixels2 = malloc(width * height * 2);
    // LUMINANCE_ALPHA format needs 2 bytes per pixels -- use that opportunity to make
    // the luminance part white (0xFF) and only take the alpha channel from the font
    for (int i=0; i<width*height; i++) {
        pixels2[i*2+0] = 0xFF;
        pixels2[i*2+1] = pixels[i];
    }
    fontaine_free_pixels(font, pixels);
    fontaine_free(font);

    PyObject *rgba = PyString_FromStringAndSize((const char *)pixels2, width * height * 2);
    free(pixels2);

    PyObject *textureArgs = Py_BuildValue("iiNi", width, height, rgba, 2);
    PyObject *result = PyObject_CallObject((PyObject *)&TextureType, textureArgs);
    Py_DECREF(textureArgs);

    return result;
}

typedef struct {
    PyObject_HEAD

    int w;
    int h;
    GLuint texture_id;
} TextureObject;

static void
Texture_dealloc(TextureObject *self)
{
    glDeleteTextures(1, &self->texture_id);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Texture_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    TextureObject *self = (TextureObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->w = 0;
        self->h = 0;
        self->texture_id = 0;
    }

    return (PyObject *)self;
}

static int
Texture_init(TextureObject *self, PyObject *args, PyObject *kwargs)
{
    const char *rgba;
    int rgba_len;
    int comp;

    if (!PyArg_ParseTuple(args, "iiz#i", &self->w, &self->h, &rgba, &rgba_len, &comp)) {
        return -1;
    }

    assert(rgba_len == (self->w * self->h * comp));

    GLenum format = (comp == 2) ? GL_LUMINANCE_ALPHA : ((comp == 4) ? GL_RGBA : GL_RGB);

    glGenTextures(1, &self->texture_id);
    glBindTexture(GL_TEXTURE_2D, self->texture_id);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, (format == GL_LUMINANCE_ALPHA) ? GL_NEAREST : GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, (format == GL_LUMINANCE_ALPHA) ? GL_NEAREST : GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

    glTexImage2D(GL_TEXTURE_2D, 0, format, self->w, self->h, 0, format, GL_UNSIGNED_BYTE, rgba);

    return 0;
}

static PyObject *
Texture_bind(TextureObject *self)
{
    glBindTexture(GL_TEXTURE_2D, self->texture_id);

    Py_RETURN_NONE;
}

static PyMemberDef
Texture_members[] = {
    {"w", T_INT, offsetof(TextureObject, w), 0, "width"},
    {"h", T_INT, offsetof(TextureObject, h), 0, "height"},
    {"texture_id", T_INT, offsetof(TextureObject, texture_id), 0, "GL texture name"},
    {NULL}
};

static PyMethodDef
Texture_methods[] = {
    {"bind", (PyCFunction)Texture_bind, METH_NOARGS, "Bind the texture for use"},
    {NULL}
};

static PyTypeObject
TextureType = {
    PyObject_HEAD_INIT(NULL)
    .tp_name = "core.Texture",
    .tp_basicsize = sizeof(TextureObject),
    .tp_dealloc = (destructor)Texture_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "GL texture",
    .tp_methods = Texture_methods,
    .tp_members = Texture_members,
    .tp_init = (initproc)Texture_init,
    .tp_new = Texture_new,
};

typedef struct {
    PyObject_HEAD

    GLuint framebuffer_id;
    PyObject *texture;
} FramebufferObject;

static void
Framebuffer_dealloc(FramebufferObject *self)
{
    glDeleteFramebuffers(1, &self->framebuffer_id);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Framebuffer_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    FramebufferObject *self = (FramebufferObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->framebuffer_id = 0;
        self->texture = NULL;
    }

    return (PyObject *)self;
}

static int
Framebuffer_init(FramebufferObject *self, PyObject *args, PyObject *kwargs)
{
    int width, height;

    if (!PyArg_ParseTuple(args, "ii", &width, &height)) {
        return -1;
    }

    PyObject *textureArgs = Py_BuildValue("iisi", width, height, NULL, 4);
    self->texture = PyObject_CallObject((PyObject *)&TextureType, textureArgs);
    Py_DECREF(textureArgs);

    glGenFramebuffers(1, &self->framebuffer_id);
    glBindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_id);
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, ((TextureObject *)(self->texture))->texture_id, 0);
    glBindFramebuffer(GL_FRAMEBUFFER, 0);

    return 0;
}

static PyObject *
Framebuffer_bind(FramebufferObject *self)
{
    glBindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_id);
    Py_RETURN_NONE;
}

static PyObject *
Framebuffer_unbind(FramebufferObject *self)
{
    glBindFramebuffer(GL_FRAMEBUFFER, 0);
    Py_RETURN_NONE;
}

static PyMemberDef
Framebuffer_members[] = {
    {"framebuffer_id", T_INT, offsetof(FramebufferObject, framebuffer_id), 0, "GL framebuffer name"},
    {"texture", T_OBJECT_EX, offsetof(FramebufferObject, texture), 0, "Texture object"},
    {NULL}
};

static PyMethodDef
Framebuffer_methods[] = {
    {"bind", (PyCFunction)Framebuffer_bind, METH_NOARGS, "Bind the framebuffer as render target"},
    {"unbind", (PyCFunction)Framebuffer_unbind, METH_NOARGS, "Unbind the framebuffer as render target"},
    {NULL}
};

static PyTypeObject
FramebufferType = {
    PyObject_HEAD_INIT(NULL)
    .tp_name = "core.Framebuffer",
    .tp_basicsize = sizeof(FramebufferObject),
    .tp_dealloc = (destructor)Framebuffer_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "GL framebuffer",
    .tp_methods = Framebuffer_methods,
    .tp_members = Framebuffer_members,
    .tp_init = (initproc)Framebuffer_init,
    .tp_new = Framebuffer_new,
};

typedef struct {
    PyObject_HEAD

    GLuint program_id;
    float *vertex_buffer;
} ShaderProgramObject;

static void
ShaderProgram_dealloc(ShaderProgramObject *self)
{
    free(self->vertex_buffer);
    glDeleteProgram(self->program_id);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
ShaderProgram_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    ShaderProgramObject *self = (ShaderProgramObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->program_id = 0;
        self->vertex_buffer = NULL;
    }

    return (PyObject *)self;
}

static int
ShaderProgram_init(ShaderProgramObject *self, PyObject *args, PyObject *kwargs)
{
    const char *vertex_shader_src;
    const char *fragment_shader_src;

    if (!PyArg_ParseTuple(args, "ss", &vertex_shader_src, &fragment_shader_src)) {
        return -1;
    }

    self->program_id = glCreateProgram();

    GLuint vertex_shader_id = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertex_shader_id, 1, &vertex_shader_src, NULL);
    glCompileShader(vertex_shader_id);
    glAttachShader(self->program_id, vertex_shader_id);
    glDeleteShader(vertex_shader_id);

    GLuint fragment_shader_id = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragment_shader_id, 1, &fragment_shader_src, NULL);
    glCompileShader(fragment_shader_id);
    glAttachShader(self->program_id, fragment_shader_id);
    glDeleteShader(fragment_shader_id);

    glBindAttribLocation(self->program_id, 0, "position");
    glBindAttribLocation(self->program_id, 1, "texcoord");

    glLinkProgram(self->program_id);

    return 0;
}

static PyObject *
ShaderProgram_bind(ShaderProgramObject *self)
{
    glUseProgram(self->program_id);
    Py_RETURN_NONE;
}

static PyObject *
ShaderProgram_uniform1f(ShaderProgramObject *self, PyObject *args)
{
    const char *name;
    float v0;
    if (!PyArg_ParseTuple(args, "sf", &name, &v0)) {
        return NULL;
    }

    glUniform1f(glGetUniformLocation(self->program_id, name), v0);

    Py_RETURN_NONE;
}

static PyObject *
ShaderProgram_uniform2f(ShaderProgramObject *self, PyObject *args)
{
    const char *name;
    float v0, v1;
    if (!PyArg_ParseTuple(args, "sff", &name, &v0, &v1)) {
        return NULL;
    }

    glUniform2f(glGetUniformLocation(self->program_id, name), v0, v1);

    Py_RETURN_NONE;
}

static PyObject *
ShaderProgram_uniform4f(ShaderProgramObject *self, PyObject *args)
{
    const char *name;
    float v0, v1, v2, v3;
    if (!PyArg_ParseTuple(args, "sffff", &name, &v0, &v1, &v2, &v3)) {
        return NULL;
    }

    glUniform4f(glGetUniformLocation(self->program_id, name), v0, v1, v2, v3);

    Py_RETURN_NONE;
}

static PyObject *
ShaderProgram_enable_arrays(ShaderProgramObject *self, PyObject *args)
{
    TextureObject *texture;
    PyObject *position;
    PyObject *texcoord;
    if (!PyArg_ParseTuple(args, "OOO", (PyObject **)&texture, &position, &texcoord)) {
        return NULL;
    }

    if (!PyList_Check(position)) {
        return NULL;
    }

    if (!PyList_Check(texcoord)) {
        return NULL;
    }

    ShaderProgram_bind(self);
    Texture_bind(texture);

    Py_ssize_t position_len = PyList_Size(position);
    Py_ssize_t texcoord_len = PyList_Size(texcoord);

    if (position_len != texcoord_len) {
        return NULL;
    }

    free(self->vertex_buffer);
    self->vertex_buffer = malloc(sizeof(float) * (position_len + texcoord_len));
    for (int i=0; i<position_len / 2; i++) {
        self->vertex_buffer[i*4+0] = PyFloat_AsDouble(PyList_GET_ITEM(position, i*2+0));
        self->vertex_buffer[i*4+1] = PyFloat_AsDouble(PyList_GET_ITEM(position, i*2+1));
        self->vertex_buffer[i*4+2] = PyFloat_AsDouble(PyList_GET_ITEM(texcoord, i*2+0));
        self->vertex_buffer[i*4+3] = PyFloat_AsDouble(PyList_GET_ITEM(texcoord, i*2+1));
    }

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 4, &self->vertex_buffer[0]);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 4, &self->vertex_buffer[2]);

    Py_RETURN_NONE;
}

static PyMemberDef
ShaderProgram_members[] = {
    {"program_id", T_INT, offsetof(ShaderProgramObject, program_id), 0, "GL program name"},
    {NULL}
};

static PyMethodDef
ShaderProgram_methods[] = {
    {"bind", (PyCFunction)ShaderProgram_bind, METH_NOARGS, "Use the shader program for rendering"},
    {"uniform1f", (PyCFunction)ShaderProgram_uniform1f, METH_VARARGS, "Set float uniform"},
    {"uniform2f", (PyCFunction)ShaderProgram_uniform2f, METH_VARARGS, "Set vec2 uniform"},
    {"uniform4f", (PyCFunction)ShaderProgram_uniform4f, METH_VARARGS, "Set vec4 uniform"},
    {"enable_arrays", (PyCFunction)ShaderProgram_enable_arrays, METH_VARARGS, "Set array pointers"},
    {NULL}
};

static PyTypeObject
ShaderProgramType = {
    PyObject_HEAD_INIT(NULL)
    .tp_name = "core.ShaderProgram",
    .tp_basicsize = sizeof(ShaderProgramObject),
    .tp_dealloc = (destructor)ShaderProgram_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "GL framebuffer",
    .tp_methods = ShaderProgram_methods,
    .tp_members = ShaderProgram_members,
    .tp_init = (initproc)ShaderProgram_init,
    .tp_new = ShaderProgram_new,
};

static PyMethodDef CoreMethods[] = {
    {"sin", core_sin, METH_VARARGS, "sine"},
    {"cos", core_cos, METH_VARARGS, "cosine"},
    {"sqrt", core_sqrt, METH_VARARGS, "square root"},
    {"time_seconds", (PyCFunction)core_time_seconds, METH_NOARGS, "current time"},
    {"randint", core_randint, METH_VARARGS, "random integer"},
    {"randuniform", core_randuniform, METH_VARARGS, "random uniform"},
    {"draw_init", (PyCFunction)core_draw_init, METH_NOARGS, "init opengl"},
    {"draw_clear", (PyCFunction)core_draw_clear, METH_NOARGS, "clear screen"},
    {"draw_quad", (PyCFunction)core_draw_quad, METH_NOARGS, "draw a quad"},
    {"load_image", core_load_image, METH_VARARGS, "Load image data from a file"},
    {"render_text", core_render_text, METH_VARARGS, "Render text to a texture"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initcore(void)
{
    srand((uint32_t)time(NULL));

    PyObject *m = Py_InitModule("core", CoreMethods);

    TextureType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&TextureType) < 0) {
        return;
    }
    Py_INCREF(&TextureType);
    PyModule_AddObject(m, "Texture", (PyObject *)&TextureType);

    FramebufferType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&FramebufferType) < 0) {
        return;
    }
    Py_INCREF(&FramebufferType);
    PyModule_AddObject(m, "Framebuffer", (PyObject *)&FramebufferType);

    ShaderProgramType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&ShaderProgramType) < 0) {
        return;
    }
    Py_INCREF(&ShaderProgramType);
    PyModule_AddObject(m, "ShaderProgram", (PyObject *)&ShaderProgramType);
}
