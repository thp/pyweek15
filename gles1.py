
# Automatically generated from gl.h
# Generator: header2py.py by Thomas Perl <thp.io/about>

from ctypes import *

glesv1 = cdll.LoadLibrary('libGLES_CM.so')






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
# ignored typedef: GLvoid
GLfixed = c_int
GLclampx = c_int

GLintptr = c_int
GLsizeiptr = c_int


# ***********************************************************

# OpenGL ES core versions
GL_VERSION_ES_CM_1_0 = 1
GL_VERSION_ES_CL_1_0 = 1
GL_VERSION_ES_CM_1_1 = 1
GL_VERSION_ES_CL_1_1 = 1

# ClearBufferMask
GL_DEPTH_BUFFER_BIT = 0x00000100
GL_STENCIL_BUFFER_BIT = 0x00000400
GL_COLOR_BUFFER_BIT = 0x00004000

# Boolean
GL_FALSE = 0
GL_TRUE = 1

# BeginMode
GL_POINTS = 0x0000
GL_LINES = 0x0001
GL_LINE_LOOP = 0x0002
GL_LINE_STRIP = 0x0003
GL_TRIANGLES = 0x0004
GL_TRIANGLE_STRIP = 0x0005
GL_TRIANGLE_FAN = 0x0006

# AlphaFunction
GL_NEVER = 0x0200
GL_LESS = 0x0201
GL_EQUAL = 0x0202
GL_LEQUAL = 0x0203
GL_GREATER = 0x0204
GL_NOTEQUAL = 0x0205
GL_GEQUAL = 0x0206
GL_ALWAYS = 0x0207

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

# ClipPlaneName
GL_CLIP_PLANE0 = 0x3000
GL_CLIP_PLANE1 = 0x3001
GL_CLIP_PLANE2 = 0x3002
GL_CLIP_PLANE3 = 0x3003
GL_CLIP_PLANE4 = 0x3004
GL_CLIP_PLANE5 = 0x3005

# ColorMaterialFace
# GL_FRONT_AND_BACK

# ColorMaterialParameter
# GL_AMBIENT_AND_DIFFUSE

# ColorPointerType
# GL_UNSIGNED_BYTE
# GL_FLOAT
# GL_FIXED

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
GL_FOG = 0x0B60
GL_LIGHTING = 0x0B50
GL_TEXTURE_2D = 0x0DE1
GL_CULL_FACE = 0x0B44
GL_ALPHA_TEST = 0x0BC0
GL_BLEND = 0x0BE2
GL_COLOR_LOGIC_OP = 0x0BF2
GL_DITHER = 0x0BD0
GL_STENCIL_TEST = 0x0B90
GL_DEPTH_TEST = 0x0B71
# GL_LIGHT0
# GL_LIGHT1
# GL_LIGHT2
# GL_LIGHT3
# GL_LIGHT4
# GL_LIGHT5
# GL_LIGHT6
# GL_LIGHT7
GL_POINT_SMOOTH = 0x0B10
GL_LINE_SMOOTH = 0x0B20
GL_SCISSOR_TEST = 0x0C11
GL_COLOR_MATERIAL = 0x0B57
GL_NORMALIZE = 0x0BA1
GL_RESCALE_NORMAL = 0x803A
GL_POLYGON_OFFSET_FILL = 0x8037
GL_VERTEX_ARRAY = 0x8074
GL_NORMAL_ARRAY = 0x8075
GL_COLOR_ARRAY = 0x8076
GL_TEXTURE_COORD_ARRAY = 0x8078
GL_MULTISAMPLE = 0x809D
GL_SAMPLE_ALPHA_TO_COVERAGE = 0x809E
GL_SAMPLE_ALPHA_TO_ONE = 0x809F
GL_SAMPLE_COVERAGE = 0x80A0

# ErrorCode
GL_NO_ERROR = 0
GL_INVALID_ENUM = 0x0500
GL_INVALID_VALUE = 0x0501
GL_INVALID_OPERATION = 0x0502
GL_STACK_OVERFLOW = 0x0503
GL_STACK_UNDERFLOW = 0x0504
GL_OUT_OF_MEMORY = 0x0505

# FogMode
# GL_LINEAR
GL_EXP = 0x0800
GL_EXP2 = 0x0801

