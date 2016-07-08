import math
import numbers


class Vec3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __mul__(self, f):
        if isinstance(f, Vec3):
            return Vec3(self.x * f.x, self.y * f.y, self.z * f.z)
        else:
            return Vec3(self.x * f, self.y * f, self.z * f)

    __rmul__ = __mul__

    def __neg__(self):
        return self * -1

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self.dot(self)

    def normalized(self):
        return self / self.length()

    def __div__(self, f):
        return Vec3(self.x / f, self.y / f, self.z / f)


class Matrix4x4(object):
    def __init__(self, m=None):
        if m:
            self.matrix = m
        else:
            self.identity()

    def __eq__(self, other):
        return ((isinstance(self, Matrix4x4), self.matrix) ==
                (isinstance(other, Matrix4x4), other.matrix))

    def identity(self):
        self.matrix = [1 if x == y else 0 for y in range(4) for x in range(4)]

    def __imul__(self, other):
        self.matrix = (self * other).matrix
        return self

    def __mul__(self, other):
        a = self.matrix
        b = other.matrix
        return Matrix4x4([
            a[0] * b[0] + a[1] * b[4] + a[2] * b[8] + a[3] * b[12],
            a[0] * b[1] + a[1] * b[5] + a[2] * b[9] + a[3] * b[13],
            a[0] * b[2] + a[1] * b[6] + a[2] * b[10] + a[3] * b[14],
            a[0] * b[3] + a[1] * b[7] + a[2] * b[11] + a[3] * b[15],

            a[4] * b[0] + a[5] * b[4] + a[6] * b[8] + a[7] * b[12],
            a[4] * b[1] + a[5] * b[5] + a[6] * b[9] + a[7] * b[13],
            a[4] * b[2] + a[5] * b[6] + a[6] * b[10] + a[7] * b[14],
            a[4] * b[3] + a[5] * b[7] + a[6] * b[11] + a[7] * b[15],

            a[8] * b[0] + a[9] * b[4] + a[10] * b[8] + a[11] * b[12],
            a[8] * b[1] + a[9] * b[5] + a[10] * b[9] + a[11] * b[13],
            a[8] * b[2] + a[9] * b[6] + a[10] * b[10] + a[11] * b[14],
            a[8] * b[3] + a[9] * b[7] + a[10] * b[11] + a[11] * b[15],

            a[12] * b[0] + a[13] * b[4] + a[14] * b[8] + a[15] * b[12],
            a[12] * b[1] + a[13] * b[5] + a[14] * b[9] + a[15] * b[13],
            a[12] * b[2] + a[13] * b[6] + a[14] * b[10] + a[15] * b[14],
            a[12] * b[3] + a[13] * b[7] + a[14] * b[11] + a[15] * b[15],
        ])

    __rmul__ = __mul__

    def map_vec3(self, v3):
        p = (v3.x, v3.y, v3.z, 1.)
        p = [sum(p[row] * self.matrix[i * 4 + row] for row in range(4)) for i, v in enumerate(p)]
        if p[3] == 0.0:
            return Vec3(p[0], p[1], p[2])
        else:
            return Vec3(p[0] / p[3], p[1] / p[3], p[2] / p[3])

    @staticmethod
    def translation(x, y, z):
        return Matrix4x4([
                1, 0, 0, x,
                0, 1, 0, y,
                0, 0, 1, z,
                0, 0, 0, 1,
        ])

    @classmethod
    def perspective(cls, fovy, aspect, zNear, zFar):
        f = math.cos(fovy / 2) / math.sin(fovy / 2)
        return cls([
                f / aspect, 0, 0, 0,
                0, f, 0, 0,
                0, 0, (zFar + zNear) / (zNear - zFar), (2 * zFar * zNear) / (zNear - zFar),
                0, 0, -1, 0,
        ])

    def lookAt(self, eye, center, up):
        f = (center - eye).normalized()
        UP = up.normalized()
        s = f.cross(UP).normalized()
        u = s.cross(f).normalized()
        self *= Matrix4x4([
                s.x, s.y, s.z, 0,
                u.x, u.y, u.z, 0,
                -f.x, -f.y, -f.z, 0,
                0, 0, 0, 1,
        ])
        self *= Matrix4x4.translation(-eye.x, -eye.y, -eye.z)
