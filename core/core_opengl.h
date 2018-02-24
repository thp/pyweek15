#include "core_common.h"

#include "core_opengl_platform.h"

static struct {
    GLint viewport[4];
} g;

static void
draw_init()
{
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    glEnableVertexAttribArray(0);
    glEnableVertexAttribArray(1);
    glGetIntegerv(GL_VIEWPORT, g.viewport);
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
    Py_TYPE(self)->tp_free((PyObject *)self);
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

    if (rgba_len != 0 && rgba_len != (self->w * self->h * comp)) {
        return -1;
    }

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

DEFINE_TYPE(Texture);

typedef struct {
    PyObject_HEAD

    GLuint framebuffer_id;
    int width;
    int height;
    PyObject *texture;
} FramebufferObject;

static void
Framebuffer_dealloc(FramebufferObject *self)
{
    glDeleteFramebuffers(1, &self->framebuffer_id);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
Framebuffer_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    FramebufferObject *self = (FramebufferObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->framebuffer_id = 0;
        self->width = 0;
        self->height = 0;
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

    PyObject *textureArgs = Py_BuildValue("iisi", width, height, NULL, 3);
    self->texture = PyObject_CallObject((PyObject *)&TextureType, textureArgs);
    Py_DECREF(textureArgs);

    glGenFramebuffers(1, &self->framebuffer_id);
    self->width = width;
    self->height = height;

    glBindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_id);
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, ((TextureObject *)(self->texture))->texture_id, 0);
    glBindFramebuffer(GL_FRAMEBUFFER, 0);

    return 0;
}

static PyObject *
Framebuffer_bind(FramebufferObject *self)
{
    glBindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_id);
    glViewport(0, 0, self->width, self->height);
    Py_RETURN_NONE;
}

static PyObject *
Framebuffer_unbind(FramebufferObject *self)
{
    glBindFramebuffer(GL_FRAMEBUFFER, 0);
    glViewport(g.viewport[0], g.viewport[1], g.viewport[2], g.viewport[3]);
    Py_RETURN_NONE;
}

static PyObject *
Framebuffer_begin(FramebufferObject *self)
{
    Py_RETURN_NONE;
}

static PyObject *
Framebuffer_finish(FramebufferObject *self)
{
    Py_RETURN_NONE;
}

static PyObject *
Framebuffer_supported(FramebufferObject *self)
{
    Py_RETURN_TRUE;
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
    {"begin", (PyCFunction)Framebuffer_begin, METH_NOARGS | METH_STATIC, "Rendering of frame begins"},
    {"finish", (PyCFunction)Framebuffer_finish, METH_NOARGS | METH_STATIC, "Rendering of frame ends"},
    {"supported", (PyCFunction)Framebuffer_supported, METH_NOARGS | METH_STATIC, "True if we support FBOs and shaders"},
    {NULL}
};

DEFINE_TYPE(Framebuffer);

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
    Py_TYPE(self)->tp_free((PyObject *)self);
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

#if defined(USE_OPENGL_ES)
    const char *prefix = "precision mediump float;";
#else
    const char *prefix = "";
#endif

    const char *src[2] = {
        prefix,
        vertex_shader_src,
    };

    GLuint vertex_shader_id = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertex_shader_id, sizeof(src) / sizeof(src[0]), src, NULL);
    glCompileShader(vertex_shader_id);
    glAttachShader(self->program_id, vertex_shader_id);
    glDeleteShader(vertex_shader_id);

    src[1] = fragment_shader_src;

    GLuint fragment_shader_id = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragment_shader_id, sizeof(src) / sizeof(src[0]), src, NULL);
    glCompileShader(fragment_shader_id);
    glAttachShader(self->program_id, fragment_shader_id);
    glDeleteShader(fragment_shader_id);

    glBindAttribLocation(self->program_id, 0, "position");
    glBindAttribLocation(self->program_id, 1, "texcoord");

    glLinkProgram(self->program_id);

    // 2 component position, 2 component texture coordinate, 4 vertices
    self->vertex_buffer = malloc(sizeof(float) * 2 * 2 * 4);

    return 0;
}

static PyObject *
ShaderProgram_bind(ShaderProgramObject *self)
{
    glUseProgram(self->program_id);
    Py_RETURN_NONE;
}

static PyObject *
ShaderProgram_draw_quad(ShaderProgramObject *self, PyObject *args)
{
    TextureObject *texture;
    PyObject *position;
    PyObject *uniforms;
    if (!PyArg_ParseTuple(args, "OOO", (PyObject **)&texture, &position, &uniforms)) {
        return NULL;
    }

    if (!PyList_Check(position) || PyList_Size(position) != (2 * 4)) {
        return NULL;
    }

    if (!PyDict_Check(uniforms)) {
        return NULL;
    }

    ShaderProgram_bind(self);
    Texture_bind(texture);

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while (PyDict_Next(uniforms, &pos, &key, &value)) {
        if (!PyUnicode_Check(key)) {
            return NULL;
        }

        const char *name = PyUnicode_AsUTF8(key);
        int location = glGetUniformLocation(self->program_id, name);

        if (PyNumber_Check(value)) {
            PyObject *vo = PyNumber_Float(value);
            glUniform1f(location, PyFloat_AsDouble(vo));
            Py_DECREF(vo);
        } else if (PyTuple_Check(value)) {
            size_t comp = PyTuple_GET_SIZE(value);
            float v[comp];
            for (int i=0; i<comp; i++) {
                PyObject *item = PyTuple_GET_ITEM(value, i);
                if (!PyNumber_Check(item)) {
                    return NULL;
                }

                PyObject *vo = PyNumber_Float(item);
                v[i] = PyFloat_AsDouble(vo);
                Py_DECREF(vo);
            }

            switch (comp) {
                case 1: glUniform1f(location, v[0]); break;
                case 2: glUniform2f(location, v[0], v[1]); break;
                case 3: glUniform3f(location, v[0], v[1], v[2]); break;
                case 4: glUniform4f(location, v[0], v[1], v[2], v[3]); break;
                default: return NULL;
            }
        } else {
            return NULL;
        }
    }

    float texcoord[] = { 0.f, 0.f, 0.f, 1.f, 1.f, 0.f, 1.f, 1.f, };
    for (int i=0; i<4; i++) {
        self->vertex_buffer[i*4+0] = PyFloat_AsDouble(PyList_GET_ITEM(position, i*2+0));
        self->vertex_buffer[i*4+1] = PyFloat_AsDouble(PyList_GET_ITEM(position, i*2+1));
        self->vertex_buffer[i*4+2] = texcoord[i*2+0];
        self->vertex_buffer[i*4+3] = texcoord[i*2+1];
    }

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 4, &self->vertex_buffer[0]);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 4, &self->vertex_buffer[2]);

    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

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
    {"draw_quad", (PyCFunction)ShaderProgram_draw_quad, METH_VARARGS, "Draw a textured quad"},
    {NULL}
};

DEFINE_TYPE(ShaderProgram);
