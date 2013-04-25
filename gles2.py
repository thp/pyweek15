
# Automatically generated from gl2.h
# Generator: header2py.py by Thomas Perl <thp.io/about>

from ctypes import *

glesv2 = cdll.LoadLibrary('libGLESv2.so')







# ignored typedef: GLvoid
GLenum = c_uint
GLboolean = c_ubyte
GLbitfield = c_uint
GLbyte = c_byte
GLshort = c_short
GLint = c_int
GLsizei = c_int
GLubyte = c_ubyte
GLushort = c_ushort
GLuint = c_uint
GLfloat = c_float
GLclampf = c_float
GLfixed = c_int
GLclampx = c_int

# GL types for handling large vertex buffer objects
GLintptr = c_int
GLsizeiptr = c_int

# OpenGL ES core versions
GL_ES_VERSION_2_0 = 1

# ClearBufferMask
GL_DEPTH_BUFFER_BIT = 0x00000100
GL_STENCIL_BUFFER_BIT = 0x00000400
GL_COLOR_BUFFER_BIT = 0x00004000

# Boolean
GL_FALSE = 0
GL_TRUE = 1

# \todo check that this should be in core.
GL_NONE = 0

# BeginMode
GL_POINTS = 0x0000
GL_LINES = 0x0001
GL_LINE_LOOP = 0x0002
GL_LINE_STRIP = 0x0003
GL_TRIANGLES = 0x0004
GL_TRIANGLE_STRIP = 0x0005
GL_TRIANGLE_FAN = 0x0006

# AlphaFunction (not supported in ES20)
# GL_NEVER
# GL_LESS
# GL_EQUAL
# GL_LEQUAL
# GL_GREATER
# GL_NOTEQUAL
# GL_GEQUAL
# GL_ALWAYS

# BlendingFactorDest
GL_ZERO = 0
GL_ONE = 1
GL_SRC_COLOR = 0x0300
GL_ONE_MINUS_SRC_COLOR = 0x0301
GL_SRC_ALPHA = 0x0302
GL_ONE_MINUS_SRC_ALPHA = 0x0303
GL_DST_ALPHA = 0x0304
GL_ONE_MINUS_DST_ALPHA = 0x0305

# BlendingFactorSrc
# GL_ZERO
# GL_ONE
GL_DST_COLOR = 0x0306
GL_ONE_MINUS_DST_COLOR = 0x0307
GL_SRC_ALPHA_SATURATE = 0x0308
# GL_SRC_ALPHA
# GL_ONE_MINUS_SRC_ALPHA
# GL_DST_ALPHA
# GL_ONE_MINUS_DST_ALPHA

# BlendEquationSeparate
GL_FUNC_ADD = 0x8006
GL_BLEND_EQUATION = 0x8009
GL_BLEND_EQUATION_RGB = 0x8009	#  same as BLEND_EQUATION
GL_BLEND_EQUATION_ALPHA = 0x883D

# BlendSubtract
GL_FUNC_SUBTRACT = 0x800A
GL_FUNC_REVERSE_SUBTRACT = 0x800B

# Separate Blend Functions
GL_BLEND_DST_RGB = 0x80C8
GL_BLEND_SRC_RGB = 0x80C9
GL_BLEND_DST_ALPHA = 0x80CA
GL_BLEND_SRC_ALPHA = 0x80CB
GL_CONSTANT_COLOR = 0x8001
GL_ONE_MINUS_CONSTANT_COLOR = 0x8002
GL_CONSTANT_ALPHA = 0x8003
GL_ONE_MINUS_CONSTANT_ALPHA = 0x8004
GL_BLEND_COLOR = 0x8005

# Buffer Objects
GL_ARRAY_BUFFER = 0x8892
GL_ELEMENT_ARRAY_BUFFER = 0x8893
GL_ARRAY_BUFFER_BINDING = 0x8894
GL_ELEMENT_ARRAY_BUFFER_BINDING = 0x8895

GL_STREAM_DRAW = 0x88E0
GL_STATIC_DRAW = 0x88E4
GL_DYNAMIC_DRAW = 0x88E8

GL_BUFFER_SIZE = 0x8764
GL_BUFFER_USAGE = 0x8765

GL_CURRENT_VERTEX_ATTRIB = 0x8626

# CullFaceMode
GL_FRONT = 0x0404
GL_BACK = 0x0405
GL_FRONT_AND_BACK = 0x0408