# FogParameter
GL_FOG_DENSITY = 0x0B62
GL_FOG_START = 0x0B63
GL_FOG_END = 0x0B64
GL_FOG_MODE = 0x0B65
GL_FOG_COLOR = 0x0B66

# FrontFaceDirection
GL_CW = 0x0900
GL_CCW = 0x0901

# GetPName
GL_CURRENT_COLOR = 0x0B00
GL_CURRENT_NORMAL = 0x0B02
GL_CURRENT_TEXTURE_COORDS = 0x0B03
GL_POINT_SIZE = 0x0B11
GL_POINT_SIZE_MIN = 0x8126
GL_POINT_SIZE_MAX = 0x8127
GL_POINT_FADE_THRESHOLD_SIZE = 0x8128
GL_POINT_DISTANCE_ATTENUATION = 0x8129
GL_SMOOTH_POINT_SIZE_RANGE = 0x0B12
GL_LINE_WIDTH = 0x0B21
GL_SMOOTH_LINE_WIDTH_RANGE = 0x0B22
GL_ALIASED_POINT_SIZE_RANGE = 0x846D
GL_ALIASED_LINE_WIDTH_RANGE = 0x846E
GL_CULL_FACE_MODE = 0x0B45
GL_FRONT_FACE = 0x0B46
GL_SHADE_MODEL = 0x0B54
GL_DEPTH_RANGE = 0x0B70
GL_DEPTH_WRITEMASK = 0x0B72
GL_DEPTH_CLEAR_VALUE = 0x0B73
GL_DEPTH_FUNC = 0x0B74
GL_STENCIL_CLEAR_VALUE = 0x0B91
GL_STENCIL_FUNC = 0x0B92
GL_STENCIL_VALUE_MASK = 0x0B93
GL_STENCIL_FAIL = 0x0B94
GL_STENCIL_PASS_DEPTH_FAIL = 0x0B95
GL_STENCIL_PASS_DEPTH_PASS = 0x0B96
GL_STENCIL_REF = 0x0B97
GL_STENCIL_WRITEMASK = 0x0B98
GL_MATRIX_MODE = 0x0BA0
GL_VIEWPORT = 0x0BA2
GL_MODELVIEW_STACK_DEPTH = 0x0BA3
GL_PROJECTION_STACK_DEPTH = 0x0BA4
GL_TEXTURE_STACK_DEPTH = 0x0BA5
GL_MODELVIEW_MATRIX = 0x0BA6
GL_PROJECTION_MATRIX = 0x0BA7
GL_TEXTURE_MATRIX = 0x0BA8
GL_ALPHA_TEST_FUNC = 0x0BC1
GL_ALPHA_TEST_REF = 0x0BC2
GL_BLEND_DST = 0x0BE0
GL_BLEND_SRC = 0x0BE1
GL_LOGIC_OP_MODE = 0x0BF0
GL_SCISSOR_BOX = 0x0C10
GL_SCISSOR_TEST = 0x0C11
GL_COLOR_CLEAR_VALUE = 0x0C22
GL_COLOR_WRITEMASK = 0x0C23
GL_UNPACK_ALIGNMENT = 0x0CF5
GL_PACK_ALIGNMENT = 0x0D05
GL_MAX_LIGHTS = 0x0D31
GL_MAX_CLIP_PLANES = 0x0D32
GL_MAX_TEXTURE_SIZE = 0x0D33
GL_MAX_MODELVIEW_STACK_DEPTH = 0x0D36
GL_MAX_PROJECTION_STACK_DEPTH = 0x0D38
GL_MAX_TEXTURE_STACK_DEPTH = 0x0D39
GL_MAX_VIEWPORT_DIMS = 0x0D3A
GL_MAX_TEXTURE_UNITS = 0x84E2
GL_SUBPIXEL_BITS = 0x0D50
GL_RED_BITS = 0x0D52
GL_GREEN_BITS = 0x0D53
GL_BLUE_BITS = 0x0D54
GL_ALPHA_BITS = 0x0D55
GL_DEPTH_BITS = 0x0D56
GL_STENCIL_BITS = 0x0D57
GL_POLYGON_OFFSET_UNITS = 0x2A00
GL_POLYGON_OFFSET_FILL = 0x8037
GL_POLYGON_OFFSET_FACTOR = 0x8038
GL_TEXTURE_BINDING_2D = 0x8069
GL_VERTEX_ARRAY_SIZE = 0x807A
GL_VERTEX_ARRAY_TYPE = 0x807B
GL_VERTEX_ARRAY_STRIDE = 0x807C
GL_NORMAL_ARRAY_TYPE = 0x807E
GL_NORMAL_ARRAY_STRIDE = 0x807F
GL_COLOR_ARRAY_SIZE = 0x8081
GL_COLOR_ARRAY_TYPE = 0x8082
GL_COLOR_ARRAY_STRIDE = 0x8083
GL_TEXTURE_COORD_ARRAY_SIZE = 0x8088
GL_TEXTURE_COORD_ARRAY_TYPE = 0x8089
GL_TEXTURE_COORD_ARRAY_STRIDE = 0x808A
GL_VERTEX_ARRAY_POINTER = 0x808E
GL_NORMAL_ARRAY_POINTER = 0x808F
GL_COLOR_ARRAY_POINTER = 0x8090
GL_TEXTURE_COORD_ARRAY_POINTER = 0x8092
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
GL_PERSPECTIVE_CORRECTION_HINT = 0x0C50
GL_POINT_SMOOTH_HINT = 0x0C51
GL_LINE_SMOOTH_HINT = 0x0C52
GL_FOG_HINT = 0x0C54
GL_GENERATE_MIPMAP_HINT = 0x8192

