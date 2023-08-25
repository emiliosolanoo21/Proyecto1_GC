import random
import numpy as np
from math import sin, pi

#-----------------------------------------------------
#Shaders para vertices
def vertexShader(vertex, **kwargs):
    
    # El Vertex Shader se lleva a cabo por cada v�rtice

    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    vpMatrix = kwargs["vpMatrix"]

    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

    vt = vpMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt

    vt = vt.tolist()[0]

    vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

    return vt

def fatShader(vertex, **kwargs):
    # El Vertex Shader se lleva a cabo por cada v�rtice

    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    vpMatrix = kwargs["vpMatrix"]
    normal = kwargs["normal"]
    
    blowAmount = 0.2

    vt = [vertex[0] + (normal[0]*blowAmount),
          vertex[1] + (normal[1]*blowAmount),
          vertex[2] + (normal[2]*blowAmount),
          1]

    vt = vpMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt

    vt = vt.tolist()[0]

    vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

    return vt

#-----------------------------------------------------
#Shaders para textura
def fragmentShader(**kwargs):

    # El Fragment Shader se lleva a cabo por cada pixel
    # que se renderizar� en la pantalla.
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    u, v, w = kwargs["bCoords"]

    b=1.0
    g=1.0
    r=1.0
    
    if texture != None:
        
        tU = u*tA[0] + v*tB[0] + w*tC[0]
        tV = u*tA[1] + v*tB[1] + w*tC[1]
        
        textureColor = texture.getColor(tU, tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]

    return r,g,b

def flatShader(**kwargs):
    dLight = kwargs["dLight"]
    normal = kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    
    b=1.0
    g=1.0
    r=1.0
    
    if texture != None:
        textureColor = texture.getColor(texCoords[0], texCoords[1])
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]
    
    
    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    if intensity > 0:
        return r,g,b
    else:
        return [0,0,0]

def gouradShader(**kwargs):
    dLight = kwargs["dLight"]
    nA, nB, nC = kwargs["normals"]
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    u, v, w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]
    
    b=1.0
    g=1.0
    r=1.0
    
    if texture != None:
        
        tU = u*tA[0] + v*tB[0] + w*tC[0]
        tV = u*tA[1] + v*tB[1] + w*tC[1]
        
        textureColor = texture.getColor(tU, tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]
    
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2],
              0]
    
    normal = modelMatrix @ normal
    normal = normal.tolist()[0]
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)
    
    b *= intensity/0.2
    g *= intensity/0.2
    r *= intensity/0.2
    
    if b>=1.0:b=1.0
    if g>=1.0:g=1.0
    if r>=1.0:r=1.0
    
    if intensity > 0:
        return r,g,b
    else:
        return [0,0,0]

def toonShader(**kwargs):
    dLight = kwargs["dLight"]
    nA, nB, nC = kwargs["normals"]
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    u, v, w = kwargs["bCoords"]
    
    b=1.0
    g=1.0
    r=1.0
    
    if texture != None:
        
        tU = u*tA[0] + v*tB[0] + w*tC[0]
        tV = u*tA[1] + v*tB[1] + w*tC[1]
        
        textureColor = texture.getColor(tU, tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]
    
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)
    
    if intensity <= 0.25:
        intensity = 0.2
    elif intensity <= 0.5:
        intensity = 0.45
    elif intensity <= 0.75:
        intensity = 0.7
    elif intensity <= 1.0:
        intensity = 0.95
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    if intensity > 0:
        return r,g,b
    else:
        return [0,0,0]

def redShader(**kwargs):
    dLight = kwargs["dLight"]
    nA, nB, nC = kwargs["normals"]
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    u, v, w = kwargs["bCoords"]
    
    b=1.0
    g=1.0
    r=1.0
    
    if texture != None:
        
        tU = u*tA[0] + v*tB[0] + w*tC[0]
        tV = u*tA[1] + v*tB[1] + w*tC[1]
        
        textureColor = texture.getColor(tU, tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]
    
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    red = (1,0,0)
    
    b *= red[2]
    g *= red[1]
    r *= red[0]
    
    if intensity > 0:
        return r,g,b
    else:
        return [0,0,0]

def yellowGlowShader(**kwargs):
    dLight = kwargs["dLight"]
    nA, nB, nC = kwargs["normals"]
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    u, v, w = kwargs["bCoords"]
    camMatrix = kwargs["camMatrix"]
    
    b=1.0
    g=1.0
    r=1.0
    
    if texture != None:
        
        tU = u*tA[0] + v*tB[0] + w*tC[0]
        tV = u*tA[1] + v*tB[1] + w*tC[1]
        
        textureColor = texture.getColor(tU, tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]
    
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)
    
    if intensity <= 0:
        intensity = 0
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    camForward = (camMatrix.item(0,2),
                  camMatrix.item(1,2),
                  camMatrix.item(2,2))
    
    glowAmount = 1-np.dot(normal, camForward)
    
    if glowAmount <= 0: 
        glowAmount = 0
    
    yellow = (1,1,0)
    
    b += glowAmount*yellow[2]
    g += glowAmount*yellow[1]
    r += glowAmount*yellow[0]
    
    if b>=1.0:
        b = 1.0
    if g>=1.0:
        g = 1.0
    if r>=1.0:
        r = 1.0
    
    return r,g,b

