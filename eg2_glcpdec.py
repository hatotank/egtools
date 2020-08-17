#! /usr/bin/env python

# ラスピリのAlpha8なpngのデコードスクリプト(python) ID:nK9ql/in
# ChromaPack-PlaneTransparent Alpha 8bit(YCbCr+Alpha) -> RGBA32PNG

# Modification by hatotank

# $pip install Pillow
# $pip install numpy
# $pip install PyOpenGL
## $pip install opencv-python
# C:\Windows\System32\glut64.dll (http://ktm11.eng.shizuoka.ac.jp/lesson/modeling.html)
# $python eg2_glcpdec.py [-m] shader.vert shader.flag input.png output.png

import numpy as np
import cv2
import sys
import os
import time
from PIL import Image
import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *

import argparse # hatotank

vertices = None
indices = None
texture_file = None

def saveImage(imageWidth, imageHeight, outname):
    glReadBuffer( GL_BACK )
#    temp = np.zeros((imageWidth, imageHeight, 4), dtype=np.uint8) # hatotank
    temp = np.zeros((imageHeight,imageWidth, 4), dtype=np.uint8) # hatotank
    
    glReadPixels( 0,
                  0,
                  imageWidth,
                  imageHeight,
                  GL_RGBA,
                  GL_UNSIGNED_BYTE,
                  temp )
    temp = cv2.cvtColor(temp, cv2.COLOR_BGRA2RGBA)
    temp = cv2.flip(temp, 0)
    cv2.imwrite(outname, temp)

def InitGL( vertex_shade_code, fragment_shader_code, texture_image ):
    glClearColor(0.0, 0.0, 0.0, 0.0)

    texture_id = glGenTextures( 1 )
    glPixelStorei( GL_UNPACK_ALIGNMENT, 1 )
    glActiveTexture( GL_TEXTURE0 )
    glBindTexture( GL_TEXTURE_2D, texture_id )

    if texture_image.mode == 'RGB':
        glTexImage2D( GL_TEXTURE_2D,
                      0,
                      4,
                      texture_image.size[0],
                      texture_image.size[1],
                      0,
                      GL_RGB,
                      GL_UNSIGNED_BYTE,
                      texture_image.tobytes() )
    else:
        glTexImage2D( GL_TEXTURE_2D,
                      0,
                      4,
                      texture_image.size[0],
                      texture_image.size[1],
                      0,
                      GL_RGBA,
                      GL_UNSIGNED_BYTE,
                      texture_image.tobytes() )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )

    program = compileProgram(
        compileShader( vertex_shade_code,GL_VERTEX_SHADER),
        compileShader( fragment_shader_code,GL_FRAGMENT_SHADER),)

    glUseProgram(program)
    glUniform1i( glGetUniformLocation( program, "s_texture" ), 0 );
    glUniform1f( glGetUniformLocation( program, "texture_width" ), float( texture_image.size[ 0 ] ) )
    glUniform1f( glGetUniformLocation( program, "texture_height" ), float( texture_image.size[ 1 ] ) )


    global vertices
    global indices
    position_vertices = [ -1.0,  1.0, 0.0,
                          -1.0, -1.0, 0.0,
                           1.0, -1.0, 0.0,
                           1.0,  1.0, 0.0, ]
    texture_vertices = [ 0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0 ]

    indices = [ 0, 1, 2, 0, 2, 3 ]

    position_loc = glGetAttribLocation( program, 'a_position' )
    glVertexAttribPointer( position_loc,
                           3,
                           GL_FLOAT,
                           GL_FALSE,
                           3 * 4,
                           np.array( position_vertices, np.float32 ) )

    tex_loc = glGetAttribLocation( program, 'a_texCoord' )
    glVertexAttribPointer( tex_loc,
                           2,
                           GL_FLOAT,
                           GL_FALSE,
                           2 * 4,
                           np.array( texture_vertices, np.float32 ) )

    glEnableVertexAttribArray( position_loc )
    glEnableVertexAttribArray( tex_loc )


def ReSizeGLScene(Width, Height):
    glViewport(0, 0, Width, Height)

# The main drawing function.
def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable( GL_TEXTURE_2D )

    glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, np.array( indices, np.uint16 ) )
    glDisable(GL_TEXTURE_2D)

    glutSwapBuffers()

def keyPressed(*args):
    # If escape is pressed, kill everything.    
#    print(args[0]) # hatotank
    
    if args[0] == b'\x0d':
      fname = "_rgb-converted".join(os.path.splitext(texture_file))
      saveImage(glutGet(GLUT_WINDOW_WIDTH),glutGet(GLUT_WINDOW_HEIGHT),fname)
      print("| OUTPUT | {0}".format(fname))
      sys.exit()

# hatotank str
def timer(value):
    saveImage(glutGet(GLUT_WINDOW_WIDTH),glutGet(GLUT_WINDOW_HEIGHT),args.destination_file)
    print("| OUTPUT | {0}".format(args.destination_file))
    sys.exit()
# hatotank end

def usage():
    print("usage:{0} vertex_shader_file fragment_shader_file texture_file".format(sys.argv[ 0 ]))

def main():
    global texture_file
    # hatotank str
    global args
    """
    try:
        vertex_shader_file = sys.argv[ 1 ]
        fragment_shader_file = sys.argv[ 2 ]
        texture_file = sys.argv[ 3 ]
    except IndexError:
        usage()
        sys.exit( -1 )
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("vertex_shader_file")
    parser.add_argument("fragment_shader_file")
    parser.add_argument("texture_file")
    parser.add_argument("destination_file")
    parser.add_argument("-m","--mask",help="image with iamge mask",action="store_true")
    args = parser.parse_args()
    vertex_shader_file = args.vertex_shader_file
    fragment_shader_file = args.fragment_shader_file
    texture_file = args.texture_file
    destination_file = args.destination_file
    # hatotank end

    vertex_shade_code = '\n'.join( open( vertex_shader_file, 'r' ).readlines() )
#    fragment_shader_code = '\n'.join( open( fragment_shader_file, 'r' ).readlines()) # hatotank
    fragment_shader_code = open( fragment_shader_file, 'r' ).readlines() # hatotank
    texture_image = Image.open( texture_file )
    if texture_image.mode == 'P':
        texture_image = texture_image.convert("RGBA")
    assert texture_image.mode == 'RGBA' or texture_image.mode == 'RGB'

    # hatotank str
    if args.mask:
      fragment_shader_code = [code.replace('//--mask//','') for code in fragment_shader_code]
    else:
      fragment_shader_code = [code.replace('//default// ','') for code in fragment_shader_code]
	  # hatotank end

    glutInit(sys.argv)

    if texture_image.mode == 'RGBA':
        # glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH) # alpha off
         glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA) # alpha on
    else:
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

#    glutInitWindowSize( int(texture_image.size[0] / 2), texture_image.size[1] ) # hatotank
    # hatotank str
    if args.mask:
      texture_width = int(texture_image.size[0] * 2 / 5)
    else:
      texture_width = int(texture_image.size[0] * 2 / 3)
    
    glutInitWindowSize( texture_width, texture_image.size[1] )
    # hatotank end

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    glutCreateWindow(b"Hello")

    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    # Register the function called when a specified number of milliseconds. # hatotank
    glutTimerFunc(2000,timer, 0) # hatotank

    # Initialize our window.
    InitGL( vertex_shade_code, fragment_shader_code, texture_image )

    # Start Event Processing Engine
    glutMainLoop()

if __name__ == "__main__":
#    print("Hit ENTER key to save & quit.") # hatotank
    main()
