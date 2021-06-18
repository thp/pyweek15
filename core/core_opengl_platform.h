#if defined(__APPLE__)
#define GL_SILENCE_DEPRECATION
#include <OpenGL/GL.h>
#else
#define GL_GLEXT_PROTOTYPES
#include <GL/gl.h>
#include <GL/glext.h>
#endif
