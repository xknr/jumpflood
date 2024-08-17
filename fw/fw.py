import numpy as np
from OpenGL.GL import *
#from OpenGL.GLUT import *

import pygame
from pygame.locals import DOUBLEBUF, OPENGL

from fw.mat4 import Mat4

from abc import ABC, abstractmethod

class App(ABC):

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def onFrame(self):
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def keyDown(self, key):
        pass

    @abstractmethod
    def keyUp(self, key):
        pass


class Fw():

    def __init__(self, windowSize) -> None:
        self.windowSize = windowSize
        self.projMat = np.zeros((16), dtype=np.float32)
        self.mvMat = np.zeros((16), dtype=np.float32)
        self.currentProgram = None
        self.renderSize = self.windowSize
        self.currentRenderTarget = None
        self.pressed_keys = set()  # Keep track of pressed keys
        self.app = None

    def onFrame(self):
        self.checkGlError("frame begin", True)
        self.app.onFrame()
        self.checkGlError("frame end", True)

    def onInit(self, app):
        
        if not app:
            raise Exception("app == None")
        
        if self.app:
            raise Exception("app was already set or init was called")
        
        glViewport(0, 0, self.windowSize[0], self.windowSize[1])

        self.app = app
        self.app.create()

    def release(self):
        if self.app:
            self.app.release()
            self.app = None

    def onKeyDown(self, key):
        self.pressed_keys.add(key)  # Add the pressed key to the set
        self.app.keyDown(key)


    def onKeyUp(self, key):
        self.pressed_keys.discard(key)  # Remove the released key from the set
        self.app.keyUp(key)


    def isKeyDown(self, key):
        return key in self.pressed_keys

    def setUniform1i(self, name, value):
        if name in self.currentProgram.unis:
            glUniform1i(self.currentProgram.unis[name].loc, value)
        
    def setUniform1f(self, name, value):
        if name in self.currentProgram.unis:
            glUniform1f(self.currentProgram.unis[name].loc, value)
        
    def setUniform2f(self, name, x, y):
        if name in self.currentProgram.unis:
            glUniform2f(self.currentProgram.unis[name].loc, x, y)

    def setProgram(self, program):
        self.currentProgram = program
        if self.currentProgram != None:
            glUseProgram(self.currentProgram.program)
        else:
            glUseProgram(0)

    def programUpdateMatrices(self):
        self.currentProgram.updateMatrices(self)


    def checkGlError(self, text, doThrow):
        err = glGetError()
        if err != GL_NO_ERROR:
            msg = f"Opengl error: {err}, {text}"
            print(msg)
            if doThrow:            
                raise Exception(msg)


    def clearScreen(self, r, g, b, a, depthValue, stencilValue, doColor, doDepth, doStencil):
        if not (doColor or doDepth or doStencil):
            return

        if doColor:
            glClearColor(r, g, b, a)

        if doDepth:
            glClearDepth(depthValue)

        if doStencil:
            glClearStencil(stencilValue)

        mask = 0

        if doColor:
            mask |= GL_COLOR_BUFFER_BIT

        if doDepth:
            mask |= GL_DEPTH_BUFFER_BIT

        if doStencil:
            mask |= GL_STENCIL_BUFFER_BIT

        glClear(mask)

    def setRenderTarget(self, renderTarget):
        self.currentRenderTarget = renderTarget

        if self.currentRenderTarget == None:
            self.renderSize = self.windowSize
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
        else:
            self.renderSize = self.currentRenderTarget.width, self.currentRenderTarget.height
            glBindFramebuffer(GL_FRAMEBUFFER, self.currentRenderTarget.fbo)

        glViewport(0, 0, self.renderSize[0], self.renderSize[1])

    def set2D(self):
        Mat4.ortho(self.projMat, 0, self.windowSize[0], 0, self.windowSize[1], -1, 1)
        Mat4.identity(self.mvMat)
        return self
        

    def set2DFixed(self):
        
        w, h = self.windowSize

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()



class FwPyGame:

    def checkEvents(fw):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:                
                #print("KEYDOWN: key =", event.key)
                fw.onKeyDown(event.key)
            elif event.type == pygame.KEYUP:
                fw.onKeyUp(event.key)

        return True

    def gameLoop(fw, app):
        pygame.init()
        pygame.display.set_mode(fw.windowSize, DOUBLEBUF | OPENGL, vsync=1)

        fw.onInit(app)
        running = True
        while running:
            running = FwPyGame.checkEvents(fw)
            if not running:
                break
            fw.onFrame()
            pygame.display.flip()

