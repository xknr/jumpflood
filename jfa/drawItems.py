import numpy as np
import random
import math
from collections import namedtuple
import pygame
import os
from OpenGL.GL import * # pip install PyOpenGL
from fw.mat4 import Mat4

class Particle():
    def __init__(self, x, y, vx, vy) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

class DrawItems():
    def __init__(self, windowSize) -> None:
        self.windowSize = windowSize

    def loadTextures(self):

        # Get the image's width, height, and pixel data

        textureDir = "jfa/data"
        filenames = ["0.png", "1.png","2.png","3.png"]
        self.textures = [None] * len(filenames)

        Texture = namedtuple('Texture', ['tex', 'width', 'height'])

        for i in range(len(self.textures)):
            image = pygame.image.load(os.path.join(textureDir, filenames[i]))
            width, height = image.get_size()
            imageData = pygame.image.tostring(image, "RGBA", 1)
            tex = glGenTextures(1)
            texture = Texture(tex, width, height)
            self.textures[i] = texture
            glBindTexture(GL_TEXTURE_2D, tex)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)  
            glBindTexture(GL_TEXTURE_2D, 0)

    def create(self, fw, programBlit):

        self.fw = fw
        self.programBlit = programBlit

        self.loadTextures()

        self.drawQuadPosData = np.array([
            [0.0, 0.0],
            [100.0, 0.0],
            [0.0, 100.0],
            [100.0, 100.0]
        ], dtype=np.float32)

        self.drawQuadUvData = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0]
        ], dtype=np.float32)

        self.drawQuadPos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.drawQuadPos)
        glBufferData(GL_ARRAY_BUFFER, self.drawQuadPosData.nbytes, self.drawQuadPosData, GL_DYNAMIC_DRAW)

        self.drawQuadUv = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.drawQuadUv)
        glBufferData(GL_ARRAY_BUFFER, self.drawQuadUvData.nbytes, self.drawQuadUvData, GL_DYNAMIC_DRAW)





        self.drawPointPosData = np.array([
            [0.0, 0.0]
        ], dtype=np.float32)
        self.drawPointPos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.drawPointPos)
        glBufferData(GL_ARRAY_BUFFER, self.drawPointPosData.nbytes, self.drawPointPosData, GL_DYNAMIC_DRAW)

        self.drawLinePosData = np.array([
            [0.0, 0.0],
            [0.0, 0.0]
        ], dtype=np.float32)
        self.drawLinePos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.drawLinePos)
        glBufferData(GL_ARRAY_BUFFER, self.drawLinePosData.nbytes, self.drawLinePosData, GL_DYNAMIC_DRAW)






        random.seed(42)

        numParticles = 30
        particles = [None] * numParticles
        for i in range(len(particles)):            
            particles[i] = self.createRandomParticle()

        self.particles = particles

    def release(self):
        if self.drawLinePos:
            glDeleteBuffers(1, [self.drawLinePos])
            self.drawLinePos = None

        if self.drawPointPos:
            glDeleteBuffers(1, [self.drawPointPos])
            self.drawPointPos = None

        if self.drawQuadUv:
            glDeleteBuffers(1, [self.drawQuadUv])
            self.drawQuadUv = None

        if self.drawQuadPos:
            glDeleteBuffers(1, [self.drawQuadPos])
            self.drawQuadPos = None
            
        if self.textures:
            for i in range(len(self.textures)):
                if self.textures[i]:
                    glDeleteTextures(1, [self.textures[i].tex])
                    self.textures[i] = None
            self.textures = None

        print("TODO DrawItems release")

    def createRandomParticle(self):
        w, h = self.windowSize
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        velocity = random.uniform(1, 2) * 0.25
        dir = random.uniform(0, 2 * math.pi)
        vx = math.cos(dir) * velocity
        vy = math.sin(dir) * velocity
        return Particle(x, y, vx, vy)
    

    def drawPoints(self, beg, end):
        self.fw.setProgram(self.programBlit)
        aPos = self.fw.currentProgram.atts["aPos"].loc
        self.fw.setUniform1i("bUseTexture", 0)
        glEnableVertexAttribArray(aPos)
        self.fw.set2D().programUpdateMatrices() 

        glBindBuffer(GL_ARRAY_BUFFER, self.drawPointPos)
        glVertexAttribPointer(aPos, 2, GL_FLOAT, GL_FALSE, 0, None)

        for i in range(beg, end):
            p = self.particles[i]
            x, y = math.floor(p.x), math.floor(p.y)

            data = self.drawPointPosData
            data[0][0], data[0][1] = x, y
            glBufferSubData(GL_ARRAY_BUFFER, 0, self.drawPointPosData.nbytes, self.drawPointPosData)
            glDrawArrays(GL_POINTS, 0, 1)


        glDisableVertexAttribArray(aPos)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


    def drawLines(self, beg, end):

        self.fw.setProgram(self.programBlit)
        aPos = self.fw.currentProgram.atts["aPos"].loc
        self.fw.setUniform1i("bUseTexture", 0)
        glEnableVertexAttribArray(aPos)
        self.fw.set2D().programUpdateMatrices() 

        glBindBuffer(GL_ARRAY_BUFFER, self.drawLinePos)
        glVertexAttribPointer(aPos, 2, GL_FLOAT, GL_FALSE, 0, None)

        for i in range(beg, end, 2):
            p0, p1 = self.particles[i], self.particles[i + 1]

            x0, y0 = math.floor(p0.x), math.floor(p0.y)
            x1, y1 = math.floor(p1.x), math.floor(p1.y)

            # Make sure line length doesn't exceed a certain threshold.
            dx, dy = x1 - x0, y1 - y0
            length = math.sqrt(dx**2 + dy**2)
            maxLen = 150
            if length > maxLen:
                x1 = x0 + dx * maxLen / length
                y1 = y0 + dy * maxLen / length

            data = self.drawLinePosData
            data[0][0], data[0][1] = x0, y0
            data[1][0], data[1][1] = x1, y1
            glBufferSubData(GL_ARRAY_BUFFER, 0, self.drawLinePosData.nbytes, self.drawLinePosData)
            glDrawArrays(GL_LINES, 0, 2)

        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, aPos)

    def drawQuad(self, x, y, texture, angle, scale):        
        
        temp = np.zeros((16), dtype=np.float32)

        glBindTexture(GL_TEXTURE_2D, texture.tex);
        w, h = 180*texture.width/128, 180*texture.height/128

        Mat4.scale(self.fw.mvMat, scale, scale, scale)
        Mat4.rotate(temp, angle, [0, 0, 1])
        Mat4.mul(self.fw.mvMat, temp, self.fw.mvMat)
        Mat4.translate(temp, x, y, 0)
        Mat4.mul(self.fw.mvMat, temp, self.fw.mvMat)

        self.fw.programUpdateMatrices() 

        data = self.drawQuadPosData
        data[0][0], data[0][1] = -w/2, -w/2
        data[1][0], data[1][1] = +w/2, -h/2
        data[2][0], data[2][1] = -w/2, +w/2
        data[3][0], data[3][1] = +w/2, +h/2
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.drawQuadPosData.nbytes, self.drawQuadPosData)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)


    def drawQuads(self, beg, end, elapsed):

        self.fw.setProgram(self.programBlit)
        self.fw.setUniform1i("bUseTexture", 1)
        aPos = self.fw.currentProgram.atts["aPos"].loc
        aUv = self.fw.currentProgram.atts["aUv"].loc

        glEnableVertexAttribArray(aPos)
        glEnableVertexAttribArray(aUv)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        self.fw.set2D()

        glBindBuffer(GL_ARRAY_BUFFER, self.drawQuadUv)
        glVertexAttribPointer(aUv, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.drawQuadPos) # Keep this bound.
        glVertexAttribPointer(aPos, 2, GL_FLOAT, GL_FALSE, 0, None)

        for i in range(beg, end):
            p = self.particles[i]

            scale = 1 + 0.3 * math.cos(elapsed + i * 1.2345)
            angle = elapsed * 30 * math.pi / 180.0 # Angle is in radians.
            angle += 77 * i # Extra term for each particle.
            angle *= (i % 2) * 2 - 1 # Negative rotation for every other particle.

            self.drawQuad(p.x, p.y, self.textures[i], angle, scale)

        glBindTexture(GL_TEXTURE_2D, 0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)          
        glDisable(GL_BLEND)
        glDisableVertexAttribArray(aPos)
        glDisableVertexAttribArray(aUv)
        self.fw.setProgram(None)


    def draw(self, elapsed):

        # Half of particles used for lines, the other half for points.

        part0 = len(self.textures)
        remaining = len(self.particles) - part0
        part1 = (remaining // 2)
        part1 -= part1 % 2 # Ensure divisible by 2.
        part2 = remaining - part1

        self.drawQuads(0, part0, elapsed)
        self.drawLines(part0, part1)
        self.drawPoints(part1, len(self.particles))






    def updateParticles(self):

        w, h = self.windowSize

        for i in range(len(self.particles)):

            p = self.particles[i]

            # TODO use delta time

            # Add velocities.
            p.x += p.vx
            p.y += p.vy

            # Bounce from edges:

            if p.x < 0:         # If outside left boundary,
                p.x = 0         #   Bring to boundary.
                p.vx *= -1      #   Invert horizontal velocity.
            elif p.x > w - 1:   # If outside right boundary,
                p.x = w - 1     #   Bring to boundary.
                p.vx *= -1      #   Invert horizontal velocity.

            if p.y < 0:         # If outside bottom boundary,
                p.y = 0         #   Bring to boundary.
                p.vy *= -1      #   Invert vertical velocity.
            elif p.y > h - 1:   # If outside top boundary,
                p.y = h - 1     #   Bring to boundary.
                p.vy *= -1      #   Invert vertical velocity.





























