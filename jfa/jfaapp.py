from fw.fw import Fw, App, FwPyGame
from jfa.jfasteps import JfaSteps
from jfa.jfa import Jfa
from fw.blitter import Blitter
from jfa.drawItems import DrawItems

from OpenGL.GL import * # pip install PyOpenGL
#from OpenGL.GLUT import *

import pygame

class JfaApp(App):

    methods = [JfaSteps.jfa, 
        JfaSteps.jfaIncreasing, 
        JfaSteps.jfa1, JfaSteps.jfa2, 
        JfaSteps._1jfa, JfaSteps.jfaPow2]

    
    def __init__(self, fw) -> None:
        self.fw = fw
        self.bShowDistance = True

    def create(self) -> None:

        self.setMethodId(0)

        self.elapsed = 0.0

        # Dummy value. TODO: Use actual time measurement code.
        self.frameDelta = 1.0 / 60.0 

        self.jfa = Jfa(self.fw)
        self.jfa.create()

        self.blitter = Blitter(self.fw)        
        self.blitter.create()

        self.drawItems = DrawItems(self.fw.windowSize)
        self.drawItems.create(self.fw, self.blitter.programBlit)

    def release(self):
        self.jfa.release()
        self.blitter.release()
        self.drawItems.release()
        pass

    def onFrame(self):

        self.bShowDistance = not self.fw.isKeyDown(32)

        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)
        glDepthMask(False)

        self.paintMap(self.jfa.surface[1])

        method = JfaApp.methods[self.methodId]
        self.jfa.process(method, self.bShowDistance)

        self.blitter.blitResult(self.jfa.surface[0].colorTexture)

        self.drawItems.updateParticles()

        self.elapsed += self.frameDelta

    def keyDown(self, key):

        if key == pygame.K_LEFT or key == pygame.K_RIGHT:

            if key == pygame.K_LEFT:
                self.methodId -= 1
            elif key == pygame.K_RIGHT:
                self.methodId += 1

            # Wrap around in both cases.
            self.methodId = (self.methodId + len(JfaApp.methods)) % len(JfaApp.methods)
            self.setMethodId(self.methodId)

    def setMethodId(self, methodId):
        self.methodId = methodId

        method =  JfaApp.methods[self.methodId]
        steps = method(self.fw.windowSize[0], self.fw.windowSize[1])
        print(steps)

        

    def keyUp(self, key):
        pass

    def paintMap(self, renderTarget):

        w, h = self.fw.windowSize
        
        self.fw.setRenderTarget(renderTarget)
        self.fw.clearScreen(0, 0, 0, 0, 1.0, 1, True, False, False)

        self.drawItems.draw(self.elapsed)

        self.fw.setRenderTarget(None)