# DepthFunction
# GL_NEVER
# GL_LESS
# GL_EQUAL
# GL_LEQUAL
# GL_GREATER
# GL_NOTEQUAL
# GL_GEQUAL
# GL_ALWAYS

# EnableCap
GL_TEXTURE_2D = 0x0DE1
GL_CULL_FACE = 0x0B44
GL_BLEND = 0x0BE2
GL_DITHER = 0x0BD0
GL_STENCIL_TEST = 0x0B90
GL_DEPTH_TEST = 0x0B71
GL_SCISSOR_TEST = 0x0C11
GL_POLYGON_OFFSET_FILL = 0x8037
GL_SAMPLE_ALPHA_TO_COVERAGE = 0x809E
GL_SAMPLE_COVERAGE = 0x80A0

# ErrorCode
GL_NO_ERROR = 0
GL_INVALID_ENUM = 0x0500
GL_INVALID_VALUE = 0x0501
GL_INVALID_OPERATION = 0x0502
GL_OUT_OF_MEMORY = 0x0505

# FrontFaceDirection
GL_CW = 0x0900
GL_CCW = 0x0901

# GetPName
GL_LINE_WIDTH = 0x0B21
GL_ALIASED_POINT_SIZE_RANGE = 0x846D
GL_ALIASED_LINE_WIDTH_RANGE = 0x846E
GL_CULL_FACE_MODE = 0x0B45
GL_FRONT_FACE = 0x0B46
GL_DEPTH_RANGE = 0x0B70
GL_DEPTH_WRITEMASK = 0x0B72
GL_DEPTH_CLEAR_VALUE = 0x0B73
GL_DEPTH_FUNC = 0x0B74
GL_STENCIL_CLEAR_VALUE = 0x0B91
GL_STENCIL_FUNC = 0x0B92
GL_STENCIL_FAIL = 0x0B94
GL_STENCIL_PASS_DEPTH_FAIL = 0x0B95
GL_STENCIL_PASS_DEPTH_PASS = 0x0B96
GL_STENCIL_REF = 0x0B97
GL_STENCIL_VALUE_MASK = 0x0B93
GL_STENCIL_WRITEMASK = 0x0B98
GL_STENCIL_BACK_FUNC = 0x8800
GL_STENCIL_BACK_FAIL = 0x8801
GL_STENCIL_BACK_PASS_DEPTH_FAIL = 0x8802
GL_STENCIL_BACK_PASS_DEPTH_PASS = 0x8803
GL_STENCIL_BACK_REF = 0x8CA3
GL_STENCIL_BACK_VALUE_MASK = 0x8CA4
GL_STENCIL_BACK_WRITEMASK = 0x8CA5
GL_VIEWPORT = 0x0BA2
GL_SCISSOR_BOX = 0x0C10
# GL_SCISSOR_TEST
GL_COLOR_CLEAR_VALUE = 0x0C22
GL_COLOR_WRITEMASK = 0x0C23
GL_UNPACK_ALIGNMENT = 0x0CF5
GL_PACK_ALIGNMENT = 0x0D05
GL_MAX_TEXTURE_SIZE = 0x0D33
GL_MAX_VIEWPORT_DIMS = 0x0D3A
GL_SUBPIXEL_BITS = 0x0D50
GL_RED_BITS = 0x0D52
GL_GREEN_BITS = 0x0D53
GL_BLUE_BITS = 0x0D54
GL_ALPHA_BITS = 0x0D55
GL_DEPTH_BITS = 0x0D56
GL_STENCIL_BITS = 0x0D57
GL_POLYGON_OFFSET_UNITS = 0x2A00
# GL_POLYGON_OFFSET_FILL
GL_POLYGON_OFFSET_FACTOR = 0x8038
GL_TEXTURE_BINDING_2D = 0x8069
GL_SAMPLE_BUFFERS = 0x80A8
GL_SAMPLES = 0x80A9
GL_SAMPLE_COVERAGE_VALUE = 0x80AA
GL_SAMPLE_COVERAGE_INVERT = 0x80AB

# GetTextureParameter
# GL_TEXTURE_MAG_FILTER
# GL_TEXTURE_MIN_FILTER
# GL_TEXTURE_WRAP_S
# GL_TEXTURE_WRAP_T

GL_NUM_COMPRESSED_TEXTURE_FORMATS = 0x86A2
GL_COMPRESSED_TEXTURE_FORMATS = 0x86A3