# LightModelParameter
GL_LIGHT_MODEL_AMBIENT = 0x0B53
GL_LIGHT_MODEL_TWO_SIDE = 0x0B52

# LightParameter
GL_AMBIENT = 0x1200
GL_DIFFUSE = 0x1201
GL_SPECULAR = 0x1202
GL_POSITION = 0x1203
GL_SPOT_DIRECTION = 0x1204
GL_SPOT_EXPONENT = 0x1205
GL_SPOT_CUTOFF = 0x1206
GL_CONSTANT_ATTENUATION = 0x1207
GL_LINEAR_ATTENUATION = 0x1208
GL_QUADRATIC_ATTENUATION = 0x1209

# DataType
GL_BYTE = 0x1400
GL_UNSIGNED_BYTE = 0x1401
GL_SHORT = 0x1402
GL_UNSIGNED_SHORT = 0x1403
GL_FLOAT = 0x1406
GL_FIXED = 0x140C

# LogicOp
GL_CLEAR = 0x1500
GL_AND = 0x1501
GL_AND_REVERSE = 0x1502
GL_COPY = 0x1503
GL_AND_INVERTED = 0x1504
GL_NOOP = 0x1505
GL_XOR = 0x1506
GL_OR = 0x1507
GL_NOR = 0x1508
GL_EQUIV = 0x1509
GL_INVERT = 0x150A
GL_OR_REVERSE = 0x150B
GL_COPY_INVERTED = 0x150C
GL_OR_INVERTED = 0x150D
GL_NAND = 0x150E
GL_SET = 0x150F

# MaterialFace
# GL_FRONT_AND_BACK

# MaterialParameter
GL_EMISSION = 0x1600
GL_SHININESS = 0x1601
GL_AMBIENT_AND_DIFFUSE = 0x1602
# GL_AMBIENT
# GL_DIFFUSE
# GL_SPECULAR

# MatrixMode
GL_MODELVIEW = 0x1700
GL_PROJECTION = 0x1701
GL_TEXTURE = 0x1702

# NormalPointerType
# GL_BYTE
# GL_SHORT
# GL_FLOAT
# GL_FIXED

# PixelFormat
GL_ALPHA = 0x1906
GL_RGB = 0x1907
GL_RGBA = 0x1908
GL_LUMINANCE = 0x1909
GL_LUMINANCE_ALPHA = 0x190A

# PixelStoreParameter
GL_UNPACK_ALIGNMENT = 0x0CF5
GL_PACK_ALIGNMENT = 0x0D05

# PixelType
# GL_UNSIGNED_BYTE
GL_UNSIGNED_SHORT_4_4_4_4 = 0x8033
GL_UNSIGNED_SHORT_5_5_5_1 = 0x8034
GL_UNSIGNED_SHORT_5_6_5 = 0x8363

