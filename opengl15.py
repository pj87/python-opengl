#!/usr/bin/python2.7
"""Quick hack of 'modern' OpenGL example using pysdl2 and pyopengl

Based on

pysdl2 OpenGL example
http://www.arcsynthesis.org/gltut/Basics/Tut02%20Vertex%20Attributes.html
http://schi.iteye.com/blog/1969710
"""
import sys
import ctypes
import numpy

from OpenGL import GL, GLU
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

import sdl2
from sdl2 import video
from numpy import array

def run():
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return -1

    window = sdl2.SDL_CreateWindow(b"OpenGL demo",
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
                                   sdl2.SDL_WINDOW_OPENGL)
    if not window:
        print(sdl2.SDL_GetError())
        return -1

    # Force OpenGL 3.3 'core' context.
    # Must set *before* creating GL context!
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK,
        video.SDL_GL_CONTEXT_PROFILE_CORE)
    context = sdl2.SDL_GL_CreateContext(window)

    quad = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
             0.5,  0.5, 0.0, 0.0, 0.0, 1.0, 
            -0.5,  0.5, 0.0, 1.0, 1.0, 1.0]

    quad = numpy.array(quad, dtype=numpy.float32)

    indices = [0, 1, 2, 
               2, 3, 0]

    indices = numpy.array(indices, dtype=numpy.uint32) 

    # Setup GL shaders, data, etc.
    vertex_shader = shaders.compileShader("""
   #version 330 
   in vec3 position; 
   in vec3 color; 

   out vec3 newColor; 
   void main() 
   { 
      gl_Position = vec4(position, 1.0f); 
      newColor = color; 
   } 
   """
   , GL.GL_VERTEX_SHADER)

    fragment_shader = shaders.compileShader("""
   #version 330 
   in vec3 newColor; 

   out vec4 outColor; 
   void main()
   {
      outColor = vec4(newColor, 1.0f); 
   }
   """
   , GL.GL_FRAGMENT_SHADER)


    shaderProgram = shaders.compileProgram(vertex_shader, fragment_shader)

    GL.glUseProgram(shaderProgram)

    VAO = GL.glGenVertexArrays(1);
    GL.glBindVertexArray(VAO);

    # Need VBO for triangle vertices and colours
    VBO = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, 96, quad, GL.GL_STATIC_DRAW)

    EBO = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, EBO)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, 24, indices, GL.GL_STATIC_DRAW)

    position = GL.glGetAttribLocation(shaderProgram, "position")
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(position)
    
    color = GL.glGetAttribLocation(shaderProgram, "color")
    GL.glVertexAttribPointer(color, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, ctypes.c_void_p(12))
    GL.glEnableVertexAttribArray(color)

    event = sdl2.SDL_Event()
    running = True
    
    GL.glClearColor(0, 0, 0, 1)

    while running: 
       while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0: 
          if event.type == sdl2.SDL_QUIT: 
             running = False
          if event.type == sdl2.events.SDL_KEYDOWN: 
             print "SDL_KEYDOWN" 
             if event.key.keysym.sym == sdl2.SDLK_ESCAPE: 
                running = False
       GL.glClear(GL.GL_COLOR_BUFFER_BIT)
       GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)

       sdl2.SDL_GL_SwapWindow(window)
       #sdl2.SDL_Delay(10)

    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
