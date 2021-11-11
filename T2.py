# coding=utf-8
"""Tarea 2"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.viewPos = np.array([10,10,10])
        self.camUp = np.array([0, 1, 0])
        self.distance = 10


controller = Controller()

def setPlot(pipeline, mvpPipeline):
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 5, 5, 5)
    
    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

def setView(pipeline, mvpPipeline):
    view = tr.lookAt(
            controller.viewPos,
            np.array([0,0,0]),
            controller.camUp
        )

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])
    

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    
    elif key == glfw.KEY_1:
        controller.viewPos = np.array([controller.distance,controller.distance,controller.distance]) #Vista diagonal 1
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_2:
        controller.viewPos = np.array([0,0,controller.distance]) #Vista frontal
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_3:
        controller.viewPos = np.array([controller.distance,0,controller.distance]) #Vista lateral
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_4:
        controller.viewPos = np.array([0,controller.distance,0]) #Vista superior
        controller.camUp = np.array([1,0,0])
    
    elif key == glfw.KEY_5:
        controller.viewPos = np.array([controller.distance,controller.distance,-controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_6:
        controller.viewPos = np.array([-controller.distance,controller.distance,-controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_7:
        controller.viewPos = np.array([-controller.distance,controller.distance,controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    else:
        print('Unknown key')

def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

#NOTA: Aqui creas tu escena. En escencia, sólo tendrías que modificar esta función.
def createScene(pipeline):
    cone = createGPUShape(pipeline, bs.createColorConeTarea2(0.8,0.251,0.0))
    cone1 = createGPUShape(pipeline, bs.createColorConeTarea2(0.0,0.9,0.0))
    cone2 = createGPUShape(pipeline, bs.createColorConeTarea2(1.0,1.0,0.0))
    cube = createGPUShape(pipeline, bs.createColorCubeTarea2(0.0,0.9,0.0))
    cylinder = createGPUShape(pipeline, bs.createColorCylinderTarea2(1.0, 1.0, 1.0))
    cylinder1 = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.2,0.2,0.2))
    cylinder2 = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.0,0.9,0.0))
    cylinder3 = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.8,0.251,0.0))
    cylinder4 = createGPUShape(pipeline, bs.createColorCylinderTarea2(1.0,1.0,1.0))
    cylinder5 = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.0,0.3,0.0))

    #Ala1, se rota respecto a Z en pi/2 radianes. luego se translada para al final escalar y así formar el ala
    # verde de abajo.
    cubeNode = sg.SceneGraphNode('cube')
    cubeNode.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.translate(-0.3, -1.0, 0.0), tr.scale(0.1, 0.5, 3.0)])
    cubeNode.childs += [cube]
    
    #Ala2, se rota respecto a Z en pi/2 radianes. luego se translada para al final escalar y así formar el ala
    # verde de arriba.
    cubeNode1 = sg.SceneGraphNode('cube')
    cubeNode1.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.translate(1.8, -1.3, 0.0), tr.scale(0.1, 0.5, 3.0)])
    cubeNode1.childs += [cube]

    #Tubo que une a las ruedas se rota respecto al eje X, se translada y luego se escala.
    cylinderNode = sg.SceneGraphNode('cylinder')
    cylinderNode.transform = tr.matmul([tr.rotationX(np.pi/2), tr.translate(1.0, 0.0, 1.0), tr.scale(0.08, 0.5, 0.08)])
    cylinderNode.childs += [cylinder]

    #Rueda1 que se rota respecto al eje X, se traslada y luego se escala.
    cylinderNode1 = sg.SceneGraphNode('cylinder1')
    cylinderNode1.transform = tr.matmul([tr.rotationX(np.pi/2),tr.translate(1.0, 0.5, 1.0), tr.scale(0.3, 0.08, 0.3)])
    cylinderNode1.childs += [cylinder1]

    #Rueda2 que se rota respecto al eje X, se traslada y luego se escala.
    cylinderNode2 = sg.SceneGraphNode('cylinder1')
    cylinderNode2.transform = tr.matmul([tr.rotationX(np.pi/2),tr.translate(1.0, -0.5, 1.0), tr.scale(0.3, 0.08, 0.3)])
    cylinderNode2.childs += [cylinder1]

    #Redondela alas1, simula el contorno circular del borde de las alas
    # se translada, se rota respecto al eje Y y se escala.
    cylinderNode3 = sg.SceneGraphNode('cylinder2')
    cylinderNode3.transform = tr.matmul([tr.translate(1.0, -0.3, 3.0), tr.rotationY(np.pi),tr.scale(0.5, 0.1, 0.3)])
    cylinderNode3.childs += [cylinder2]

    #Redondela alas2, simula el contorno circular del borde de las alas
    # se translada, se rota respecto al eje Y y se escala.
    cylinderNode4 = sg.SceneGraphNode('cylinder2')
    cylinderNode4.transform = tr.matmul([tr.translate(1.0, -0.3, -3.0), tr.rotationY(np.pi),tr.scale(0.5, 0.1, 0.3)])
    cylinderNode4.childs += [cylinder2]

    #Tubo para cortar el cono gigante, simula en corte que tiene la aprte trasera de la aeronave.
    # Se translada, se rota respecto al eje Z y se escala.
    cylinderNode5 = sg.SceneGraphNode('cylinder2')
    cylinderNode5.transform = tr.matmul([tr.translate(-1.5, 0.5, 0.0), tr.rotationZ(np.pi/2),tr.scale(0.2, 2.0, 0.2)])
    cylinderNode5.childs += [cylinder2]

    #redondela alas3, simula el contorno circular del borde de las alas
    # se translada, se rota respecto al eje Y y se escala.
    cylinderNode6 = sg.SceneGraphNode('cylinder2')
    cylinderNode6.transform = tr.matmul([tr.translate(1.3, 1.8, -3.0), tr.rotationY(np.pi),tr.scale(0.5, 0.1, 0.3)])
    cylinderNode6.childs += [cylinder2]

    #redondela alas4, simula el contorno circular del borde de las alas
    # se translada, se rota respecto al eje Y y se escala.
    cylinderNode7 = sg.SceneGraphNode('cylinder2')
    cylinderNode7.transform = tr.matmul([tr.translate(1.3, 1.8, 3.0), tr.rotationY(np.pi),tr.scale(0.5, 0.1, 0.3)])
    cylinderNode7.childs += [cylinder2]

    #Tubo café1 recto que conecta las alas, se transladan, se rotan respecto al eje Y y se escala.
    cylinderNode8 = sg.SceneGraphNode('cylinder3')
    cylinderNode8.transform = tr.matmul([tr.translate(1.2, 0.8, 3.0), tr.rotationY(np.pi),tr.scale(0.01, 1.0, 0.01)])
    cylinderNode8.childs += [cylinder3]

    #Tubo café2 recto que conecta las alas, se transladan, se rotan respecto al eje Y y se escala.
    cylinderNode9 = sg.SceneGraphNode('cylinder3')
    cylinderNode9.transform = tr.matmul([tr.translate(1.0, 0.8, 3.0), tr.rotationY(np.pi),tr.scale(0.01, 1.0, 0.01)])
    cylinderNode9.childs += [cylinder3]

    #Tubo café3 recto que conecta las alas, se transladan, se rotan respecto al eje Y y se escala.
    cylinderNode10 = sg.SceneGraphNode('cylinder3')
    cylinderNode10.transform = tr.matmul([tr.translate(1.2, 0.8, -3.0), tr.rotationY(np.pi),tr.scale(0.01, 1.0, 0.01)])
    cylinderNode10.childs += [cylinder3]

    #Tubo café4 recto que conecta las alas, se transladan, se rotan respecto al eje Y y se escala.
    cylinderNode11 = sg.SceneGraphNode('cylinder3')
    cylinderNode11.transform = tr.matmul([tr.translate(1.0, 0.8, -3.0), tr.rotationY(np.pi),tr.scale(0.01, 1.0, 0.01)])
    cylinderNode11.childs += [cylinder3]

    #Circulo grande1 enfrente que se translada, se rota respecto el eje Z y se escala.
    cylinderNode12 = sg.SceneGraphNode('cylinder1')
    cylinderNode12.transform = tr.matmul([tr.translate(2.52, 0.5, 0.0),tr.rotationZ(np.pi/2), tr.scale(0.7, 0.0, 0.7)])
    cylinderNode12.childs += [cylinder1]

    #Circulo ala1 arriba del ala que se translada, se rota y se escala.
    cylinderNode13 = sg.SceneGraphNode('cylinder1')
    cylinderNode13.transform = tr.matmul([tr.translate(1.3, 1.905, 2.3),tr.rotationY(np.pi/2), tr.scale(0.5, 0.0, 0.5)])
    cylinderNode13.childs += [cylinder1]

    #Circulo ala2 arriba del ala que se translada, se rota y se escala.
    cylinderNode14 = sg.SceneGraphNode('cylinder1')
    cylinderNode14.transform = tr.matmul([tr.translate(1.3, 1.905, -2.3),tr.rotationY(np.pi/2), tr.scale(0.5, 0.0, 0.5)])
    cylinderNode14.childs += [cylinder1]

    #Persona que maneja la avioneta. Se translada, se rota respecto al eje Z y se escala.
    cylinderNode15 = sg.SceneGraphNode('cylinder1')
    cylinderNode15.transform = tr.matmul([tr.translate(1.0, 1.3, 0.0),tr.rotationZ(np.pi/2), tr.scale(0.25, 0.0, 0.25)])
    cylinderNode15.childs += [cylinder1]

    #Tubo café5 diagonal que conecta las alas, se transladan, se rotan respecto al eje Y y se escala.
    cylinderNode16 = sg.SceneGraphNode('cylinder3')
    cylinderNode16.transform = tr.matmul([tr.translate(1.5, 1.3, 1.2), tr.rotationX(np.pi/4),tr.scale(0.01, 0.8, 0.01)])
    cylinderNode16.childs += [cylinder3]

    #Tubo café6 diagonal que conecta las alas, se transladan, se rotan respecto al eje Y y se escala.
    cylinderNode17 = sg.SceneGraphNode('cylinder3')
    cylinderNode17.transform = tr.matmul([tr.translate(1.2, 1.3, 1.2), tr.rotationX(np.pi/4),tr.scale(0.01, 0.8, 0.01)])
    cylinderNode17.childs += [cylinder3]

    #Tubo café7 diagonal que conecta las alas, se transladan, se rotan respecto al eje Y y se escala.
    cylinderNode18 = sg.SceneGraphNode('cylinder3')
    cylinderNode18.transform = tr.matmul([tr.translate(1.2, 1.3, -1.2), tr.rotationX(-np.pi/4),tr.scale(0.01, 0.8, 0.01)])
    cylinderNode18.childs += [cylinder3]

    #Tubo café8 diagonal que conecta las alas, se transladan, se rotan respecto al eje Y y se escala.
    cylinderNode19 = sg.SceneGraphNode('cylinder3')
    cylinderNode19.transform = tr.matmul([tr.translate(1.5, 1.3, -1.2), tr.rotationX(-np.pi/4),tr.scale(0.01, 0.8, 0.01)])
    cylinderNode19.childs += [cylinder3]

    #Circunferencia1 simula las mini alas semicircunferenciales de la avioneta original.
    # Se translada, se rota respecto al eje Y y se escala.
    cylinderNode20 = sg.SceneGraphNode('cylinder5')
    cylinderNode20.transform = tr.matmul([tr.translate(-3.405, 0.5, 0.0), tr.rotationY(np.pi/2),tr.scale(0.5, 0.0, 0.1)])
    cylinderNode20.childs += [cylinder5]

    #Circunferencia2 vertical, simula la semicircunferencia blanca de la avioneta original.
    # Se translada, se rota respecto al eje X y se escala.
    cylinderNode21 = sg.SceneGraphNode('cylinder4')
    cylinderNode21.transform = tr.matmul([tr.translate(-3.2, 0.7, 0.0), tr.rotationX(np.pi/2),tr.scale(0.3, 0.0, 0.2)])
    cylinderNode21.childs += [cylinder4]

    #Soporte hélice, se translada, se rota respecto al eje Y y se escala.
    cylinderNode22 = sg.SceneGraphNode('cylinder1')
    cylinderNode22.transform = tr.matmul([tr.translate(2.52, 0.5, 0.0),tr.rotationZ(np.pi/2), tr.scale(0.1, 0.08, 0.1)])
    cylinderNode22.childs += [cylinder1]

    #Hélice de la avioneta, se translada, se rota repecto al eje Y y se escala.
    cylinderNode23 = sg.SceneGraphNode('cylinder1')
    cylinderNode23.transform = tr.matmul([tr.translate(2.62, 0.5, 0.0), tr.rotationY(np.pi/2),tr.scale(0.5, 0.0, 0.05)])
    cylinderNode23.childs += [cylinder1]

    #Triángulo rueda1 color café que se transladan, se rotan respecto al eje X y se escalan.
    coneNode = sg.SceneGraphNode('cone')
    coneNode.transform = tr.matmul([tr.translate(1.0, -0.6, 0.4) , tr.scale(0.4, 0.4, 0.0), tr.rotationX(np.pi)])
    coneNode.childs += [cone]

    #Triángulo rueda2 color café que se transladan, se rotan respecto al eje X y se escalan.
    coneNode1 = sg.SceneGraphNode('cone')
    coneNode1.transform = tr.matmul([tr.translate(1.0, -0.6, -0.4) , tr.scale(0.4, 0.4, 0.0), tr.rotationX(np.pi)])
    coneNode1.childs += [cone]

    #Cono gigante que simula el cuerpo de la avioneta, se translada, se rota respecto al eje Z y se escala.
    coneNode2 = sg.SceneGraphNode('cone1')
    coneNode2.transform = tr.matmul([tr.translate(-0.5, 0.5, 0.0), tr.rotationZ(np.pi/2), tr.scale(1.0, 3.0, 1.0)])
    coneNode2.childs += [cone1]

    #Triángulo cola, simula el ala vertical que está debajo en la cola.
    # Se translada, se escala y se rota respecto al eje Z.
    coneNode3 = sg.SceneGraphNode('cone2')
    coneNode3.transform = tr.matmul([tr.translate(-3.3, 0.4, 0.0) , tr.scale(0.2, 0.2, 0.0), tr.rotationZ(-np.pi/2)])
    coneNode3.childs += [cone2]

    scene = sg.SceneGraphNode('system')
    scene.childs += [coneNode]
    scene.childs += [coneNode1]
    scene.childs += [coneNode2]
    scene.childs += [coneNode3]
    scene.childs += [cubeNode]
    scene.childs += [cubeNode1]
    scene.childs += [cylinderNode]
    scene.childs += [cylinderNode1]
    scene.childs += [cylinderNode2]
    scene.childs += [cylinderNode3]
    scene.childs += [cylinderNode4]
    scene.childs += [cylinderNode5]
    scene.childs += [cylinderNode6]
    scene.childs += [cylinderNode7]
    scene.childs += [cylinderNode8]
    scene.childs += [cylinderNode9]
    scene.childs += [cylinderNode10]
    scene.childs += [cylinderNode11]
    scene.childs += [cylinderNode12]
    scene.childs += [cylinderNode13]
    scene.childs += [cylinderNode14]
    scene.childs += [cylinderNode15]
    scene.childs += [cylinderNode16]
    scene.childs += [cylinderNode17]
    scene.childs += [cylinderNode18]
    scene.childs += [cylinderNode19]
    scene.childs += [cylinderNode20]
    scene.childs += [cylinderNode21]
    scene.childs += [cylinderNode22]
    scene.childs += [cylinderNode23]

    return scene

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "Tarea 2"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline = ls.SimpleGouraudShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    cpuAxis = bs.createAxis(7)
    gpuAxis = es.GPUShape().initBuffers()
    mvpPipeline.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    #NOTA: Aqui creas un objeto con tu escena
    dibujo = createScene(pipeline)

    setPlot(pipeline, mvpPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        setView(pipeline, mvpPipeline)

        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)

        #NOTA: Aquí dibujas tu objeto de escena
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(dibujo, pipeline, "model")
        

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()
    

    glfw.terminate()