#Nuevos shaders
def darkRedShader(**kwargs):
    dLight = kwargs["dLight"]
    nA, nB, nC = kwargs["normals"]
    u, v, w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]
    
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2],
              0]
    
    normal = modelMatrix @ normal
    normal = normal.tolist()[0]
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)
    
    if intensity <= 0:
        intensity = 0
    
    b = intensity  
    g = intensity  
    
    # Valores de r, g, b basados en el espectro del arcoíris
    r = abs(sin(intensity * pi))  
    r = max(0, min(1, r))
    
    return r, g, b

def bnWShader(**kwargs):
    dLight = kwargs["dLight"]
    nA, nB, nC = kwargs["normals"]
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    u, v, w = kwargs["bCoords"]
    camMatrix = kwargs["camMatrix"]
    modelMatrix = kwargs["modelMatrix"]
    
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2],
              0]
    
    normal = modelMatrix @ normal
    normal = normal.tolist()[0]
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)
    
    if intensity <= 0:
        intensity = 0
    
    b = intensity  
    g = intensity  
    r = intensity  
    
    camForward = (camMatrix.item(0, 2),
                  camMatrix.item(1, 2),
                  camMatrix.item(2, 2))
    
    specular = np.dot(np.array(normal), np.array(camForward))
    
    # Brillo especular
    if specular > 0:
        specular_power = 32  #Cambiar para administrar concentración de brillo
        specular_intensity = (specular ** specular_power) * 0.5
        r += specular_intensity
    

    if texture != None:
        tU = u*tA[0] + v*tB[0] + w*tC[0]
        tV = u*tA[1] + v*tB[1] + w*tC[1]
        textureColor = texture.getColor(tU, tV)
        b *= textureColor[2]
        g *= textureColor[1]
        r *= textureColor[0]
    
    return r, g, b

def darkGlowShader(**kwargs):
    dLight = kwargs["dLight"]
    nA, nB, nC = kwargs["normals"]
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    u, v, w = kwargs["bCoords"]
    camMatrix = kwargs["camMatrix"]
    
    b=1.0
    g=1.0
    r=1.0
    
    if texture != None:
        
        tU = u*tA[0] + v*tB[0] + w*tC[0]
        tV = u*tA[1] + v*tB[1] + w*tC[1]
        
        textureColor = texture.getColor(tU, tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]
    
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
    dLight = np.array(dLight)
    intensity = np.dot(normal, -dLight)
    
    if intensity <= 0:
        intensity = 0
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    camForward = (camMatrix.item(0,2),
                  camMatrix.item(1,2),
                  camMatrix.item(2,2))
    
    glowAmount = 1 - np.dot(normal, camForward)
    
    if glowAmount <= 0: 
        glowAmount = 0
    
    white = (1,1,1)
    
    b *= glowAmount+white[2]
    g *= glowAmount+white[1]
    r *= glowAmount+white[0]
    
    if b>=1.0:
        b = 1.0
    if g>=1.0:
        g = 1.0
    if r>=1.0:
        r = 1.0
    
    return r,g,b

#-----------------------------------------------------
#Shaders para aplicar mapa normal
def normalMapShader(**kwargs):
    dLight = kwargs["dLight"]
    normalMap = kwargs["normalMap"]
    nA, nB, nC = kwargs["normals"]
    tA, tB, tC = kwargs["texCoords"]
    texture = kwargs["texture"]
    u, v, w = kwargs["bCoords"]
    modelMatrix = kwargs["modelMatrix"]
    tangent = kwargs["tangent"]
    
    b=1.0
    g=1.0
    r=1.0
    
    tU = u*tA[0] + v*tB[0] + w*tC[0]
    tV = u*tA[1] + v*tB[1] + w*tC[1]
    
    if texture != None:
        
        textureColor = texture.getColor(tU, tV)
        b*=textureColor[2]
        g*=textureColor[1]
        r*=textureColor[0]
    
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2],
              0]
    
    normal = modelMatrix @ normal
    normal = normal.tolist()[0]
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = np.array(dLight)
    
    if normalMap:
        texNormal= normalMap.getColor(tU, tV)
        texNormal = [texNormal[0]*2-1, texNormal[1]*2-1, texNormal[2]*2-1]
        texNormal = texNormal / np.linalg.norm(texNormal)
        
        bitangent = np.cross(normal, tangent)
        bitangent = bitangent / np.linalg.norm(bitangent)
        
        tangent = np.cross(normal, bitangent)
        tangent = tangent / np.linalg.norm(tangent)
        
        tangentMatrix = np.matrix([[tangent[0],bitangent[0],normal[0]],
                                  [tangent[1],bitangent[1],normal[1]],
                                  [tangent[2],bitangent[2],normal[2]]])
        
        texNormal = tangentMatrix @ texNormal
        texNormal = texNormal.tolist()[0]
        texNormal = texNormal / np.linalg.norm(texNormal)
        
        intensity = intensity = np.dot(texNormal, -dLight)
        
    else:
        intensity = np.dot(normal, -dLight)
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    if b>=1.0:b=1.0
    if g>=1.0:g=1.0
    if r>=1.0:r=1.0
    
    if intensity > 0:
        return r,g,b
    else:
        return [0,0,0]

