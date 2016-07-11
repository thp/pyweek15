#include "core.h"

#include "core_common.h"

#include "core_image.h"
#include "core_fileio.h"
#include "core_window.h"
#include "core_sound.h"
#include "core_font.h"
#include "core_opengl.h"
#include "core_vfs.h"
#include "core_time.h"
#include "core_math.h"
#include "core_random.h"

#define INIT_TYPE(name) \
    name##Type.tp_new = PyType_GenericNew; \
    PyType_Ready(&name##Type); \
    Py_INCREF(&name##Type); \
    PyModule_AddObject(m, #name, (PyObject *)&name##Type)

PyMODINIT_FUNC
initcore(void)
{
    PyObject *m = Py_InitModule("core", NULL);

    INIT_TYPE(Texture);
    INIT_TYPE(Framebuffer);
    INIT_TYPE(ShaderProgram);
    INIT_TYPE(Window);
    INIT_TYPE(Sound);
    INIT_TYPE(Font);
    INIT_TYPE(VFS);
    INIT_TYPE(Image);

    INIT_TYPE(time);
    INIT_TYPE(math);
    INIT_TYPE(random);
}
