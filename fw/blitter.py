from fw.ogl.Ogl import Program, RenderTarget
from jfa.jfa import Jfa
import numpy as np

from OpenGL.GL import * # pip install PyOpenGL

class Blitter():
    def __init__(self, fw) -> None:
        self.fw = fw

    def create(self):
        self.programBlit = Program()
        self.programBlit.createFromFile("fw/blit.vert", "fw/blit.frag")
        self.fw.setProgram(self.programBlit)
        self.fw.setUniform1i("uTexture", 0)
        self.fw.setUniform1i("bUseTexture", 1)

        self.fw.setProgram(None)

        w, h = self.fw.windowSize
        
        self.blitPosData = np.zeros((4, 2), dtype=np.float32)
        self.blitUvData = np.zeros((4, 2), dtype=np.float32)

        self.blitPos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.blitPos)
        glBufferData(GL_ARRAY_BUFFER, self.blitPosData.nbytes, self.blitPosData, GL_DYNAMIC_DRAW)

        self.blitUv = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.blitUv)
        glBufferData(GL_ARRAY_BUFFER, self.blitUvData.nbytes, self.blitUvData, GL_DYNAMIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def release(self):        
        if self.programBlit:
            self.programBlit.release()
            self.programBlit = None

        if self.blitPos:
            glDeleteBuffers(1, [self.blitPos])
            self.blitPos = 0

        if self.blitUv:
            glDeleteBuffers(1, [self.blitUv])
            self.blitUv = 0

    def blitResult(self, tex):
        
        self.fw.setProgram(self.programBlit)

        aPos = self.fw.currentProgram.atts["aPos"].loc
        aUv = self.fw.currentProgram.atts["aUv"].loc
        glEnableVertexAttribArray(aPos)
        glEnableVertexAttribArray(aUv)

        self.fw.setUniform1i("bUseTexture", 1)
        glBindTexture(GL_TEXTURE_2D, tex)     

        self.fw.set2D().programUpdateMatrices() 

        w, h = self.fw.windowSize
        dx0, dy0, dx1, dy1 = 0, 0, w, h
        data = self.blitPosData
        data[0][0], data[0][1] = dx0, dy0
        data[1][0], data[1][1] = dx1, dy0
        data[2][0], data[2][1] = dx0, dy1
        data[3][0], data[3][1] = dx1, dy1

        sx0, sy0, sx1, sy1 = 0, 0, w, h
        data = self.blitUvData
        data[0][0], data[0][1] = sx0/w, sy0/h
        data[1][0], data[1][1] = sx1/w, sy0/h
        data[2][0], data[2][1] = sx0/w, sy1/h
        data[3][0], data[3][1] = sx1/w, sy1/h

        glBindBuffer(GL_ARRAY_BUFFER, self.blitPos)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.blitPosData.nbytes, self.blitPosData)
        glVertexAttribPointer(aPos, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.blitUv)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.blitUvData.nbytes, self.blitUvData)
        glVertexAttribPointer(aUv, 2, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0) # Fbo texture must not be left bound.

        glDisableVertexAttribArray(aPos)
        glDisableVertexAttribArray(aUv)

        glBindBuffer(GL_ARRAY_BUFFER, 0)