# HintMode
GL_DONT_CARE = 0x1100
GL_FASTEST = 0x1101
GL_NICEST = 0x1102

# HintTarget
GL_GENERATE_MIPMAP_HINT = 0x8192

# DataType
GL_BYTE = 0x1400
GL_UNSIGNED_BYTE = 0x1401
GL_SHORT = 0x1402
GL_UNSIGNED_SHORT = 0x1403
GL_INT = 0x1404
GL_UNSIGNED_INT = 0x1405
GL_FLOAT = 0x1406
GL_FIXED = 0x140C

# PixelFormat
GL_DEPTH_COMPONENT = 0x1902
GL_ALPHA = 0x1906
GL_RGB = 0x1907
GL_RGBA = 0x1908
GL_LUMINANCE = 0x1909
GL_LUMINANCE_ALPHA = 0x190A

# PixelType
# GL_UNSIGNED_BYTE
GL_UNSIGNED_SHORT_4_4_4_4 = 0x8033
GL_UNSIGNED_SHORT_5_5_5_1 = 0x8034
GL_UNSIGNED_SHORT_5_6_5 = 0x8363

# Shaders
GL_FRAGMENT_SHADER = 0x8B30
GL_VERTEX_SHADER = 0x8B31
GL_MAX_VERTEX_ATTRIBS = 0x8869
GL_MAX_VERTEX_UNIFORM_VECTORS = 0x8DFB
GL_MAX_VARYING_VECTORS = 0x8DFC
GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS = 0x8B4D
GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS = 0x8B4C
GL_MAX_TEXTURE_IMAGE_UNITS = 0x8872
GL_MAX_FRAGMENT_UNIFORM_VECTORS = 0x8DFD
GL_SHADER_TYPE = 0x8B4F
GL_DELETE_STATUS = 0x8B80
GL_LINK_STATUS = 0x8B82
GL_VALIDATE_STATUS = 0x8B83
GL_ATTACHED_SHADERS = 0x8B85
GL_ACTIVE_UNIFORMS = 0x8B86
GL_ACTIVE_UNIFORM_MAX_LENGTH = 0x8B87
GL_ACTIVE_ATTRIBUTES = 0x8B89
GL_ACTIVE_ATTRIBUTE_MAX_LENGTH = 0x8B8A
GL_SHADING_LANGUAGE_VERSION = 0x8B8C
GL_CURRENT_PROGRAM = 0x8B8D

# StencilFunction
GL_NEVER = 0x0200
GL_LESS = 0x0201
GL_EQUAL = 0x0202
GL_LEQUAL = 0x0203
GL_GREATER = 0x0204
GL_NOTEQUAL = 0x0205
GL_GEQUAL = 0x0206
GL_ALWAYS = 0x0207

# StencilOp
# GL_ZERO
GL_KEEP = 0x1E00
GL_REPLACE = 0x1E01
GL_INCR = 0x1E02
GL_DECR = 0x1E03
GL_INVERT = 0x150A
GL_INCR_WRAP = 0x8507
GL_DECR_WRAP = 0x8508

# StringName
GL_VENDOR = 0x1F00
GL_RENDERER = 0x1F01
GL_VERSION = 0x1F02
GL_EXTENSIONS = 0x1F03

# TextureMagFilter
GL_NEAREST = 0x2600
GL_LINEAR = 0x2601

# TextureMinFilter
# GL_NEAREST
# GL_LINEAR
GL_NEAREST_MIPMAP_NEAREST = 0x2700
GL_LINEAR_MIPMAP_NEAREST = 0x2701
GL_NEAREST_MIPMAP_LINEAR = 0x2702
GL_LINEAR_MIPMAP_LINEAR = 0x2703

# TextureParameterName
GL_TEXTURE_MAG_FILTER = 0x2800
GL_TEXTURE_MIN_FILTER = 0x2801
GL_TEXTURE_WRAP_S = 0x2802
GL_TEXTURE_WRAP_T = 0x2803

# TextureTarget
# GL_TEXTURE_2D
GL_TEXTURE = 0x1702

