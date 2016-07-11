from core import cos, sin, sqrt

class Vec3(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __sub__(self, o):
        return Vec3(self.x - o.x, self.y - o.y, self.z - o.z)

    def cross(self, o):
        return Vec3(self.y * o.z - self.z * o.y, self.z * o.x - self.x * o.z, self.x * o.y - self.y * o.x)

    def normalized(self):
        f = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        return Vec3(self.x / f, self.y / f, self.z / f)

class Matrix4x4(object):
    def __init__(self, m):
        self.matrix = m

    def __mul__(self, other):
        a, b = self.matrix, other.matrix
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

    def map_vec3(self, v3):
        p = (v3.x, v3.y, v3.z, 1.)
        p = [sum(p[row] * self.matrix[i * 4 + row] for row in range(4)) for i, v in enumerate(p)]
        return Vec3(p[0] / p[3], p[1] / p[3], p[2] / p[3])

    @classmethod
    def perspective(cls, fovy, aspect, zNear, zFar):
        f = cos(fovy / 2) / sin(fovy / 2)
        return cls([
                f / aspect, 0, 0, 0,
                0, f, 0, 0,
                0, 0, (zFar + zNear) / (zNear - zFar), (2 * zFar * zNear) / (zNear - zFar),
                0, 0, -1, 0,
        ])

    @classmethod
    def lookAt(cls, eye, center, up):
        f = (center - eye).normalized()
        UP = up.normalized()
        s = f.cross(UP).normalized()
        u = s.cross(f).normalized()
        return cls([
                s.x, s.y, s.z, 0,
                u.x, u.y, u.z, 0,
                -f.x, -f.y, -f.z, 0,
                0, 0, 0, 1,
        ]) * cls([
                1, 0, 0, -eye.x,
                0, 1, 0, -eye.y,
                0, 0, 1, -eye.z,
                0, 0, 0, 1,
        ])
