# coding=utf-8
"""Dibujo de un tablero de ajedrez con damas"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.easy_shaders as es
import grafica.basic_shapes as bs
from grafica.gpu_shape import GPUShape, SIZE_IN_BYTES

# We will use 32 bits data, so floats and integers have 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')


def createQuad():

    # Defining locations and colors for each vertex of the shape
    # Four vertices(rows) create a square with respective indicate color(in each row).
    
    vertexData = np.array([ 
    #   positions        colors
        -0.8, -0.8, 0.0,  0.0, 0.0, 0.0,
        -0.6, -0.8, 0.0,  0.0, 0.0, 0.0, 
        -0.6,  0.8, 0.0,  0.0, 0.0, 0.0, 
        -0.8,  0.8, 0.0,  0.0, 0.0, 0.0,

        -0.6, -0.8, 0.0,  1.0, 1.0, 1.0,
        -0.4, -0.8, 0.0,  1.0, 1.0, 1.0,
        -0.4,  0.8, 0.0,  1.0, 1.0, 1.0,
        -0.6,  0.8, 0.0,  1.0, 1.0, 1.0,

        -0.4, -0.8, 0.0,  0.0, 0.0, 0.0,
        -0.2, -0.8, 0.0,  0.0, 0.0, 0.0,
        -0.2,  0.8, 0.0,  0.0, 0.0, 0.0,
        -0.4,  0.8, 0.0,  0.0, 0.0, 0.0,

        -0.2, -0.8, 0.0,  1.0, 1.0, 1.0,
         0.0, -0.8, 0.0,  1.0, 1.0, 1.0,
         0.0,  0.8, 0.0,  1.0, 1.0, 1.0,
        -0.2,  0.8, 0.0,  1.0, 1.0, 1.0,

         0.0,  -0.8, 0.0,  0.0, 0.0, 0.0,
         0.2,  -0.8, 0.0,  0.0, 0.0, 0.0,
         0.2,   0.8, 0.0,  0.0, 0.0, 0.0,
         0.0,   0.8, 0.0,  0.0, 0.0, 0.0,

         0.2, -0.8, 0.0,  1.0, 1.0, 1.0,
         0.4, -0.8, 0.0,  1.0, 1.0, 1.0,
         0.4,  0.8, 0.0,  1.0, 1.0, 1.0,
         0.2,  0.8, 0.0,  1.0, 1.0, 1.0,
         
         0.4,  -0.8, 0.0,  0.0, 0.0, 0.0,
         0.6,  -0.8, 0.0,  0.0, 0.0, 0.0,
         0.6,   0.8, 0.0,  0.0, 0.0, 0.0,
         0.4,   0.8, 0.0,  0.0, 0.0, 0.0,

         0.6, -0.8, 0.0,  1.0, 1.0, 1.0,
         0.8, -0.8, 0.0,  1.0, 1.0, 1.0,
         0.8,  0.8, 0.0,  1.0, 1.0, 1.0,
         0.6,  0.8, 0.0,  1.0, 1.0, 1.0,

        -0.8,  0.4, 0.0,  1.0, 1.0, 1.0,
        -0.8,  0.6, 0.0,  1.0, 1.0, 1.0,
         0.8,  0.6, 0.0,  1.0, 1.0, 1.0,
         0.8,  0.4, 0.0,  1.0, 1.0, 1.0,

        -0.8,  0.0, 0.0,  1.0, 1.0, 1.0,
        -0.8,  0.2, 0.0,  1.0, 1.0, 1.0,
         0.8,  0.2, 0.0,  1.0, 1.0, 1.0,
         0.8,  0.0, 0.0,  1.0, 1.0, 1.0,

        -0.8, -0.4, 0.0,  1.0, 1.0, 1.0,
        -0.8, -0.2, 0.0,  1.0, 1.0, 1.0,
         0.8, -0.2, 0.0,  1.0, 1.0, 1.0,
         0.8, -0.4, 0.0,  1.0, 1.0, 1.0,

        -0.8, -0.8, 0.0,  1.0, 1.0, 1.0,
        -0.8, -0.6, 0.0,  1.0, 1.0, 1.0,
         0.8, -0.6, 0.0,  1.0, 1.0, 1.0,
         0.8, -0.8, 0.0,  1.0, 1.0, 1.0,

        -0.6,  0.4, 0.0,  0.0, 0.0, 0.0,
        -0.6,  0.6, 0.0,  0.0, 0.0, 0.0,
        -0.4,  0.6, 0.0,  0.0, 0.0, 0.0,
        -0.4,  0.4, 0.0,  0.0, 0.0, 0.0,

         0.0,  0.4, 0.0,  0.0, 0.0, 0.0,
         0.0,  0.6, 0.0,  0.0, 0.0, 0.0,
        -0.2,  0.6, 0.0,  0.0, 0.0, 0.0,
        -0.2,  0.4, 0.0,  0.0, 0.0, 0.0,

         0.2,  0.4, 0.0,  0.0, 0.0, 0.0,
         0.2,  0.6, 0.0,  0.0, 0.0, 0.0,
         0.4,  0.6, 0.0,  0.0, 0.0, 0.0,
         0.4,  0.4, 0.0,  0.0, 0.0, 0.0,

         0.6,  0.4, 0.0,  0.0, 0.0, 0.0,
         0.6,  0.6, 0.0,  0.0, 0.0, 0.0,
         0.8,  0.6, 0.0,  0.0, 0.0, 0.0,
         0.8,  0.4, 0.0,  0.0, 0.0, 0.0,

        -0.6,  0.0, 0.0,  0.0, 0.0, 0.0,
        -0.6,  0.2, 0.0,  0.0, 0.0, 0.0,
        -0.4,  0.2, 0.0,  0.0, 0.0, 0.0,
        -0.4,  0.0, 0.0,  0.0, 0.0, 0.0,

         0.0,  0.0, 0.0,  0.0, 0.0, 0.0,
         0.0,  0.2, 0.0,  0.0, 0.0, 0.0,
        -0.2,  0.2, 0.0,  0.0, 0.0, 0.0,
        -0.2,  0.0, 0.0,  0.0, 0.0, 0.0,

         0.2,  0.0, 0.0,  0.0, 0.0, 0.0,
         0.2,  0.2, 0.0,  0.0, 0.0, 0.0,
         0.4,  0.2, 0.0,  0.0, 0.0, 0.0,
         0.4,  0.0, 0.0,  0.0, 0.0, 0.0,

         0.6,  0.0, 0.0,  0.0, 0.0, 0.0,
         0.6,  0.2, 0.0,  0.0, 0.0, 0.0,
         0.8,  0.2, 0.0,  0.0, 0.0, 0.0,
         0.8,  0.0, 0.0,  0.0, 0.0, 0.0,

        -0.6, -0.4, 0.0,  0.0, 0.0, 0.0,
        -0.6, -0.2, 0.0,  0.0, 0.0, 0.0,
        -0.4, -0.2, 0.0,  0.0, 0.0, 0.0,
        -0.4, -0.4, 0.0,  0.0, 0.0, 0.0,

         0.0, -0.4, 0.0,  0.0, 0.0, 0.0,
         0.0, -0.2, 0.0,  0.0, 0.0, 0.0,
        -0.2, -0.2, 0.0,  0.0, 0.0, 0.0,
        -0.2, -0.4, 0.0,  0.0, 0.0, 0.0,

         0.2, -0.4, 0.0,  0.0, 0.0, 0.0,
         0.2, -0.2, 0.0,  0.0, 0.0, 0.0,
         0.4, -0.2, 0.0,  0.0, 0.0, 0.0,
         0.4, -0.4, 0.0,  0.0, 0.0, 0.0,

         0.6, -0.4, 0.0,  0.0, 0.0, 0.0,
         0.6, -0.2, 0.0,  0.0, 0.0, 0.0,
         0.8, -0.2, 0.0,  0.0, 0.0, 0.0,
         0.8, -0.4, 0.0,  0.0, 0.0, 0.0,

        -0.6, -0.8, 0.0,  0.0, 0.0, 0.0,
        -0.6, -0.6, 0.0,  0.0, 0.0, 0.0,
        -0.4, -0.6, 0.0,  0.0, 0.0, 0.0,
        -0.4, -0.8, 0.0,  0.0, 0.0, 0.0,

         0.0, -0.6, 0.0,  0.0, 0.0, 0.0,
         0.0, -0.8, 0.0,  0.0, 0.0, 0.0,
        -0.2, -0.8, 0.0,  0.0, 0.0, 0.0,
        -0.2, -0.6, 0.0,  0.0, 0.0, 0.0,

         0.2, -0.6, 0.0,  0.0, 0.0, 0.0,
         0.2, -0.8, 0.0,  0.0, 0.0, 0.0,
         0.4, -0.8, 0.0,  0.0, 0.0, 0.0,
         0.4, -0.6, 0.0,  0.0, 0.0, 0.0,

         0.6, -0.8, 0.0,  0.0, 0.0, 0.0,
         0.6, -0.6, 0.0,  0.0, 0.0, 0.0,
         0.8, -0.6, 0.0,  0.0, 0.0, 0.0,
         0.8, -0.8, 0.0,  0.0, 0.0, 0.0,
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    #Must have same quantity of group vertices and group of indices.
    #Indice are related with respective vertices.
    indices = np.array(
        [0, 1, 2,
         2, 3, 0,

         4, 5, 6,
         6, 7, 4,
         
         8, 9, 10,
         10, 11, 8,
         
         12, 13, 14,
         14, 15, 12,
         
         16, 17, 18,
         18, 19, 16,
         
         20, 21, 22,
         22, 23, 20,

         24, 25, 26,
         26, 27, 24,
         
         28, 29, 30,
         30, 31, 28,
         
         32, 33, 34,
         34, 35, 32,
         
         36, 37, 38,
         38, 39, 36,
         
         40, 41 ,42,
         42, 43, 40,
         
         44, 45, 46,
         46, 47, 44,
         
         48, 49, 50,
         50, 51, 48,

         52, 53, 54,
         54, 55, 52,
         
         56, 57, 58,
         58, 59, 56,
         
         60, 61, 62,
         62, 63, 60,
         
         64, 65, 66,
         66, 67, 64,
         
         68, 69, 70,
         70, 71, 68,
         
         72, 73, 74,
         74, 75, 72,
         
         76, 77, 78,
         78, 79, 76,

         80, 81, 82,
         82, 83, 80,
         
         84, 85, 86,
         86, 87, 84,
         
         88, 89, 90,
         90, 91, 88,
         
         92, 93, 94,
         94, 95, 92,
         
         96, 97, 98,
         98, 99, 96,
         
         100, 101, 102,
         102, 103, 100,
         
         104, 105, 106,
         106, 107, 104,
         
         108, 109, 110,
         110, 111, 108], dtype= np.uint32)

    size = len(indices)
    #We supose to return an array with vertices and dtype=np.float32 but didn't work in that way
    # So I replace array for bs.Shape
    return bs.Shape(vertexData, indices)

#We create checkers 
def crear_dama(): #x=-0.7, y=0.7, r=1.0, g=0.0 b=0.0, radius=0.1
    
    circle = [] #Empty list
    for angle in range(0,360,10):
        #We extend list "circle" with the element in this line of code three times to create de circle
        # also we choose color in that way to do a "shadow effect" in the center of each one
        # that because a simple circle it's bored. We do this 12 times changing positions and keeping red color
        #and its radius. Then other 12 times but with color blue. 
        circle.extend([-0.7, 0.7, 0.0, 0.5, 0.0, 0.0])
        circle.extend([-0.7+np.cos(np.radians(angle))*0.07, 
                       0.7+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([-0.7+np.cos(np.radians(angle+10))*0.07, 
                       0.7+np.sin(np.radians(angle+10))*0.07, 
                       0.0, 0.8, 0.0, 0.0]) #First Red checkers

        circle.extend([-0.3, 0.7, 0.0, 0.5, 0.0, 0.0])
        circle.extend([-0.3+np.cos(np.radians(angle))*0.07, 
                       0.7+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([-0.3+np.cos(np.radians(angle+10))*0.07, 
                       0.7+np.sin(np.radians(angle+10))*0.07, 
                       0.0, 0.8, 0.0, 0.0]) #Second Red checkers

        circle.extend([0.1, 0.7, 0.0, 0.5, 0.0, 0.0])
        circle.extend([0.1+np.cos(np.radians(angle))*0.07, 
                       0.7+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([0.1+np.cos(np.radians(angle+10))*0.07, 
                       0.7+np.sin(np.radians(angle+10))*0.07, 
                       0.0, 0.8, 0.0, 0.0]) #Third Red checkers

        circle.extend([0.5, 0.7, 0.0, 0.5, 0.0, 0.0])
        circle.extend([0.5+np.cos(np.radians(angle))*0.07, 
                       0.7+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([0.5+np.cos(np.radians(angle+10))*0.07, 
                       0.7+np.sin(np.radians(angle+10))*0.07, 
                       0.0, 0.8, 0.0, 0.0]) #Fourth Red checkers

        circle.extend([-0.5, 0.5, 0.0, 0.5, 0.0, 0.0])
        circle.extend([-0.5+np.cos(np.radians(angle))*0.07, 
                       0.5+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([-0.5+np.cos(np.radians(angle+10))*0.07, 
                       0.5+np.sin(np.radians(angle+10))*0.07, 
                       0.0, 0.8, 0.0, 0.0]) #Fifth Red checkers
        
        circle.extend([-0.1, 0.5, 0.0, 0.5, 0.0, 0.0])
        circle.extend([-0.1+np.cos(np.radians(angle))*0.07, 
                       0.5+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([-0.1+np.cos(np.radians(angle+10))*0.07, 
                       0.5+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.8, 0.0, 0.0]) #Sixth Red checkers
        
        circle.extend([0.3, 0.5, 0.0, 0.5, 0.0, 0.0])
        circle.extend([0.3+np.cos(np.radians(angle))*0.07, 
                       0.5+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([0.3+np.cos(np.radians(angle+10))*0.07, 
                       0.5+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.8, 0.0, 0.0]) #Seventh Red checkers

        circle.extend([0.7, 0.5, 0.0, 0.5, 0.0, 0.0])
        circle.extend([0.7+np.cos(np.radians(angle))*0.07, 
                       0.5+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([0.7+np.cos(np.radians(angle+10))*0.07, 
                       0.5+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.8, 0.0, 0.0]) #eighth Red checkers
        
        circle.extend([-0.7, 0.3, 0.0, 0.5, 0.0, 0.0])
        circle.extend([-0.7+np.cos(np.radians(angle))*0.07, 
                       0.3+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([-0.7+np.cos(np.radians(angle+10))*0.07, 
                       0.3+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.8, 0.0, 0.0]) #Ninth Red checkers
        
        circle.extend([-0.3, 0.3, 0.0, 0.5, 0.0, 0.0])
        circle.extend([-0.3+np.cos(np.radians(angle))*0.07, 
                       0.3+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([-0.3+np.cos(np.radians(angle+10))*0.07, 
                       0.3+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.8, 0.0, 0.0]) #Tenth Red checkers

        circle.extend([0.1, 0.3, 0.0, 0.5, 0.0, 0.0])
        circle.extend([0.1+np.cos(np.radians(angle))*0.07, 
                       0.3+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([0.1+np.cos(np.radians(angle+10))*0.07, 
                       0.3+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.8, 0.0, 0.0]) #Eleventh Red checkers
        
        circle.extend([0.5, 0.3, 0.0, 0.5, 0.0, 0.0])
        circle.extend([0.5+np.cos(np.radians(angle))*0.07, 
                       0.3+np.sin(np.radians(angle))*0.07, 
                       0.0, 1.0, 0.0, 0.0])
        circle.extend([0.5+np.cos(np.radians(angle+10))*0.07, 
                       0.3+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.8, 0.0, 0.0]) #twelfth

        circle.extend([-0.5,-0.3, 0.0, 0.0, 0.0, 0.5])
        circle.extend([-0.5+np.cos(np.radians(angle))*0.07, 
                      -0.3+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([-0.5+np.cos(np.radians(angle+10))*0.07, 
                       -0.3+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #First Blue checkers
        
        circle.extend([-0.1,-0.3, 0.0, 0.0, 0.0, 0.5])
        circle.extend([-0.1+np.cos(np.radians(angle))*0.07, 
                      -0.3+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([-0.1+np.cos(np.radians(angle+10))*0.07, 
                       -0.3+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Second Blue checkers
        circle.extend([0.3,-0.3, 0.0, 0.0, 0.0, 0.5])
        circle.extend([0.3+np.cos(np.radians(angle))*0.07, 
                      -0.3+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([0.3+np.cos(np.radians(angle+10))*0.07, 
                       -0.3+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Third Blue checkers
        
        circle.extend([0.7,-0.3, 0.0, 0.0, 0.0, 0.5])
        circle.extend([0.7+np.cos(np.radians(angle))*0.07, 
                      -0.3+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([0.7+np.cos(np.radians(angle+10))*0.07, 
                       -0.3+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Fourth Blue checkers

        circle.extend([-0.7,-0.5, 0.0, 0.0, 0.0, 0.5])
        circle.extend([-0.7+np.cos(np.radians(angle))*0.07, 
                      -0.5+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([-0.7+np.cos(np.radians(angle+10))*0.07, 
                       -0.5+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Fifth Blue checkers
        
        circle.extend([-0.3,-0.5, 0.0, 0.0, 0.0, 0.5])
        circle.extend([-0.3+np.cos(np.radians(angle))*0.07, 
                      -0.5+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([-0.3+np.cos(np.radians(angle+10))*0.07, 
                       -0.5+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Sixth Blue checkers
        
        circle.extend([0.1,-0.5, 0.0, 0.0, 0.0, 0.5])
        circle.extend([0.1+np.cos(np.radians(angle))*0.07, 
                      -0.5+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([0.1+np.cos(np.radians(angle+10))*0.07, 
                       -0.5+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Seventh Blue checkers
        
        circle.extend([0.5,-0.5, 0.0, 0.0, 0.0, 0.5])
        circle.extend([0.5+np.cos(np.radians(angle))*0.07, 
                      -0.5+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([0.5+np.cos(np.radians(angle+10))*0.07, 
                       -0.5+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Eighth Blue checkers
        
        circle.extend([-0.5,-0.7, 0.0, 0.0, 0.0, 0.5])
        circle.extend([-0.5+np.cos(np.radians(angle))*0.07, 
                      -0.7+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([-0.5+np.cos(np.radians(angle+10))*0.07, 
                       -0.7+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Ninth Blue checkers
        
        circle.extend([-0.1,-0.7, 0.0, 0.0, 0.0, 0.5])
        circle.extend([-0.1+np.cos(np.radians(angle))*0.07, 
                      -0.7+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([-0.1+np.cos(np.radians(angle+10))*0.07, 
                       -0.7+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Tenth Blue checkers
        
        circle.extend([0.3,-0.7, 0.0, 0.0, 0.0, 0.5])
        circle.extend([0.3+np.cos(np.radians(angle))*0.07, 
                      -0.7+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([0.3+np.cos(np.radians(angle+10))*0.07, 
                       -0.7+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Eleventh Blue checkers
        
        circle.extend([0.7,-0.7, 0.0, 0.0, 0.0, 0.5])
        circle.extend([0.7+np.cos(np.radians(angle))*0.07, 
                      -0.7+np.sin(np.radians(angle))*0.07, 
                       0.0, 0.0, 0.0, 1.0])
        circle.extend([0.7+np.cos(np.radians(angle+10))*0.07, 
                       -0.7+np.sin(np.radians(angle+10))*0.07,
                       0.0, 0.0, 0.0, 0.8]) #Twelfth Blue checkers
    
    #We return a bs.Shape with circle and range with its len
    return bs.Shape(circle, range(len(circle)))


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    #Window size
    width = 600
    height = 600

    window = glfw.create_window(width, height, "ChessBoard", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleShaderProgram()

    # Creating shapes on GPU memory
    squareshape = createQuad()
    gpuShape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(squareshape.vertices, squareshape.indices, GL_STATIC_DRAW)

    #Creating circle shapes on GPU memory
    circleshape = crear_dama()
    # We use GPUShape (import)
    gpuCircle = GPUShape().initBuffers()
    pipeline.setupVAO(gpuCircle)
    gpuCircle.fillBuffers(circleshape.vertices, circleshape.indices, GL_STATIC_DRAW)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Se le dice a OpenGL que use el shaderProgram simple
        glUseProgram(pipeline.shaderProgram)
        pipeline.drawCall(gpuShape) # Se la letra
        pipeline.drawCall(gpuCircle)
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuShape.clear()

    glfw.terminate()