GL_TEXTURE_CUBE_MAP = 0x8513
GL_TEXTURE_BINDING_CUBE_MAP = 0x8514
GL_TEXTURE_CUBE_MAP_POSITIVE_X = 0x8515
GL_TEXTURE_CUBE_MAP_NEGATIVE_X = 0x8516
GL_TEXTURE_CUBE_MAP_POSITIVE_Y = 0x8517
GL_TEXTURE_CUBE_MAP_NEGATIVE_Y = 0x8518
GL_TEXTURE_CUBE_MAP_POSITIVE_Z = 0x8519
GL_TEXTURE_CUBE_MAP_NEGATIVE_Z = 0x851A
GL_MAX_CUBE_MAP_TEXTURE_SIZE = 0x851C

# TextureUnit
GL_TEXTURE0 = 0x84C0
GL_TEXTURE1 = 0x84C1
GL_TEXTURE2 = 0x84C2
GL_TEXTURE3 = 0x84C3
GL_TEXTURE4 = 0x84C4
GL_TEXTURE5 = 0x84C5
GL_TEXTURE6 = 0x84C6
GL_TEXTURE7 = 0x84C7
GL_TEXTURE8 = 0x84C8
GL_TEXTURE9 = 0x84C9
GL_TEXTURE10 = 0x84CA
GL_TEXTURE11 = 0x84CB
GL_TEXTURE12 = 0x84CC
GL_TEXTURE13 = 0x84CD
GL_TEXTURE14 = 0x84CE
GL_TEXTURE15 = 0x84CF
GL_TEXTURE16 = 0x84D0
GL_TEXTURE17 = 0x84D1
GL_TEXTURE18 = 0x84D2
GL_TEXTURE19 = 0x84D3
GL_TEXTURE20 = 0x84D4
GL_TEXTURE21 = 0x84D5
GL_TEXTURE22 = 0x84D6
GL_TEXTURE23 = 0x84D7
GL_TEXTURE24 = 0x84D8
GL_TEXTURE25 = 0x84D9
GL_TEXTURE26 = 0x84DA
GL_TEXTURE27 = 0x84DB
GL_TEXTURE28 = 0x84DC
GL_TEXTURE29 = 0x84DD
GL_TEXTURE30 = 0x84DE
GL_TEXTURE31 = 0x84DF
GL_ACTIVE_TEXTURE = 0x84E0

# TextureWrapMode
GL_REPEAT = 0x2901
GL_CLAMP_TO_EDGE = 0x812F
GL_MIRRORED_REPEAT = 0x8370

# Uniform Types
GL_FLOAT_VEC2 = 0x8B50
GL_FLOAT_VEC3 = 0x8B51
GL_FLOAT_VEC4 = 0x8B52
GL_INT_VEC2 = 0x8B53
GL_INT_VEC3 = 0x8B54
GL_INT_VEC4 = 0x8B55
GL_BOOL = 0x8B56
GL_BOOL_VEC2 = 0x8B57
GL_BOOL_VEC3 = 0x8B58
GL_BOOL_VEC4 = 0x8B59
GL_FLOAT_MAT2 = 0x8B5A
GL_FLOAT_MAT3 = 0x8B5B
GL_FLOAT_MAT4 = 0x8B5C
GL_SAMPLER_2D = 0x8B5E
GL_SAMPLER_CUBE = 0x8B60

# Vertex Arrays
GL_VERTEX_ATTRIB_ARRAY_ENABLED = 0x8622
GL_VERTEX_ATTRIB_ARRAY_SIZE = 0x8623
GL_VERTEX_ATTRIB_ARRAY_STRIDE = 0x8624
GL_VERTEX_ATTRIB_ARRAY_TYPE = 0x8625
GL_VERTEX_ATTRIB_ARRAY_NORMALIZED = 0x886A
GL_VERTEX_ATTRIB_ARRAY_POINTER = 0x8645
GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING = 0x889F

# Read Format
GL_IMPLEMENTATION_COLOR_READ_TYPE = 0x8B9A
GL_IMPLEMENTATION_COLOR_READ_FORMAT = 0x8B9B

# Shader Source
GL_COMPILE_STATUS = 0x8B81
GL_INFO_LOG_LENGTH = 0x8B84
GL_SHADER_SOURCE_LENGTH = 0x8B88
GL_SHADER_COMPILER = 0x8DFA

# Shader Binary
GL_PLATFORM_BINARY = 0x8D63
GL_SHADER_BINARY_FORMATS = 0x8DF8
GL_NUM_SHADER_BINARY_FORMATS = 0x8DF9

