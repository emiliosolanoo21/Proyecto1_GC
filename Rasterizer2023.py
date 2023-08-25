from gl import Renderer, Model
import shaders

# El tama�o del FrameBuffer
width = 960
height = 540


# Se crea el renderizador
rend = Renderer(width, height)

rend.glClearColor(0.1,0.1,0.1)
rend.glClear()

""" #Delimitacion del viewport
rend.glViewPort(width/4, height/4, width/2, height/2) """

#Background
rend.glBackgroundTexture("background\desk.bmp")
rend.glClearBackground()

""" rend.directionalLight = (0,0,-1) """

# Cargamos los modelos que rederizaremos
bracelet = Model("models/bracelet.obj",
              translate = (1.15,0,-7),
              rotate= (90,0,-1),
              scale = (0.15,0.15,0.15))
bracelet.LoadTexture("textures/bracelet.bmp")
bracelet.LoadNormalMap("textures/braceletNormal.bmp")
bracelet.SetShaders(shaders.vertexShader, shaders.normalMapShader)

hand = Model("models/hand.obj",
              translate = (1,-2.05,-5),
              rotate= (-50,75,150),
              scale = (0.15,0.15,0.15))
hand.LoadTexture("textures/skin.bmp")
hand.SetShaders(shaders.vertexShader, shaders.gouradShader)

axe = Model("models/axe.obj",
              translate = (4,6,-7),
              rotate= (0,0,120),
              scale = (3.5,3.5,3.5))
axe.LoadTexture("textures/axe.bmp")
axe.LoadNormalMap("textures/axeNormal.bmp")
axe.SetShaders(shaders.vertexShader, shaders.normalMapShader)


rend.glAddModel(hand)
rend.glAddModel(bracelet)
rend.glAddModel(axe)

# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("output.bmp")
