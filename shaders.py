import mathLib as ml
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
    
    vt = ml.MxV(vt,ml.MxM(ml.MxM(ml.MxM(vpMatrix, projectionMatrix), viewMatrix), modelMatrix))
    """ vt = vpMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt """

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

    vt = ml.MxV(vt,ml.MxM(ml.MxM(ml.MxM(vpMatrix, projectionMatrix), viewMatrix), modelMatrix))

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
    
    
    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] = -1 * dLight[i]
    intensity = ml.dotProd(normal, dLight)
    
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
    
    normal = ml.MxV(normal, modelMatrix)
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] = -1 * dLight[i]
    intensity = ml.dotProd(normal, dLight)
    
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
    
    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] = -1 * dLight[i]
    intensity = ml.dotProd(normal, dLight)
    
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
    
    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] = -1 * dLight[i]
    intensity = ml.dotProd(normal, dLight)
    
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
    
    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] = -1 * dLight[i]
    intensity = ml.dotProd(normal, dLight)
    
    if intensity <= 0:
        intensity = 0
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    camForward = (camMatrix[0][2],
                  camMatrix[1][2],
                  camMatrix[2][2])
    
    glowAmount = 1-ml.dotProd(normal, camForward)
    
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
    
    normal = ml.MxV(normal, modelMatrix)
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] = -1 * dLight[i]
    intensity = ml.dotProd(normal, dLight)
    
    if intensity <= 0:
        intensity = 0
    
    b = intensity*0.2  
    g = intensity*0.2 
    
    # Valores de r, g, b basados en el espectro del arcoíris
    r = abs(sin(intensity * pi))*2  
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
    
    normal = ml.MxV(normal, modelMatrix)
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] = -1 * dLight[i]
    intensity = ml.dotProd(normal, dLight)
    
    if intensity <= 0:
        intensity = 0
    
    b = intensity/0.2
    g = intensity/0.2
    r = intensity/0.2
    
    camForward = (camMatrix[0][2],
                  camMatrix[1][2],
                  camMatrix[2][2])
    
    
    specular = ml.dotProd(normal, list(camForward)) * 0.5
    
    # Brillo especular
    if specular < 0:
        specular_power = 75 #Cambiar para administrar concentración de brillo
        specular_intensity = (specular ** specular_power)
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
    
    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] = -1 * dLight[i]
    intensity = ml.dotProd(normal, dLight)
    
    if intensity <= 0:
        intensity = 0
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    camForward = (camMatrix[0][2],
                  camMatrix[1][2],
                  camMatrix[2][2])
    
    glowAmount = 1 - ml.dotProd(normal, camForward)
    
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
    
    normal = ml.MxV(normal, modelMatrix)
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = list(dLight)
    
    if normalMap:
        texNormal= normalMap.getColor(tU, tV)
        texNormal = [texNormal[0]*2-1, texNormal[1]*2-1, texNormal[2]*2-1]
        texNormal = ml.normalizeV(texNormal)
        
        bitangent = ml.crossProd(normal, tangent)
        bitangent = ml.normalizeV(bitangent)
        
        tangent = ml.crossProd(normal, bitangent)
        tangent = ml.normalizeV(tangent)
        
        tangentMatrix = [[tangent[0],bitangent[0],normal[0]],
                                  [tangent[1],bitangent[1],normal[1]],
                                  [tangent[2],bitangent[2],normal[2]]]
        
        texNormal = ml.MxV(texNormal, tangentMatrix)
        texNormal = ml.normalizeV(texNormal)
        
        dLight = list(dLight)
        for i in range(len(dLight)):
            dLight[i] = -1 * dLight[i]
        intensity = ml.dotProd(normal, dLight)
        
    else:
        dLight = list(dLight)
        for i in range(len(dLight)):
            dLight[i] = -1 * dLight[i]
        intensity = ml.dotProd(normal, dLight)
    
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

def negativeShader(**kwargs):
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
    
    normal = ml.MxV(normal, modelMatrix)
    normal = [normal[0], normal[1], normal[2]]
    
    dLight = list(dLight)
    for i in range(len(dLight)):
        dLight[i] = -1 * dLight[i]
    intensity = ml.dotProd(normal, dLight)
    
    b *= intensity/0.2
    g *= intensity/0.2
    r *= intensity/0.2
    
    if b>=1.0:b=1.0
    if g>=1.0:g=1.0
    if r>=1.0:r=1.0
    
    if intensity > 0:
        r = 1.0-r
        g = 1.0-g
        b = 1.0-b
        r = max(0.0, min(1.0,r))
        g = max(0.0, min(1.0,g))
        b = max(0.0, min(1.0,b))
        return r,g,b
    else:
        return [0,0,0]