# ShadingModel
GL_FLAT = 0x1D00
GL_SMOOTH = 0x1D01

# StencilFunction
# GL_NEVER
# GL_LESS
# GL_EQUAL
# GL_LEQUAL
# GL_GREATER
# GL_NOTEQUAL
# GL_GEQUAL
# GL_ALWAYS

# StencilOp
# GL_ZERO
GL_KEEP = 0x1E00
GL_REPLACE = 0x1E01
GL_INCR = 0x1E02
GL_DECR = 0x1E03
# GL_INVERT

# StringName
GL_VENDOR = 0x1F00
GL_RENDERER = 0x1F01
GL_VERSION = 0x1F02
GL_EXTENSIONS = 0x1F03

# TexCoordPointerType
# GL_SHORT
# GL_FLOAT
# GL_FIXED
# GL_BYTE

# TextureEnvMode
GL_MODULATE = 0x2100
GL_DECAL = 0x2101
# GL_BLEND
GL_ADD = 0x0104
# GL_REPLACE

# TextureEnvParameter
GL_TEXTURE_ENV_MODE = 0x2200
GL_TEXTURE_ENV_COLOR = 0x2201

# TextureEnvTarget
GL_TEXTURE_ENV = 0x2300

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
GL_GENERATE_MIPMAP = 0x8191

# TextureTarget
# GL_TEXTURE_2D

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
GL_CLIENT_ACTIVE_TEXTURE = 0x84E1

# TextureWrapMode
GL_REPEAT = 0x2901
GL_CLAMP_TO_EDGE = 0x812F

# VertexPointerType
# GL_SHORT
# GL_FLOAT
# GL_FIXED
# GL_BYTE

# LightName
GL_LIGHT0 = 0x4000
GL_LIGHT1 = 0x4001
GL_LIGHT2 = 0x4002
GL_LIGHT3 = 0x4003
GL_LIGHT4 = 0x4004
GL_LIGHT5 = 0x4005
GL_LIGHT6 = 0x4006
GL_LIGHT7 = 0x4007

# Buffer Objects
GL_ARRAY_BUFFER = 0x8892
GL_ELEMENT_ARRAY_BUFFER = 0x8893

GL_ARRAY_BUFFER_BINDING = 0x8894
GL_ELEMENT_ARRAY_BUFFER_BINDING = 0x8895
GL_VERTEX_ARRAY_BUFFER_BINDING = 0x8896
GL_NORMAL_ARRAY_BUFFER_BINDING = 0x8897
GL_COLOR_ARRAY_BUFFER_BINDING = 0x8898
GL_TEXTURE_COORD_ARRAY_BUFFER_BINDING = 0x889A

GL_STATIC_DRAW = 0x88E4
GL_DYNAMIC_DRAW = 0x88E8

GL_BUFFER_SIZE = 0x8764
GL_BUFFER_USAGE = 0x8765

# Texture combine + dot3
GL_SUBTRACT = 0x84E7
GL_COMBINE = 0x8570
GL_COMBINE_RGB = 0x8571
GL_COMBINE_ALPHA = 0x8572
GL_RGB_SCALE = 0x8573
GL_ADD_SIGNED = 0x8574
GL_INTERPOLATE = 0x8575
GL_CONSTANT = 0x8576
GL_PRIMARY_COLOR = 0x8577
GL_PREVIOUS = 0x8578
GL_OPERAND0_RGB = 0x8590
GL_OPERAND1_RGB = 0x8591
GL_OPERAND2_RGB = 0x8592
GL_OPERAND0_ALPHA = 0x8598
GL_OPERAND1_ALPHA = 0x8599
GL_OPERAND2_ALPHA = 0x859A

GL_ALPHA_SCALE = 0x0D1C

GL_SRC0_RGB = 0x8580
GL_SRC1_RGB = 0x8581
GL_SRC2_RGB = 0x8582
GL_SRC0_ALPHA = 0x8588
GL_SRC1_ALPHA = 0x8589
GL_SRC2_ALPHA = 0x858A

GL_DOT3_RGB = 0x86AE
GL_DOT3_RGBA = 0x86AF


