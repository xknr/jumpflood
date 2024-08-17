from OpenGL.GL import *

from abc import ABC, abstractmethod

class Ogl:

    def create_shader(shader_type, source):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        status = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if not status:
            info_log = glGetShaderInfoLog(shader)
            print(f"Error compiling {shader_type} shader: {info_log}")
            #print(source)
            return None
        return shader

    def create_program(vertex_shader, fragment_shader):
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        status = glGetProgramiv(program, GL_LINK_STATUS)
        if not status:
            info_log = glGetProgramInfoLog(program)
            print(f"Error linking program: {info_log}")
            return None
        return program


class AttrInfo():
    def __init__(self, name, size, type, loc) -> None:
        self.name = name
        self.size = size
        self.type = type
        self.loc = loc
 
class ProgramAbstract(ABC):
    def __init__(self) -> None:
        pass

    def release(self):
        if self.program:
            glDeleteProgram(self.program)
            self.program = 0

    def createFromFile(self, vFilename, fFilename):
        # Read vertex shader code from file
        with open(vFilename, "r") as file:
            vsrc = file.read()

        # Read fragment shader code from file
        with open(fFilename, "r") as file:
            fsrc = file.read()

        self.create(vsrc, fsrc)
    def create(self, vsrc, fsrc):
        vertex_shader = Ogl.create_shader(GL_VERTEX_SHADER, vsrc)
        fragment_shader = Ogl.create_shader(GL_FRAGMENT_SHADER, fsrc)
        
        self.program = Ogl.create_program(vertex_shader, fragment_shader)

        glDeleteShader(fragment_shader)
        glDeleteShader(vertex_shader)

        self.getUniforms()
        self.getAttribs()

    def getUniforms(self):
        num_uniforms = glGetProgramiv(self.program, GL_ACTIVE_UNIFORMS)
        self.unis = dict()
        activeUniformMaxLength = glGetProgramiv(self.program, GL_ACTIVE_UNIFORM_MAX_LENGTH)
        for i in range(num_uniforms):
            inf = self.fetchUniInfo(i, activeUniformMaxLength)
            self.unis[inf.name] = inf

    def numpyArrayToStr(asciiCodes, strLen):
        s = ""
        for j in range(strLen):
            a = asciiCodes[j]
            if a == 0:
                break
            s += chr(a)
        return s


    def fetchUniInfo(self, index, activeUniformMaxLength):
        uname = glGetActiveUniformName(self.program, index, activeUniformMaxLength)
        nameLen, nameData = uname[0], uname[1]
        uname = ProgramAbstract.numpyArrayToStr(nameData, nameLen)
        usize = glGetActiveUniform(self.program, index, GL_UNIFORM_SIZE)
        utype = glGetActiveUniform(self.program, index, GL_UNIFORM_TYPE)
        uloc = glGetUniformLocation(self.program, uname)
        return AttrInfo(uname, usize, utype, uloc)

    def getAttribs(self):
        num_attribs = glGetProgramiv(self.program, GL_ACTIVE_ATTRIBUTES)
        self.atts = dict()
        activeAttrMaxLen = glGetProgramiv(self.program, GL_ACTIVE_ATTRIBUTE_MAX_LENGTH)
        for i in range(num_attribs):
            inf = self.fetchAttrInfo(i, activeAttrMaxLen)
            self.atts[inf.name] = inf

    def fetchAttrInfo(self, index, activeAttrMaxLen):
        name, size, type = glGetActiveAttrib(self.program, index, activeAttrMaxLen)            
        name = name.decode('UTF-8')
        loc = glGetAttribLocation(self.program, name)
        return AttrInfo(name, size, type, loc)

    @abstractmethod
    def updateMatrices(self, fw):
        pass

class Program(ProgramAbstract):

    def __init__(self):
        super().__init__()

    def release(self):
        super().release()

    def updateMatrices(self, fw):
        glUniformMatrix4fv(self.unis["uProjMat"].loc, 1, GL_FALSE, fw.projMat)
        glUniformMatrix4fv(self.unis["uMvMat"].loc, 1, GL_FALSE, fw.mvMat)

        

class RenderTarget():
    def __init__(self, width, height):
        self.width = width
        self.height = height        


    def create(self):
        width, height = self.width, self.height
        fbo = glGenFramebuffers(1)

        glBindFramebuffer(GL_FRAMEBUFFER, fbo)

        # Create a color texture object (texture)
        colorTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, colorTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)  
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, colorTexture, 0)
        glBindTexture(GL_TEXTURE_2D, 0)


        """
        # Create a color renderbuffer object (texture)
        color_rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, color_rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA8, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, color_rbo)
        """

        """
        # Create a depth renderbuffer object (texture)
        depth_rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depth_rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_rbo)
        """

        # Check if the framebuffer is complete
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            print("Error: Framebuffer is not complete.")
            return None

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        self.fbo = fbo
        self.colorTexture = colorTexture

    def release(self):
        if self.colorTexture:
            glDeleteTextures(1, [self.colorTexture])
            self.colorTexture = 0
            
        if self.fbo:
            glDeleteFramebuffers(1, [self.fbo])
            self.fbo = 0
