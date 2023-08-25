from gl import Renderer, Model
import shaders

# El tama�o del FrameBuffer
width = 960
height = 540


# Se crea el renderizador
rend = Renderer(width, height)

rend.glClearColor(0.1,0.1,0.1)
rend.glClear()

#Delimitacion del viewport
rend.glViewPort(width/4, height/4, width/2, height/2)

#Background
rend.glBackgroundTexture("textures\wood.bmp")
rend.glClearBackground()


rend.directionalLight = (0,0,-1)

# Cargamos los modelos que rederizaremos
model1 = Model("models\model.obj",
              translate = (-1,0,-5),
              scale = (1.5,1.5,1.5))
model1.LoadTexture("textures\model.bmp")
""" model1.LoadNormalMap("textures\model_normal.bmp") """
model1.SetShaders(shaders.vertexShader, shaders.normalMapShader)

model2 = Model("models\model.obj",
              translate = (1,0,-5),
              scale = (1.5,1.5,1.5))
model2.LoadTexture("textures\model.bmp")
model2.SetShaders(shaders.vertexShader, shaders.gouradShader)

rend.glAddModel(model1)
rend.glAddModel(model2)

# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("output.bmp")