# OES_read_format
GL_IMPLEMENTATION_COLOR_READ_TYPE_OES = 0x8B9A
GL_IMPLEMENTATION_COLOR_READ_FORMAT_OES = 0x8B9B

# GL_OES_compressed_paletted_texture
GL_PALETTE4_RGB8_OES = 0x8B90
GL_PALETTE4_RGBA8_OES = 0x8B91
GL_PALETTE4_R5_G6_B5_OES = 0x8B92
GL_PALETTE4_RGBA4_OES = 0x8B93
GL_PALETTE4_RGB5_A1_OES = 0x8B94
GL_PALETTE8_RGB8_OES = 0x8B95
GL_PALETTE8_RGBA8_OES = 0x8B96
GL_PALETTE8_R5_G6_B5_OES = 0x8B97
GL_PALETTE8_RGBA4_OES = 0x8B98
GL_PALETTE8_RGB5_A1_OES = 0x8B99

# OES_point_size_array
GL_POINT_SIZE_ARRAY_OES = 0x8B9C
GL_POINT_SIZE_ARRAY_TYPE_OES = 0x898A
GL_POINT_SIZE_ARRAY_STRIDE_OES = 0x898B
GL_POINT_SIZE_ARRAY_POINTER_OES = 0x898C
GL_POINT_SIZE_ARRAY_BUFFER_BINDING_OES = 0x8B9F

# GL_OES_point_sprite
GL_POINT_SPRITE_OES = 0x8861
GL_COORD_REPLACE_OES = 0x8862

# ***********************************************************

# Available only in Common profile
def glAlphaFunc(func, ref):
    return glesv1.glAlphaFunc(func, GLclampf(ref))

def glClearColor(red, green, blue, alpha):
    return glesv1.glClearColor(GLclampf(red), GLclampf(green), GLclampf(blue), GLclampf(alpha))

def glClearDepthf(depth):
    return glesv1.glClearDepthf(GLclampf(depth))

def glClipPlanef(plane, *equation):
    return glesv1.glClipPlanef(plane, *equation)

def glColor4f(red, green, blue, alpha):
    return glesv1.glColor4f(GLfloat(red), GLfloat(green), GLfloat(blue), GLfloat(alpha))

glColor = glColor4f

def glDepthRangef(zNear, zFar):
    return glesv1.glDepthRangef(GLclampf(zNear), GLclampf(zFar))

def glFogf(pname, param):
    return glesv1.glFogf(pname, GLfloat(param))

def glFogfv(pname, *params):
    return glesv1.glFogfv(pname, *params)

def glFrustumf(left, right, bottom, top, zNear, zFar):
    return glesv1.glFrustumf(GLfloat(left), GLfloat(right), GLfloat(bottom), GLfloat(top), GLfloat(zNear), GLfloat(zFar))

def glGetClipPlanef(pname, eqn):
    return glesv1.glGetClipPlanef(pname, GLfloat(eqn))

def glGetFloatv(pname, *params):
    return glesv1.glGetFloatv(pname, GLfloat(*params))

def glGetLightfv(light, pname, *params):
    return glesv1.glGetLightfv(light, pname, GLfloat(*params))

def glGetMaterialfv(face, pname, *params):
    return glesv1.glGetMaterialfv(face, pname, GLfloat(*params))

def glGetTexEnvfv(env, pname, *params):
    return glesv1.glGetTexEnvfv(env, pname, GLfloat(*params))

def glGetTexParameterfv(target, pname, *params):
    return glesv1.glGetTexParameterfv(target, pname, GLfloat(*params))

def glLightModelf(pname, param):
    return glesv1.glLightModelf(pname, GLfloat(param))

def glLightModelfv(pname, *params):
    return glesv1.glLightModelfv(pname, *params)

def glLightf(light, pname, param):
    return glesv1.glLightf(light, pname, GLfloat(param))

def glLightfv(light, pname, *params):
    return glesv1.glLightfv(light, pname, *params)

def glLineWidth(width):
    return glesv1.glLineWidth(GLfloat(width))

def glLoadMatrixf(*m):
    return glesv1.glLoadMatrixf(*m)

def glMaterialf(face, pname, param):
    return glesv1.glMaterialf(face, pname, GLfloat(param))

def glMaterialfv(face, pname, *params):
    return glesv1.glMaterialfv(face, pname, *params)

