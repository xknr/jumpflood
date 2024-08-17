import numpy as np
from fw.ogl.Ogl import Program, RenderTarget
from OpenGL.GL import * # pip install PyOpenGL
import os

class Jfa():

    INVALID_COLOR = [1.0, 1.0, 1.0, 1.0]

    def __init__(self, fw) -> None:
        self.fw = fw
   
    def create(self):

        self.createSurfaces()

        self.programJfa = Program()
        self.programJfa.createFromFile("jfa/jfa.vert", "jfa/jfa.frag")
        self.fw.setProgram(self.programJfa)
        self.fw.setUniform1i("uTexture", 0)
        self.fw.setUniform2f("screenSize", self.fw.windowSize[0], self.fw.windowSize[1])

        w, h = self.fw.windowSize

        quadPosData = np.array([
            [0.0, 0.0],
            [w, 0.0],
            [0.0, h],
            [w, h]
        ], dtype=np.float32)

        quadUvData = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0]
        ], dtype=np.float32)

        self.quadPos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadPos)
        glBufferData(GL_ARRAY_BUFFER, quadPosData.nbytes, quadPosData, GL_STATIC_DRAW)

        self.quadUv = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadUv)
        glBufferData(GL_ARRAY_BUFFER, quadUvData.nbytes, quadUvData, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def release(self):
        if self.surface:
            for i in range(len(self.surface)):
                if self.surface[i]:
                    self.surface[i].release()
                    self.surface[i] = None
            self.surface = None

        if self.programJfa:
            self.programJfa.release()
            self.programJfa = None

        if self.quadPos:
            glDeleteBuffers(1, [self.quadPos])
            self.quadPos = None
        
        if self.quadUv:
            glDeleteBuffers(1, [self.quadUv])
            self.quadUv = None
        

    def createSurfaces(self):
        w, h = self.fw.windowSize
        self.surface = [None] * 2

        for i in range(len(self.surface)):
            surf = RenderTarget(w, h)
            surf.create()
            glBindTexture(GL_TEXTURE_2D, surf.colorTexture)
            glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, Jfa.INVALID_COLOR)
            glBindTexture(GL_TEXTURE_2D, 0) # Fbo texture must not be left bound.
            self.surface[i] = surf


    def process(self, method, bShowDistance):
        self.encodeMap(self.surface[1], self.surface[0])
        self.doFloodPasses(method, bShowDistance)


    def encodeMap(self, src, dst):
        self.fw.setProgram(self.programJfa)
        self.fw.setUniform1f("chooseMain", 0.0)
        self.fw.set2D().programUpdateMatrices() 
        self.fw.setRenderTarget(dst)

        aPos = self.fw.currentProgram.atts["aPos"].loc
        aUv = self.fw.currentProgram.atts["aUv"].loc
        glEnableVertexAttribArray(aPos)
        glEnableVertexAttribArray(aUv)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadPos)
        glVertexAttribPointer(aPos, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadUv)
        glVertexAttribPointer(aUv, 2, GL_FLOAT, GL_FALSE, 0, None)

        glBindTexture(GL_TEXTURE_2D, src.colorTexture)       
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0) # Fbo texture must not be left bound.
        glDisableVertexAttribArray(aPos)
        glDisableVertexAttribArray(aUv)
        self.fw.setRenderTarget(None)

    def doFloodPasses(self, method, bShowDistance):
        self.fw.setProgram(self.programJfa)
        aPos = self.fw.currentProgram.atts["aPos"].loc
        aUv = self.fw.currentProgram.atts["aUv"].loc
        glEnableVertexAttribArray(aPos)
        glEnableVertexAttribArray(aUv)

        self.fw.setUniform1f("chooseMain", 1.0)
        self.fw.set2D().programUpdateMatrices() 
        
        steps = method(self.fw.windowSize[0], self.fw.windowSize[1])

        for i in range(len(steps)):
            step = steps[i]

            if bShowDistance:
                isLast = i == len(steps) - 1
                bDisplayDistance = isLast
            else:
                # This renders voronoi cells.
                bDisplayDistance = False

            self.doOneFloodPass(step, self.surface[0], self.surface[1], bDisplayDistance)
            self.surface[0], self.surface[1] = self.surface[1], self.surface[0] # Swap.
        glDisableVertexAttribArray(aPos)
        glDisableVertexAttribArray(aUv)


    def doOneFloodPass(self, step, src, dst, bDisplayDistance):
        self.fw.setUniform1i("bDisplayDistance", 1 if bDisplayDistance else 0);
        
        self.fw.setRenderTarget(dst)

        aPos = self.fw.currentProgram.atts["aPos"].loc
        aUv = self.fw.currentProgram.atts["aUv"].loc
        
        glBindBuffer(GL_ARRAY_BUFFER, self.quadPos)
        glVertexAttribPointer(aPos, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadUv)
        glVertexAttribPointer(aUv, 2, GL_FLOAT, GL_FALSE, 0, None)

        glBindTexture(GL_TEXTURE_2D, src.colorTexture)       
        self.fw.setUniform1i("step", step);
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0) # Fbo texture must not be left bound.
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        self.fw.setRenderTarget(None)

