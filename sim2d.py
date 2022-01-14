

import numpy as np
import time
from numpy import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from PyQt5.QtGui import QPalette, QPixmap, QImage, QPainter
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog, QComboBox, QLineEdit, QOpenGLWidget)
from PyQt5.uic import loadUi

import TypeDBClient
import addEntity
from TypeDBClient import *
from PIL import ImageGrab

entityList = []

class object():
    def __init__(self):
        w = 0
        h = 0
        imdata = 0

class OGLWidget(QOpenGLWidget):
    def initializeGL(self,):
        self.texture = None
        self.h = 0
        self.w = 0
        self.imdata = 0
        self.texture = []
        self.plane = object()
        self.planefoe = object()
        self.missile = object()
        data = self.window().size()
        self.dataorder = []
        self.window().move(0,0)
        # self.entityList = []
        self.areas = []
        #glClearColor(0,0, 0,0)

        gluOrtho2D(-1, 1, -1, 1)
        #glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)

        # #gen texture and make current
        self.texture = glGenTextures(3)
        glBindTexture(GL_TEXTURE_2D, self.texture[0])

        # texture mode and parameters controlling wrapping and scaling
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameterf(
            GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(
            GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(
            GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(
            GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)


        #load image

        # planefoe = Image.open("planefoe2.png")

        im = Image.open("northISR1.jpg")
        airplane = Image.open("plane36.png")

        # self.image = QImage("plane36.png");
        # self.painter = QPainter(self.image)
        #missile = Image.open("missile.png")

       # faux_file = BytesIO()
        #airplane.save(faux_file, 'png')

        self.w, self.h, self.imdata = im.size[0], im.size[1], im.tobytes("raw", "RGB", 0, -1)
        self.plane.w, self.plane.h, self.plane.imdata = airplane.size[0], airplane.size[1], airplane.tobytes("raw", "RGBA", 0, -1)

        #print(self.plane.w, self.plane.h)
        #self.missile.w, self.missile.h, self.missile.imdata = missile.size[0], missile.size[1], missile.tobytes("raw", "RGBA", 0, -1)

        #self.planefoe.w, self.planefoe.h, self.planefoe.imdata = planefoe.size[0], planefoe.size[1], planefoe.tobytes("raw", "RGBA", 0, -1)                                                                             "RGBA", 0,                                                                                                           -1
        # self.planefoe.w, self.planefoe.h, self.planefoe.imdata = planefoe.size[0], planefoe.size[1], planefoe.tobytes("raw", "RGBA", 0, -1)

        #imdata = np.fromstring(image.tostring(), np.uint8)
        # map the image data to the texture. note that if the input
        # type is GL_FLOAT, the values must be in the range [0..1]
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.w, self.h, 0,
                        GL_RGB, GL_UNSIGNED_BYTE, self.imdata)

        glBindTexture(GL_TEXTURE_2D, self.texture[1])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, self.plane.w, self.plane.h, 0,
                        GL_RGBA, GL_UNSIGNED_BYTE, self.plane.imdata)

        glGenerateMipmap(GL_TEXTURE_2D)
        #
        # glBindTexture(GL_TEXTURE_2D, self.texture[2])
        # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, self.planefoe.w, self.planefoe.h, 0,
        #                 GL_RGBA, GL_UNSIGNED_BYTE, self.planefoe.imdata)
        #
        # glGenerateMipmap(GL_TEXTURE_2D)

        # glBindTexture(GL_TEXTURE_2D, self.texture[2])
        # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.missile.w, self.missile.h, 0,
        #                  GL_RGBA, GL_UNSIGNED_BYTE, self.missile.imdata)
        # glGenerateMipmap(GL_TEXTURE_2D)

        # self.x = np.load('Sim_List.npy')
        # print(self.x)
        # tu = 0
        # self.dataorder = ["EntityId", "XPos", "YPos", "Heading", "ShootingAt", "MainTarget", "IsFoe", "TU"]
        # self.x = self.x[:1000]
        # self.y = self.x[..., len(self.dataorder)-1]
        #
        # self.z = np.split(self.x, np.where(np.diff(self.y))[0]+1)

        self.setMouseTracking(True)
        self.firstRun = True
        #self.paintMap()

    def mousePressEvent(self, event):
        #print ('mouseMoveEvent: x=%d, y=%d' % (event.x(), event.y()))
        self.beginX = event.x()
        self.beginY = event.y()


        # entities = TypeDBClient.queryEntities()
        # print(*entities)
        # # open new entity ui
        # posX = event.x() / self.width()
        # posY = (self.height() - event.y() )/ self.height()
        # dialog = newEntityDialog(entities, posX, posY, self.texture, self.entityList)
        # dialog.exec()
    def mouseReleaseEvent(self, event):
        #print ('mouseReleaseEvent: x=%d, y=%d' % (event.x(), event.y()))
        self.endX = event.localPos().x()
        self.endY = event.localPos().y()
       # print(event.localPos().x(), event.localPos().y(), event.x(), event.y())
        # if (self.endY - self.beginY > 0) or (self.endX - self.endX > 0):
        #     #add to areas list
        #     self.areas.append(self.beginX, self.beginY, self.endX, self.endY)     #bottom left + top right
        #     #print("square: " + str(self.endY) + str(self.beginY) + str(self.endX) + str(self.beginX))
        entities = TypeDBClient.queryEntities()
        entities, relations = TypeDBClient.parseTql('meamnim_elab.tql')
        # print(*entities)
        # open new entity ui
        posX = self.endX / self.width()
        posY = (self.height() - self.endY )/ self.height()
        dialog = newEntityDialog(entities, relations, posX, posY, self.texture)
        dialog.exec()
    def resizeGL(self, w, h):
        glViewport(0,0,w,h)
#        glClear()
    def paintGL(self):
        # if self.firstRun == True:
        #     self.paintMap()
        #     firstRun = False
        self.paintMap()
        self.paintEntities()

    def paintEntities(self):

        #print("paintEntities")
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        global entityList
        # entityList = self.entityList
        # print(entityList)

        for i in entityList:
            #print("painting entity " + i["name"])
            #print("painting entity " + i["name"])
            # posx = i["posX"]
            # posy = i["posY"]
            # heading = i["heading"]
            posx = i[1]
            posy = i[2]
            heading = i[3]


            glEnable(GL_TEXTURE_2D)

            # if i[self.dataorder.index("IsFoe")] == 1:
            #     # bind foe air plane texture
            #     glBindTexture(GL_TEXTURE_2D, self.texture[2])
            # else:
            # bind air plane texture
            glBindTexture(GL_TEXTURE_2D, self.texture[1])

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glTexParameterf(
                GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)

            size = 0.05
            # draw a quad

            # draw a quad
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()

            glOrtho(0, 1, 0, 1, -1000, 1000)
            #gluOrtho2D(0, 1, 0, 1)
            halfsize = size / 2

            glTranslate(float(posx), float(posy),1)
            glRotate(float(heading), 0, 0, 1)

            glBegin(GL_QUADS)
            glTexCoord2f(0, 1)
            glVertex2f(-halfsize, halfsize)
            glTexCoord2f(0, 0)
            glVertex2f(-halfsize, -halfsize)
            glTexCoord2f(1, 0)
            glVertex2f(halfsize, -halfsize)
            glTexCoord2f(1, 1)
            glVertex2f(halfsize, halfsize)
            glEnd()
            glFlush()

            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
            glDisable(GL_TEXTURE_2D)

    def paintMap(self):

        sizex = self.window().size().width()*2
        sizey = self.window().size().height()*2

        #print(sizex, sizey)
        #glViewport(0, 0, sizex, sizey)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glOrtho(0, 1, 0, 1, -1000, 1000)
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        # # enable textures, bind to our texture
        glEnable(GL_TEXTURE_2D)

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glBindTexture(GL_TEXTURE_2D, self.texture[0])
        #glColor3f(1, 1, 0)
        # draw a quad
        glTranslate(0, 0, -1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0, 0, 1)
        glTexCoord2f(1, 0)
        glVertex3f(1, 0, 1)
        glTexCoord2f(1, 1)
        glVertex3f(1, 1, 1)
        glTexCoord2f(0, 1)
        glVertex3f(0, 1, 1)
        glEnd()
        glFlush()

    def onDraw(self):
        """draw function """
        # self.context().makeCurrent()

        self.paintGL()
        # swap the front and back buffers so that the texture is visible

        #self.context().swapBuffers()

class newEntityDialog(QDialog, addEntity.Ui_addEntityDialog):
    def __init__(self, entities, relations, posX, posY, texture, parent=None):
        super().__init__(parent)
        loadUi("addEntity.ui", self)

        self.posX = posX
        self.posY = posY
        self.comboBox_entities.addItems(entities)
        self.comboBox_entities.addItems(relations)
        self.lineEdit_locationX.setText(str(posX))
        self.lineEdit_locationY.setText(str(posY))
        self.connectSignalsSlots()
        self.texture = texture
        self.checkBox_isAlive.setChecked(True)
        self.lineEdit_Orientation.setText('0')
        # global entityList
        # self.entityList = entityList

    def connectSignalsSlots(self):
        self.buttonBox.accepted.connect(self.addEntity)
        self.comboBox_entities.currentTextChanged.connect(self.sourceEntChange)


    def addEntity(self):
        # newEntity = {
        # "posX" : self.lineEdit_locationX.text(),
        # "posY" : self.lineEdit_locationY.text(),
        # "heading" : self.lineEdit_Orientation.text(),
        # "name" : self.lineEdit_name.text(),
        # "isAlive" :  self.checkBox_isAlive.checkState(),
        # "action" : self.comboBox_action.currentText()}
        # self.entityList.append(newEntity)

        newEntity = [
        "Entity",
        self.lineEdit_locationX.text(),
        self.lineEdit_locationY.text(),
        self.lineEdit_Orientation.text(),
        self.lineEdit_name.text(),
        self.checkBox_isAlive.checkState(),
        self.comboBox_action.currentText()]
        # self.entityList.append(newEntity)
        global entityList
        entityList.append(newEntity)
        # print(entityList)
        #print ("added entity with name " + self.lineEdit_name.text())

    def sourceEntChange(self):
        self.lineEdit_name.setText(self.comboBox_entities.currentText() + "_new")