def glMultMatrixf(*m):
    return glesv1.glMultMatrixf(*m)

def glMultiTexCoord4f(target, s, t, r, q):
    return glesv1.glMultiTexCoord4f(target, GLfloat(s), GLfloat(t), GLfloat(r), GLfloat(q))

def glNormal3f(nx, ny, nz):
    return glesv1.glNormal3f(GLfloat(nx), GLfloat(ny), GLfloat(nz))

def glOrthof(left, right, bottom, top, zNear, zFar):
    return glesv1.glOrthof(GLfloat(left), GLfloat(right), GLfloat(bottom), GLfloat(top), GLfloat(zNear), GLfloat(zFar))

glOrtho = glOrthof

def glPointParameterf(pname, param):
    return glesv1.glPointParameterf(pname, GLfloat(param))

def glPointParameterfv(pname, *params):
    return glesv1.glPointParameterfv(pname, *params)

def glPointSize(size):
    return glesv1.glPointSize(GLfloat(size))

def glPolygonOffset(factor, units):
    return glesv1.glPolygonOffset(GLfloat(factor), GLfloat(units))

def glRotatef(angle, x, y, z):
    return glesv1.glRotatef(GLfloat(angle), GLfloat(x), GLfloat(y), GLfloat(z))

def glScalef(x, y, z):
    return glesv1.glScalef(GLfloat(x), GLfloat(y), GLfloat(z))

def glTexEnvf(target, pname, param):
    return glesv1.glTexEnvf(target, pname, GLfloat(param))

def glTexEnvfv(target, pname, *params):
    return glesv1.glTexEnvfv(target, pname, *params)

def glTexParameterf(target, pname, param):
    return glesv1.glTexParameterf(target, pname, GLfloat(param))

def glTexParameterfv(target, pname, *params):
    return glesv1.glTexParameterfv(target, pname, *params)

def glTranslatef(x, y, z):
    return glesv1.glTranslatef(GLfloat(x), GLfloat(y), GLfloat(z))


# Available in both Common and Common-Lite profiles
def glActiveTexture(texture):
    return glesv1.glActiveTexture(texture)

def glAlphaFuncx(func, ref):
    return glesv1.glAlphaFuncx(func, ref)

def glBindBuffer(target, buffer):
    return glesv1.glBindBuffer(target, buffer)

def glBindTexture(target, texture):
    return glesv1.glBindTexture(target, texture)

def glBlendFunc(sfactor, dfactor):
    return glesv1.glBlendFunc(sfactor, dfactor)

def glBufferSubData(target, offset, size, *data):
    return glesv1.glBufferSubData(target, offset, size, *data)

def glClear(mask):
    return glesv1.glClear(mask)

def glClearColorx(red, green, blue, alpha):
    return glesv1.glClearColorx(red, green, blue, alpha)

def glClearDepthx(depth):
    return glesv1.glClearDepthx(depth)

def glClearStencil(s):
    return glesv1.glClearStencil(s)

def glClientActiveTexture(texture):
    return glesv1.glClientActiveTexture(texture)

def glClipPlanex(plane, *equation):
    return glesv1.glClipPlanex(plane, *equation)

def glColor4ub(red, green, blue, alpha):
    return glesv1.glColor4ub(red, green, blue, alpha)

def glColor4x(red, green, blue, alpha):
    return glesv1.glColor4x(red, green, blue, alpha)

def glColorMask(red, green, blue, alpha):
    return glesv1.glColorMask(red, green, blue, alpha)

def glColorPointer(size, type, stride, *pointer):
    return glesv1.glColorPointer(size, type, stride, *pointer)

def glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, *data):
    return glesv1.glCompressedTexImage2D(target, level, internalformat, width, height, border, imageSize, *data)

def glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, *data):
    return glesv1.glCompressedTexSubImage2D(target, level, xoffset, yoffset, width, height, format, imageSize, *data)

def glCopyTexImage2D(target, level, internalformat, x, y, width, height, border):
    return glesv1.glCopyTexImage2D(target, level, internalformat, x, y, width, height, border)

def glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height):
    return glesv1.glCopyTexSubImage2D(target, level, xoffset, yoffset, x, y, width, height)

