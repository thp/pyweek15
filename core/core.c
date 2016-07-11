#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <dirent.h>
#include <Python.h>
#include "structmember.h"

#include <SDL.h>
#include <SDL_mixer.h>

#include <OpenGL/GL.h>

#define STB_IMAGE_IMPLEMENTATION
#define STBI_ONLY_PNG
#define STBI_ONLY_JPEG
#include "stb_image.h"

#include "fontaine.h"

#define DEFINE_TYPE(name) \
    static PyTypeObject \
    name##Type = { \
        PyObject_HEAD_INIT(NULL) \
        .tp_name = "core." #name, \
        .tp_basicsize = sizeof(name##Object), \
        .tp_dealloc = (destructor)name##_dealloc, \
        .tp_flags = Py_TPFLAGS_DEFAULT, \
        .tp_doc = #name, \
        .tp_methods = name##_methods, \
        .tp_members = name##_members, \
        .tp_init = (initproc)name##_init, \
        .tp_new = name##_new, \
    }


static PyTypeObject TextureType;

static char *
resolve_file_path(const char *filename)
{
    char *result;
    asprintf(&result, "data/%s", filename);
    return result;
}

static char **
list_files(const char *dirname, int *count)
{
    char *path = resolve_file_path(dirname);
    DIR *dir = opendir(path);
    free(path);

    int used = 0;
    int size = 16;

    char **result = malloc(sizeof(char *) * size);

    struct dirent *ent;
    while ((ent = readdir(dir)) != NULL) {
        if (strcmp(ent->d_name, ".") == 0 || strcmp(ent->d_name, "..") == 0) {
            continue;
        }

        if (used == size) {
            size += size;
            result = realloc(result, sizeof(char *) * size);
        }

        asprintf(&result[used++], "%s/%s", dirname, ent->d_name);
    }

    closedir(dir);

    *count = used;
    return result;
}

void
list_files_free(char **result, int count)
{
    for (int i=0; i<count; i++) {
        free(result[i]);
    }
    free(result);
}

static char *
read_file(const char *filename, int *length)
{
    char *path = resolve_file_path(filename);
    FILE *fp = fopen(path, "rb");
    free(path);

    fseek(fp, 0, SEEK_END);
    int len = (int)ftell(fp);

    char *buf = malloc(len);
    fseek(fp, 0, SEEK_SET);
    fread(buf, len, 1, fp);

    fclose(fp);

    *length = len;
    return buf;
}


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

static PyObject *
core_list_files(PyObject *self, PyObject *args)
{
    const char *dirname;
    if (!PyArg_ParseTuple(args, "s", &dirname)) {
        return NULL;
    }

    int count;
    char **filenames = list_files(dirname, &count);
    PyObject *list = PyList_New(count);
    for (int i=0; i<count; i++) {
        PyList_SET_ITEM(list, i, PyString_FromString(filenames[i]));
    }
    list_files_free(filenames, count);

    return list;
}

static PyObject *
core_read_file(PyObject *self, PyObject *args)
{
    const char *filename;
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }

    int len;
    char *buf = read_file(filename, &len);
    PyObject *contents = PyString_FromStringAndSize(buf, len);
    free(buf);

    return contents;
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

DEFINE_TYPE(Texture);

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
        if (!PyString_Check(key)) {
            return NULL;
        }

        const char *name = PyString_AsString(key);
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

typedef struct {
    PyObject_HEAD

    SDL_Surface *window;
} WindowObject;

static void
Window_dealloc(WindowObject *self)
{
    SDL_Quit();
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Window_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    WindowObject *self = (WindowObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->window = NULL;
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

    self->window = SDL_SetVideoMode(width, height, 0, SDL_OPENGL);
    SDL_WM_SetCaption(title, title);

    Mix_Init(0);
    Mix_OpenAudio(MIX_DEFAULT_FREQUENCY, AUDIO_S16LSB, 2, 1024);

    return 0;
}

static PyObject *
Window_swap_buffers(WindowObject *self)
{
    SDL_GL_SwapBuffers();

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

typedef struct {
    PyObject_HEAD

    Mix_Chunk *chunk;
} SoundObject;

static void
Sound_dealloc(SoundObject *self)
{
    Mix_FreeChunk(self->chunk);
    self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Sound_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    SoundObject *self = (SoundObject *)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->chunk = NULL;
    }

    return (PyObject *)self;
}

static int
Sound_init(SoundObject *self, PyObject *args, PyObject *kwargs)
{
    const char *filename;
    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return -1;
    }

    int len;
    char *buf = read_file(filename, &len);
    self->chunk = Mix_LoadWAV_RW(SDL_RWFromConstMem(buf, len), 1);
    free(buf);

    return 0;
}

static PyObject *
Sound_play(SoundObject *self)
{
    Mix_PlayChannel(-1, self->chunk, 0);

    Py_RETURN_NONE;
}

static PyMemberDef
Sound_members[] = {
    {NULL}
};

static PyMethodDef
Sound_methods[] = {
    {"play", (PyCFunction)Sound_play, METH_NOARGS, "Play the sound effect"},
    {NULL}
};

DEFINE_TYPE(Sound);

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
    unsigned char *pixels2 = malloc(width * height * 2);
    // LUMINANCE_ALPHA format needs 2 bytes per pixels -- use that opportunity to make
    // the luminance part white (0xFF) and only take the alpha channel from the font
    for (int i=0; i<width*height; i++) {
        pixels2[i*2+0] = 0xFF;
        pixels2[i*2+1] = pixels[i];
    }
    fontaine_free_pixels(self->font, pixels);

    PyObject *rgba = PyString_FromStringAndSize((const char *)pixels2, width * height * 2);
    free(pixels2);

    PyObject *textureArgs = Py_BuildValue("iiNi", width, height, rgba, 2);
    TextureObject *result = (TextureObject *)PyObject_CallObject((PyObject *)&TextureType, textureArgs);
    Py_DECREF(textureArgs);

    result->w *= self->size;
    result->h *= self->size;

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

static PyMethodDef CoreMethods[] = {
    {"sin", core_sin, METH_VARARGS, "sine"},
    {"cos", core_cos, METH_VARARGS, "cosine"},
    {"sqrt", core_sqrt, METH_VARARGS, "square root"},
    {"time_seconds", (PyCFunction)core_time_seconds, METH_NOARGS, "current time"},
    {"randint", core_randint, METH_VARARGS, "random integer"},
    {"randuniform", core_randuniform, METH_VARARGS, "random uniform"},
    {"draw_init", (PyCFunction)core_draw_init, METH_NOARGS, "init opengl"},
    {"load_image", core_load_image, METH_VARARGS, "Load image data from a file"},
    {"list_files", core_list_files, METH_VARARGS, "List files in a directory by extension"},
    {"read_file", core_read_file, METH_VARARGS, "Read a file and return its data as str"},
    {NULL, NULL, 0, NULL}
};

#define INIT_TYPE(name) \
    name##Type.tp_new = PyType_GenericNew; \
    PyType_Ready(&name##Type); \
    Py_INCREF(&name##Type); \
    PyModule_AddObject(m, #name, (PyObject *)&name##Type)

PyMODINIT_FUNC
initcore(void)
{
    srand((uint32_t)time(NULL));

    PyObject *m = Py_InitModule("core", CoreMethods);

    INIT_TYPE(Texture);
    INIT_TYPE(Framebuffer);
    INIT_TYPE(ShaderProgram);
    INIT_TYPE(Window);
    INIT_TYPE(Sound);
    INIT_TYPE(Font);
}
