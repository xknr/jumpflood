import math

class Mat4:

    # https://github.com/toji/gl-matrix/blob/master/src/mat4.js
    def mul(dst, a, b):
        a00 = a[0]
        a01 = a[1]
        a02 = a[2]
        a03 = a[3]
        a10 = a[4]
        a11 = a[5]
        a12 = a[6]
        a13 = a[7]
        a20 = a[8]
        a21 = a[9]
        a22 = a[10]
        a23 = a[11]
        a30 = a[12]
        a31 = a[13]
        a32 = a[14]
        a33 = a[15]

        # Cache only the current line of the second matrix
        b0 = b[0]
        b1 = b[1]
        b2 = b[2]
        b3 = b[3]
        dst[0] = b0 * a00 + b1 * a10 + b2 * a20 + b3 * a30
        dst[1] = b0 * a01 + b1 * a11 + b2 * a21 + b3 * a31
        dst[2] = b0 * a02 + b1 * a12 + b2 * a22 + b3 * a32
        dst[3] = b0 * a03 + b1 * a13 + b2 * a23 + b3 * a33

        b0 = b[4]
        b1 = b[5]
        b2 = b[6]
        b3 = b[7]
        dst[4] = b0 * a00 + b1 * a10 + b2 * a20 + b3 * a30
        dst[5] = b0 * a01 + b1 * a11 + b2 * a21 + b3 * a31
        dst[6] = b0 * a02 + b1 * a12 + b2 * a22 + b3 * a32
        dst[7] = b0 * a03 + b1 * a13 + b2 * a23 + b3 * a33

        b0 = b[8]
        b1 = b[9]
        b2 = b[10]
        b3 = b[11]
        dst[8] = b0 * a00 + b1 * a10 + b2 * a20 + b3 * a30
        dst[9] = b0 * a01 + b1 * a11 + b2 * a21 + b3 * a31
        dst[10] = b0 * a02 + b1 * a12 + b2 * a22 + b3 * a32
        dst[11] = b0 * a03 + b1 * a13 + b2 * a23 + b3 * a33

        b0 = b[12]
        b1 = b[13]
        b2 = b[14]
        b3 = b[15]
        dst[12] = b0 * a00 + b1 * a10 + b2 * a20 + b3 * a30
        dst[13] = b0 * a01 + b1 * a11 + b2 * a21 + b3 * a31
        dst[14] = b0 * a02 + b1 * a12 + b2 * a22 + b3 * a32
        dst[15] = b0 * a03 + b1 * a13 + b2 * a23 + b3 * a33
        

    def scale(m, sx, sy, sz):
        m[0] = sx
        m[1] = 0.0
        m[2] = 0.0
        m[3] = 0.0

        m[4] = 0.0
        m[5] = sy
        m[6] = 0.0
        m[7] = 0.0
        
        m[8] = 0.0
        m[9] = 0.0
        m[10] = sz
        m[11] = 0.0

        m[12] = 0.0
        m[13] = 0.0
        m[14] = 0.0
        m[15] = 1.0

    def identity(m):
        m[0] = 1.0
        m[1] = 0.0
        m[2] = 0.0
        m[3] = 0.0

        m[4] = 0.0
        m[5] = 1.0
        m[6] = 0.0
        m[7] = 0.0
        
        m[8] = 0.0
        m[9] = 0.0
        m[10] = 1.0
        m[11] = 0.0

        m[12] = 0.0
        m[13] = 0.0
        m[14] = 0.0
        m[15] = 1.0

    """
    def rotate(m, angleInDegrees, vx, vy, vz):
        a = angleInDegrees * 180 / math.pi
        c = math.cos(a)
        s = math.sin(a)

        d = math.sqrt(vx * vx + vy * vy + vz * vz)
        if math.abs(d) >= 1e-6:
            rd = 1 / d
            vx *= rd
            vy *= rd
            vz *= rd

        tempx = (1.0 - c) * vx
        tempy = (1.0 - c) * vy
        tempz = (1.0 - c) * vz

        m[0][0] = c + tempx * vx
        m[0][1] = 0 + tempx * vy + s * vz
        m[0][2] = 0 + tempx * vz - s * vy

        m[1][0] = 0 + tempy * vx - s * vz
        m[1][1] = c + tempy * vy
        m[1][2] = 0 + tempy * vz + s * vx

        m[2][0] = 0 + tempz * vx + s * vy
        m[2][1] = 0 + tempz * vy - s * vx
        m[2][2] = c + tempz * vz        
    """
    
    EPSILON = 0.000001

    def rotate(dst, rad, axis):
        x = axis[0]
        y = axis[1]
        z = axis[2]
        len = math.sqrt(x * x + y * y + z * z)
        #let s, c, t

        if len < Mat4.EPSILON:
            return
        

        len = 1 / len
        x *= len
        y *= len
        z *= len

        s = math.sin(rad)
        c = math.cos(rad)
        t = 1.0 - c

        # Perform rotation-specific matrix multiplication
        dst[0] = x * x * t + c
        dst[1] = y * x * t + z * s
        dst[2] = z * x * t - y * s
        dst[3] = 0
        
        dst[4] = x * y * t - z * s
        dst[5] = y * y * t + c
        dst[6] = z * y * t + x * s
        dst[7] = 0

        dst[8] = x * z * t + y * s
        dst[9] = y * z * t - x * s
        dst[10] = z * z * t + c
        dst[11] = 0

        dst[12] = 0
        dst[13] = 0
        dst[14] = 0
        dst[15] = 1
    


    def translate(m, x, y, z):
        m[0] = 1.0
        m[1] = 0.0
        m[2] = 0.0
        m[3] = 0.0

        m[4] = 0.0
        m[5] = 1.0
        m[6] = 0.0
        m[7] = 0.0
        
        m[8] = 0.0
        m[9] = 0.0
        m[10] = 1.0
        m[11] = 0.0

        m[12] = x
        m[13] = y
        m[14] = z
        m[15] = 1.0

    def ortho(m, left, right, bottom, top, nearval, farval):
        x = 2.0 / (right-left)
        y = 2.0 / (top-bottom)
        z = -2.0 / (farval-nearval)
        tx = -(right+left) / (right-left)
        ty = -(top+bottom) / (top-bottom)
        tz = -(farval+nearval) / (farval-nearval)

        # #define M(row,col)  m[col*4+row]
        m[0+4*0] = x
        m[0+4*1] = 0.0
        m[0+4*2] = 0.0
        m[0+4*3] = tx
        m[1+4*0] = 0.0
        m[1+4*1] = y
        m[1+4*2] = 0.0
        m[1+4*3] = ty
        m[2+4*0] = 0.0
        m[2+4*1] = 0.0
        m[2+4*2] = z
        m[2+4*3] = tz
        m[3+4*0] = 0.0
        m[3+4*1] = 0.0
        m[3+4*2] = 0.0
        m[3+4*3] = 1.0