# Shader Precision-Specified Types
GL_LOW_FLOAT = 0x8DF0
GL_MEDIUM_FLOAT = 0x8DF1
GL_HIGH_FLOAT = 0x8DF2
GL_LOW_INT = 0x8DF3
GL_MEDIUM_INT = 0x8DF4
GL_HIGH_INT = 0x8DF5

# Framebuffer Object.
GL_FRAMEBUFFER = 0x8D40
GL_RENDERBUFFER = 0x8D41

GL_RGBA4 = 0x8056
GL_RGB5_A1 = 0x8057
GL_RGB565 = 0x8D62
GL_DEPTH_COMPONENT16 = 0x81A5
GL_STENCIL_INDEX = 0x1901
GL_STENCIL_INDEX8 = 0x8D48

GL_RENDERBUFFER_WIDTH = 0x8D42
GL_RENDERBUFFER_HEIGHT = 0x8D43
GL_RENDERBUFFER_INTERNAL_FORMAT = 0x8D44
GL_RENDERBUFFER_RED_SIZE = 0x8D50
GL_RENDERBUFFER_GREEN_SIZE = 0x8D51
GL_RENDERBUFFER_BLUE_SIZE = 0x8D52
GL_RENDERBUFFER_ALPHA_SIZE = 0x8D53
GL_RENDERBUFFER_DEPTH_SIZE = 0x8D54
GL_RENDERBUFFER_STENCIL_SIZE = 0x8D55

GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE = 0x8CD0
GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME = 0x8CD1
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL = 0x8CD2
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE = 0x8CD3

GL_COLOR_ATTACHMENT0 = 0x8CE0
GL_DEPTH_ATTACHMENT = 0x8D00
GL_STENCIL_ATTACHMENT = 0x8D20

GL_FRAMEBUFFER_COMPLETE = 0x8CD5
GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT = 0x8CD6
GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT = 0x8CD7
GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS = 0x8CD9
GL_FRAMEBUFFER_INCOMPLETE_FORMATS = 0x8CDA
GL_FRAMEBUFFER_UNSUPPORTED = 0x8CDD

GL_FRAMEBUFFER_BINDING = 0x8CA6
GL_RENDERBUFFER_BINDING = 0x8CA7
GL_MAX_RENDERBUFFER_SIZE = 0x84E8

GL_INVALID_FRAMEBUFFER_OPERATION = 0x0506


def glActiveTexture(texture):
    return glesv2.glActiveTexture(texture)

def glAttachShader(program, shader):
    return glesv2.glAttachShader(program, shader)

def glBindAttribLocation(program, index, name):
    return glesv2.glBindAttribLocation(program, index, name)

def glBindBuffer(target, buffer):
    return glesv2.glBindBuffer(target, buffer)

def glBindFramebuffer(target, framebuffer):
    return glesv2.glBindFramebuffer(target, framebuffer)

def glBindRenderbuffer(target, renderbuffer):
    return glesv2.glBindRenderbuffer(target, renderbuffer)

def glBindTexture(target, texture):
    return glesv2.glBindTexture(target, texture)

def glBlendColor(red, green, blue, alpha):
    return glesv2.glBlendColor(GLclampf(red), GLclampf(green), GLclampf(blue), GLclampf(alpha))

def glBlendEquation(mode):
    return glesv2.glBlendEquation(mode)

def glBlendEquationSeparate(modeRGB, modeAlpha):
    return glesv2.glBlendEquationSeparate(modeRGB, modeAlpha)

def glBlendFunc(sfactor, dfactor):
    return glesv2.glBlendFunc(sfactor, dfactor)

def glBlendFuncSeparate(srcRGB, dstRGB, srcAlpha, dstAlpha):
    return glesv2.glBlendFuncSeparate(srcRGB, dstRGB, srcAlpha, dstAlpha)

def glBufferData(target, size, data, usage):
    return glesv2.glBufferData(target, size, data, usage)

def glBufferSubData(target, offset, size, data):
    return glesv2.glBufferSubData(target, offset, size, data)

def glCheckFramebufferStatus(target):
    return glesv2.glCheckFramebufferStatus(target)

def glClear(mask):
    return glesv2.glClear(mask)

def glClearColor(red, green, blue, alpha):
    return glesv2.glClearColor(GLclampf(red), GLclampf(green), GLclampf(blue), GLclampf(alpha))

def glClearDepthf(depth):
    return glesv2.glClearDepthf(GLclampf(depth))