def glCullFace(mode):
    return glesv1.glCullFace(mode)

def glDeleteBuffers(n, *buffers):
    return glesv1.glDeleteBuffers(n, *buffers)

def glDeleteTextures(n, *textures):
    return glesv1.glDeleteTextures(n, *textures)

def glDepthFunc(func):
    return glesv1.glDepthFunc(func)

def glDepthMask(flag):
    return glesv1.glDepthMask(flag)

def glDepthRangex(zNear, zFar):
    return glesv1.glDepthRangex(zNear, zFar)

def glDisable(cap):
    return glesv1.glDisable(cap)

def glDisableClientState(array):
    return glesv1.glDisableClientState(array)

def glDrawArrays(mode, first, count):
    return glesv1.glDrawArrays(mode, first, count)

def glDrawElements(mode, count, type, *indices):
    return glesv1.glDrawElements(mode, count, type, *indices)

def glEnable(cap):
    return glesv1.glEnable(cap)

def glEnableClientState(array):
    return glesv1.glEnableClientState(array)

def glFinish():
    return glesv1.glFinish()

def glFlush():
    return glesv1.glFlush()

def glFogx(pname, param):
    return glesv1.glFogx(pname, param)

def glFogxv(pname, *params):
    return glesv1.glFogxv(pname, *params)

def glFrontFace(mode):
    return glesv1.glFrontFace(mode)

def glFrustumx(left, right, bottom, top, zNear, zFar):
    return glesv1.glFrustumx(left, right, bottom, top, zNear, zFar)

def glGetBooleanv(pname, *params):
    return glesv1.glGetBooleanv(pname, *params)

def glGetBufferParameteriv(target, pname, *params):
    return glesv1.glGetBufferParameteriv(target, pname, *params)

def glGenBuffers(n, *buffers):
    return glesv1.glGenBuffers(n, *buffers)

def glGenTextures(n, *textures):
    return glesv1.glGenTextures(n, *textures)

def glGetError():
    return glesv1.glGetError()

def glGetFixedv(pname, *params):
    return glesv1.glGetFixedv(pname, *params)

def glGetIntegerv(pname, *params):
    return glesv1.glGetIntegerv(pname, *params)

def glGetLightxv(light, pname, *params):
    return glesv1.glGetLightxv(light, pname, *params)

def glGetMaterialxv(face, pname, *params):
    return glesv1.glGetMaterialxv(face, pname, *params)

def glGetPointerv(pname, **params):
    return glesv1.glGetPointerv(pname, **params)

def glGetString(name):
    return glesv1.glGetString(name)

def glGetTexEnviv(env, pname, *params):
    return glesv1.glGetTexEnviv(env, pname, *params)

def glGetTexEnvxv(env, pname, *params):
    return glesv1.glGetTexEnvxv(env, pname, *params)

def glGetTexParameteriv(target, pname, *params):
    return glesv1.glGetTexParameteriv(target, pname, *params)

def glGetTexParameterxv(target, pname, *params):
    return glesv1.glGetTexParameterxv(target, pname, *params)

def glHint(target, mode):
    return glesv1.glHint(target, mode)

def glIsBuffer(buffer):
    return glesv1.glIsBuffer(buffer)

def glIsEnabled(cap):
    return glesv1.glIsEnabled(cap)

def glIsTexture(texture):
    return glesv1.glIsTexture(texture)

def glLightModelx(pname, param):
    return glesv1.glLightModelx(pname, param)

def glLightModelxv(pname, *params):
    return glesv1.glLightModelxv(pname, *params)

def glLightx(light, pname, param):
    return glesv1.glLightx(light, pname, param)

def glLightxv(light, pname, *params):
    return glesv1.glLightxv(light, pname, *params)

def glLineWidthx(width):
    return glesv1.glLineWidthx(width)

def glLoadIdentity():
    return glesv1.glLoadIdentity()

def glLoadMatrixx(*m):
    return glesv1.glLoadMatrixx(*m)

def glLogicOp(opcode):
    return glesv1.glLogicOp(opcode)

def glMaterialx(face, pname, param):
    return glesv1.glMaterialx(face, pname, param)

def glMaterialxv(face, pname, *params):
    return glesv1.glMaterialxv(face, pname, *params)

