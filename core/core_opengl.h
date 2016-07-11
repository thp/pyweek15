#include "core_common.h"

static void
draw_init()
{
}

typedef struct {
    PyObject_HEAD

    int w;
    int h;
    sf2d_texture *texture;
} TextureObject;

static void
Texture_dealloc(TextureObject *self)
{
    if (self->texture) sf2d_free_texture(self->texture);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Texture_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    TextureObject *self = (TextureObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->w = 0;
        self->h = 0;
        self->texture = NULL;
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

    sf2d_texfmt format = (comp == 2) ? TEXFMT_IA8 : ((comp == 4) ? TEXFMT_RGBA8 : TEXFMT_RGB8);
    self->texture = sf2d_create_texture(self->w, self->h, format, SF2D_PLACE_RAM);

    if (rgba) {
        for (int y=0; y<self->h; y++) {
            char *dst = self->texture->data + comp * self->texture->pow2_w * y;
            const char *src = rgba + comp * self->w * y;
            memcpy(dst, src, comp * self->w);
        }
    }
    sf2d_texture_tile32(self->texture);

    // Because we have reduced it before
    self->w *= 2;
    self->h *= 2;

    return 0;
}

static PyObject *
Texture_bind(TextureObject *self)
{
    Py_RETURN_NONE;
}

static PyMemberDef
Texture_members[] = {
    {"w", T_INT, offsetof(TextureObject, w), 0, "width"},
    {"h", T_INT, offsetof(TextureObject, h), 0, "height"},
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

    PyObject *texture;
} FramebufferObject;

static void
Framebuffer_dealloc(FramebufferObject *self)
{
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Framebuffer_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    FramebufferObject *self = (FramebufferObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
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

    return 0;
}

static PyObject *
Framebuffer_bind(FramebufferObject *self)
{
    Py_RETURN_NONE;
}

static PyObject *
Framebuffer_unbind(FramebufferObject *self)
{
    Py_RETURN_NONE;
}

static PyObject *
Framebuffer_begin(FramebufferObject *self)
{
    sf2d_start_frame(GFX_TOP, GFX_LEFT);
    Py_RETURN_NONE;
}

static PyObject *
Framebuffer_finish(FramebufferObject *self)
{
    sf2d_end_frame();
    Py_RETURN_NONE;
}

static PyMemberDef
Framebuffer_members[] = {
    {"texture", T_OBJECT_EX, offsetof(FramebufferObject, texture), 0, "Texture object"},
    {NULL}
};

static PyMethodDef
Framebuffer_methods[] = {
    {"bind", (PyCFunction)Framebuffer_bind, METH_NOARGS, "Bind the framebuffer as render target"},
    {"unbind", (PyCFunction)Framebuffer_unbind, METH_NOARGS, "Unbind the framebuffer as render target"},
    {"begin", (PyCFunction)Framebuffer_begin, METH_NOARGS | METH_STATIC, "Rendering of frame begins"},
    {"finish", (PyCFunction)Framebuffer_finish, METH_NOARGS | METH_STATIC, "Rendering of frame ends"},
    {NULL}
};

DEFINE_TYPE(Framebuffer);

typedef struct {
    PyObject_HEAD

    float *vertex_buffer;
} ShaderProgramObject;

static void
ShaderProgram_dealloc(ShaderProgramObject *self)
{
    free(self->vertex_buffer);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
ShaderProgram_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    ShaderProgramObject *self = (ShaderProgramObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
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

    // 2 component position, 2 component texture coordinate, 4 vertices
    self->vertex_buffer = malloc(sizeof(float) * 2 * 2 * 4);

    return 0;
}

static PyObject *
ShaderProgram_bind(ShaderProgramObject *self)
{
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

    float r = 1.f;
    float g = 1.f;
    float b = 1.f;
    float a = 1.f;

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while (PyDict_Next(uniforms, &pos, &key, &value)) {
        if (!PyString_Check(key)) {
            return NULL;
        }

        const char *name = PyString_AsString(key);

        if (PyNumber_Check(value)) {
            PyObject *vo = PyNumber_Float(value);
            float v0 = PyFloat_AsDouble(vo);
            // TODO: Could use v0 here
            (void)v0;
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

            if (comp == 4 && strcmp(name, "color") == 0) {
                r = v[0];
                g = v[1];
                b = v[2];
                a = v[3];
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

    float x0 = self->vertex_buffer[0*4+0] / 2.f;
    float y0 = self->vertex_buffer[0*4+1] / 2.f;
    float x1 = self->vertex_buffer[3*4+0] / 2.f;
    float y1 = self->vertex_buffer[3*4+1] / 2.f;

    float left = x0;
    float right = x1;
    float top = y0;
    float bottom = y1;

    float fx = (float)(texture->texture->width) / (float)(texture->texture->pow2_w);
    float fy = (float)(texture->texture->height) / (float)(texture->texture->pow2_h);

    sf2d_draw_quad_uv_blend(texture->texture, left, top, right, bottom, 0.f, 0.f, fx, fy,
                            RGBA8((int)(r*255), (int)(g*255), (int)(b*255), (int)(a*255)));

    Py_RETURN_NONE;
}

static PyMemberDef
ShaderProgram_members[] = {
    {NULL}
};

static PyMethodDef
ShaderProgram_methods[] = {
    {"bind", (PyCFunction)ShaderProgram_bind, METH_NOARGS, "Use the shader program for rendering"},
    {"draw_quad", (PyCFunction)ShaderProgram_draw_quad, METH_VARARGS, "Draw a textured quad"},
    {NULL}
};

DEFINE_TYPE(ShaderProgram);