def glClearStencil(s):
    return glesv2.glClearStencil(s)

def glColorMask(red, green, blue, alpha):
    return glesv2.glColorMask(red, green, blue, alpha)

def glCompileShader(shader):
    return glesv2.glCompileShader(shader)

def glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, data):
    return glesv2.glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, data)

def glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, data):
    return glesv2.glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, data)

def glCopyTexImage2D(target, level, internalformat, x, y, width, height, border):
    return glesv2.glCopyTexImage2D(target, level, internalformat, x, y, width, height, border)

def glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height):
    return glesv2.glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height)

def glCreateProgram():
    return glesv2.glCreateProgram()

def glCreateShader(type):
    return glesv2.glCreateShader(type)

def glCullFace(mode):
    return glesv2.glCullFace(mode)

def glDeleteBuffers(n, buffers):
    return glesv2.glDeleteBuffers(n, buffers)

def glDeleteFramebuffers(n, framebuffers):
    return glesv2.glDeleteFramebuffers(n, framebuffers)

def glDeleteProgram(program):
    return glesv2.glDeleteProgram(program)

def glDeleteRenderbuffers(n, renderbuffers):
    return glesv2.glDeleteRenderbuffers(n, renderbuffers)

def glDeleteShader(shader):
    return glesv2.glDeleteShader(shader)

def glDeleteTextures(n, textures):
    return glesv2.glDeleteTextures(n, textures)

def glDepthFunc(func):
    return glesv2.glDepthFunc(func)

def glDepthMask(flag):
    return glesv2.glDepthMask(flag)

def glDepthRangef(zNear, zFar):
    return glesv2.glDepthRangef(GLclampf(zNear), GLclampf(zFar))

def glDetachShader(program, shader):
    return glesv2.glDetachShader(program, shader)

def glDisable(cap):
    return glesv2.glDisable(cap)

def glDisableVertexAttribArray(index):
    return glesv2.glDisableVertexAttribArray(index)

def glDrawArrays(mode, first, count):
    return glesv2.glDrawArrays(mode, first, count)

def glDrawElements(mode, count, type, indices):
    return glesv2.glDrawElements(mode, count, type, indices)

def glEnable(cap):
    return glesv2.glEnable(cap)

def glEnableVertexAttribArray(index):
    return glesv2.glEnableVertexAttribArray(index)

def glFinish():
    return glesv2.glFinish()

def glFlush():
    return glesv2.glFlush()

def glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer):
    return glesv2.glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer)

def glFramebufferTexture2D(target, attachment, textarget, texture, level):
    return glesv2.glFramebufferTexture2D(target, attachment, textarget, texture, level)

def glFrontFace(mode):
    return glesv2.glFrontFace(mode)

def glGenBuffers(n, buffers):
    return glesv2.glGenBuffers(n, buffers)

def glGenerateMipmap(target):
    return glesv2.glGenerateMipmap(target)

def glGenFramebuffers(n, framebuffers):
    return glesv2.glGenFramebuffers(n, framebuffers)

def glGenRenderbuffers(n, renderbuffers):
    return glesv2.glGenRenderbuffers(n, renderbuffers)

def glGenTextures(n, textures):
    return glesv2.glGenTextures(n, textures)

def glGetActiveAttrib(program, index, bufsize, length, size, type, name):
    return glesv2.glGetActiveAttrib(program, index, bufsize, length, size, type, name)

def glGetActiveUniform(program, index, bufsize, length, size, type, name):
    return glesv2.glGetActiveUniform(program, index, bufsize, length, size, type, name)

def glGetAttachedShaders(program, maxcount, count, shaders):
    return glesv2.glGetAttachedShaders(program, maxcount, count, shaders)

def glGetAttribLocation(program, name):
    return glesv2.glGetAttribLocation(program, name)

def glGetBooleanv(pname, params):
    return glesv2.glGetBooleanv(pname, params)

def glGetBufferParameteriv(target, pname, params):
    return glesv2.glGetBufferParameteriv(target, pname, params)

def glGetError():
    return glesv2.glGetError()

def glGetFloatv(pname, params):
    return glesv2.glGetFloatv(pname, params)

def glGetFramebufferAttachmentParameteriv(target, attachment, pname, params):
    return glesv2.glGetFramebufferAttachmentParameteriv(target, attachment, pname, params)

def glGetIntegerv(pname, params):
    return glesv2.glGetIntegerv(pname, params)