def glMatrixMode(mode):
    return glesv1.glMatrixMode(mode)

def glMultMatrixx(*m):
    return glesv1.glMultMatrixx(*m)

def glMultiTexCoord4x(target, s, t, r, q):
    return glesv1.glMultiTexCoord4x(target, s, t, r, q)

def glNormal3x(nx, ny, nz):
    return glesv1.glNormal3x(nx, ny, nz)

def glNormalPointer(type, stride, *pointer):
    return glesv1.glNormalPointer(type, stride, *pointer)

def glOrthox(left, right, bottom, top, zNear, zFar):
    return glesv1.glOrthox(left, right, bottom, top, zNear, zFar)

def glPixelStorei(pname, param):
    return glesv1.glPixelStorei(pname, param)

def glPointParameterx(pname, param):
    return glesv1.glPointParameterx(pname, param)

def glPointParameterxv(pname, *params):
    return glesv1.glPointParameterxv(pname, *params)

def glPointSizex(size):
    return glesv1.glPointSizex(size)

def glPolygonOffsetx(factor, units):
    return glesv1.glPolygonOffsetx(factor, units)

def glPopMatrix():
    return glesv1.glPopMatrix()

def glPushMatrix():
    return glesv1.glPushMatrix()

def glReadPixels(x, y, width, height, format, type, *pixels):
    return glesv1.glReadPixels(x, y, width, height, format, type, *pixels)

def glRotatex(angle, x, y, z):
    return glesv1.glRotatex(angle, x, y, z)

def glSampleCoverage(value, invert):
    return glesv1.glSampleCoverage(GLclampf(value), invert)

def glSampleCoveragex(value, invert):
    return glesv1.glSampleCoveragex(value, invert)

def glScalex(x, y, z):
    return glesv1.glScalex(x, y, z)

def glScissor(x, y, width, height):
    return glesv1.glScissor(x, y, width, height)

def glShadeModel(mode):
    return glesv1.glShadeModel(mode)

def glStencilFunc(func, ref, mask):
    return glesv1.glStencilFunc(func, ref, mask)

def glStencilMask(mask):
    return glesv1.glStencilMask(mask)

def glStencilOp(fail, zfail, zpass):
    return glesv1.glStencilOp(fail, zfail, zpass)

def glTexCoordPointer(size, type, stride, *pointer):
    return glesv1.glTexCoordPointer(size, type, stride, *pointer)

def glTexEnvi(target, pname, param):
    return glesv1.glTexEnvi(target, pname, param)

def glTexEnvx(target, pname, param):
    return glesv1.glTexEnvx(target, pname, param)

def glTexEnviv(target, pname, *params):
    return glesv1.glTexEnviv(target, pname, *params)

def glTexEnvxv(target, pname, *params):
    return glesv1.glTexEnvxv(target, pname, *params)

def glTexImage2D(target, level, internalformat, width, height, border, format, type, *pixels):
    return glesv1.glTexImage2D(target, level, internalformat, width, height, border, format, type, *pixels)

def glTexParameteri(target, pname, param):
    return glesv1.glTexParameteri(target, pname, param)

glTexParameter = glTexParameteri

def glTexParameterx(target, pname, param):
    return glesv1.glTexParameterx(target, pname, param)

def glTexParameteriv(target, pname, *params):
    return glesv1.glTexParameteriv(target, pname, *params)

def glTexParameterxv(target, pname, *params):
    return glesv1.glTexParameterxv(target, pname, *params)

def glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, *pixels):
    return glesv1.glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, *pixels)

def glTranslatex(x, y, z):
    return glesv1.glTranslatex(x, y, z)

def glVertexPointer(size, type, stride, *pointer):
    return glesv1.glVertexPointer(size, type, stride, *pointer)

def glViewport(x, y, width, height):
    return glesv1.glViewport(x, y, width, height)



# GL_OES_read_format
GL_OES_read_format = 1

# GL_OES_compressed_paletted_texture
GL_OES_compressed_paletted_texture = 1

# GL_OES_point_size_array
GL_OES_point_size_array = 1
def glPointSizePointerOES(type, stride, *pointer):
    return glesv1.glPointSizePointerOES(type, stride, *pointer)


# GL_OES_point_sprite
GL_OES_point_sprite = 1