def glGetProgramiv(program, pname, params):
    return glesv2.glGetProgramiv(program, pname, params)

def glGetProgramInfoLog(program, bufsize, length, infolog):
    return glesv2.glGetProgramInfoLog(program, bufsize, length, infolog)

def glGetRenderbufferParameteriv(target, pname, params):
    return glesv2.glGetRenderbufferParameteriv(target, pname, params)

def glGetShaderiv(shader, pname, params):
    return glesv2.glGetShaderiv(shader, pname, params)

def glGetShaderInfoLog(shader, bufsize, length, infolog):
    return glesv2.glGetShaderInfoLog(shader, bufsize, length, infolog)

def glGetShaderPrecisionFormat(shadertype, precisiontype, range, precision):
    return glesv2.glGetShaderPrecisionFormat(shadertype, precisiontype, range, precision)

def glGetShaderSource(shader, bufsize, length, source):
    return glesv2.glGetShaderSource(shader, bufsize, length, source)

def glGetString(name):
    return glesv2.glGetString(name)

def glGetTexParameterfv(target, pname, params):
    return glesv2.glGetTexParameterfv(target, pname, params)

def glGetTexParameteriv(target, pname, params):
    return glesv2.glGetTexParameteriv(target, pname, params)

def glGetUniformfv(program, location, params):
    return glesv2.glGetUniformfv(program, location, params)

def glGetUniformiv(program, location, params):
    return glesv2.glGetUniformiv(program, location, params)

def glGetUniformLocation(program, name):
    return glesv2.glGetUniformLocation(program, name)

def glGetVertexAttribfv(index, pname, params):
    return glesv2.glGetVertexAttribfv(index, pname, params)

def glGetVertexAttribiv(index, pname, params):
    return glesv2.glGetVertexAttribiv(index, pname, params)

def glGetVertexAttribPointerv(index, pname, pointer):
    return glesv2.glGetVertexAttribPointerv(index, pname, pointer)

def glHint(target, mode):
    return glesv2.glHint(target, mode)

def glIsBuffer(buffer):
    return glesv2.glIsBuffer(buffer)

def glIsEnabled(cap):
    return glesv2.glIsEnabled(cap)

def glIsFramebuffer(framebuffer):
    return glesv2.glIsFramebuffer(framebuffer)

def glIsProgram(program):
    return glesv2.glIsProgram(program)

def glIsRenderbuffer(renderbuffer):
    return glesv2.glIsRenderbuffer(renderbuffer)

def glIsShader(shader):
    return glesv2.glIsShader(shader)

def glIsTexture(texture):
    return glesv2.glIsTexture(texture)

def glLineWidth(width):
    return glesv2.glLineWidth(GLfloat(width))

def glLinkProgram(program):
    return glesv2.glLinkProgram(program)

def glPixelStorei(pname, param):
    return glesv2.glPixelStorei(pname, param)

def glPolygonOffset(factor, units):
    return glesv2.glPolygonOffset(GLfloat(factor), GLfloat(units))

def glReadPixels(x, y, width, height, format, type, pixels):
    return glesv2.glReadPixels(x, y, width, height, format, type, pixels)

def glReleaseShaderCompiler():
    return glesv2.glReleaseShaderCompiler()

def glRenderbufferStorage(target, internalformat, width, height):
    return glesv2.glRenderbufferStorage(target, internalformat, width, height)

def glSampleCoverage(value, invert):
    return glesv2.glSampleCoverage(GLclampf(value), invert)

def glScissor(x, y, width, height):
    return glesv2.glScissor(x, y, width, height)

def glShaderBinary(n, shaders, binaryformat, binary, length):
    return glesv2.glShaderBinary(n, shaders, binaryformat, binary, length)

def glShaderSource(shader, count, string, length):
    return glesv2.glShaderSource(shader, count, string, length)

def glStencilFunc(func, ref, mask):
    return glesv2.glStencilFunc(func, ref, mask)

def glStencilFuncSeparate(face, func, ref, mask):
    return glesv2.glStencilFuncSeparate(face, func, ref, mask)

def glStencilMask(mask):
    return glesv2.glStencilMask(mask)

def glStencilMaskSeparate(face, mask):
    return glesv2.glStencilMaskSeparate(face, mask)

def glStencilOp(fail, zfail, zpass):
    return glesv2.glStencilOp(fail, zfail, zpass)

def glStencilOpSeparate(face, fail, zfail, zpass):
    return glesv2.glStencilOpSeparate(face, fail, zfail, zpass)

def glTexImage2D(target, level, internalformat, width, height, border, format, type, pixels):
    return glesv2.glTexImage2D(target, level, internalformat, width, height, border, format, type, pixels)

def glTexParameterf(target, pname, param):
    return glesv2.glTexParameterf(target, pname, GLfloat(param))

def glTexParameterfv(target, pname, params):
    return glesv2.glTexParameterfv(target, pname, params)

def glTexParameteri(target, pname, param):
    return glesv2.glTexParameteri(target, pname, param)

def glTexParameteriv(target, pname, params):
    return glesv2.glTexParameteriv(target, pname, params)

def glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, pixels):
    return glesv2.glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, pixels)

def glUniform1f(location, x):
    return glesv2.glUniform1f(location, GLfloat(x))

def glUniform1fv(location, count, v):
    return glesv2.glUniform1fv(location, count, v)

def glUniform1i(location, x):
    return glesv2.glUniform1i(location, x)

def glUniform1iv(location, count, v):
    return glesv2.glUniform1iv(location, count, v)

def glUniform2f(location, x, y):
    return glesv2.glUniform2f(location, GLfloat(x), GLfloat(y))

def glUniform2fv(location, count, v):
    return glesv2.glUniform2fv(location, count, v)

def glUniform2i(location, x, y):
    return glesv2.glUniform2i(location, x, y)

def glUniform2iv(location, count, v):
    return glesv2.glUniform2iv(location, count, v)

def glUniform3f(location, x, y, z):
    return glesv2.glUniform3f(location, GLfloat(x), GLfloat(y), GLfloat(z))

def glUniform3fv(location, count, v):
    return glesv2.glUniform3fv(location, count, v)

def glUniform3i(location, x, y, z):
    return glesv2.glUniform3i(location, x, y, z)

def glUniform3iv(location, count, v):
    return glesv2.glUniform3iv(location, count, v)

def glUniform4f(location, x, y, z, w):
    return glesv2.glUniform4f(location, GLfloat(x), GLfloat(y), GLfloat(z), GLfloat(w))

def glUniform4fv(location, count, v):
    return glesv2.glUniform4fv(location, count, v)

def glUniform4i(location, x, y, z, w):
    return glesv2.glUniform4i(location, x, y, z, w)

def glUniform4iv(location, count, v):
    return glesv2.glUniform4iv(location, count, v)

def glUniformMatrix2fv(location, count, transpose, value):
    return glesv2.glUniformMatrix2fv(location, count, transpose, value)

def glUniformMatrix3fv(location, count, transpose, value):
    return glesv2.glUniformMatrix3fv(location, count, transpose, value)

def glUniformMatrix4fv(location, count, transpose, value):
    return glesv2.glUniformMatrix4fv(location, count, transpose, value)

def glUseProgram(program):
    return glesv2.glUseProgram(program)

def glValidateProgram(program):
    return glesv2.glValidateProgram(program)

def glVertexAttrib1f(indx, x):
    return glesv2.glVertexAttrib1f(indx, GLfloat(x))

def glVertexAttrib1fv(indx, values):
    return glesv2.glVertexAttrib1fv(indx, values)

def glVertexAttrib2f(indx, x, y):
    return glesv2.glVertexAttrib2f(indx, GLfloat(x), GLfloat(y))

def glVertexAttrib2fv(indx, values):
    return glesv2.glVertexAttrib2fv(indx, values)

def glVertexAttrib3f(indx, x, y, z):
    return glesv2.glVertexAttrib3f(indx, GLfloat(x), GLfloat(y), GLfloat(z))

def glVertexAttrib3fv(indx, values):
    return glesv2.glVertexAttrib3fv(indx, values)

def glVertexAttrib4f(indx, x, y, z, w):
    return glesv2.glVertexAttrib4f(indx, GLfloat(x), GLfloat(y), GLfloat(z), GLfloat(w))

def glVertexAttrib4fv(indx, values):
    return glesv2.glVertexAttrib4fv(indx, values)

def glVertexAttribPointer(indx, size, type, normalized, stride, ptr):
    return glesv2.glVertexAttribPointer(indx, size, type, normalized, stride, ptr)

def glViewport(x, y, width, height):
    return glesv2.glViewport(x, y, width, height)



