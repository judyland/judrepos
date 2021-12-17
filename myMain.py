import os

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

#
import main
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog, QComboBox, QLineEdit, QLabel)
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

#import nltk
#from nltk.tokenize import sent_tokenize, word_tokenize

from sim2d import *
import newRule
import sim
import addEntity


from io import BytesIO
class doctrine():
    def __init__(self):
        self.state = ""
        self.condition = {}
        self.action = ""
        self.actionOf = {}
        self.actionParam = {}

class data():
    def __init__(self):
        self.entityList = []
        self.groupList = []
        self.ruleList = []
        self.relationList = []

class simData():
    def __init__(self):
        self.frame = 0
        self.positionList = []

class ExampleApp(QtWidgets.QMainWindow, main.Ui_MainWindow, newRule.Ui_NewRuleDialog, addEntity.Ui_addEntityDialog):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)

        self.connectSignalsSlots()
        self.doctrineList = []
        self.data = data()
        global entityList
        entityList = []

        myImage = QImage()
        myImage.load("formation.jpeg")

        myLabel = self.label_ui
        myLabel.setAlignment(Qt.AlignCenter)
        # myLabel.setLayout(self.verticalLayout)
        myLabel.setPixmap(QPixmap.fromImage(myImage))

        myLabel.show()
    #
    def connectSignalsSlots(self):
        self.pushButton_openRules.clicked.connect(self.addDoctrineLine)
        self.pushButton_openEntities.clicked.connect(self.openVisual)

    def isEntityKeyword(self, item):
        if item == "entity" or item == "airplane" or item == "plane" or item == "stpt" or item == "steerpoint":
            return True
        else:
            return False

    def addDoctrineLine(self):

        dialog = NewRuleDialog(self.data.ruleList)
        dialog.exec()

        print(self.data.ruleList)

    def openVisual(self):
        dialog = VisualDialog()
        dialog.exec()

class VisualDialog(QDialog, QGLWidget, sim.Ui_SimDialog ):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("sim.ui", self)

        self.connectSignalsSlots()



    def connectSignalsSlots(self):
        self.pushButton_save.clicked.connect(self.save)

    def save(self):
        self.close()

class NewRuleDialog(QDialog, newRule.Ui_NewRuleDialog):
    def __init__(self, appData, parent=None):
        super().__init__(parent)
        loadUi("newRule.ui", self)
        # creating a line edit
        edit = QLineEdit(self)

        # setting line edit
        self.comboBox_State.setLineEdit(edit)
        self.lineEdit_condition.setText('Match $s isa enemy_element has dist<5')
        self.connectSignalsSlots()
        self.data = appData

        entities = TypeDBClient.queryEntities()
        types, relations = TypeDBClient.parseTql('meamnim_elab.tql')
        print(*entities)
        self.comboBox_actionOf.addItems(entities+types+relations)
        self.comboBox_ActionOn.addItems(entities+types+relations)
        self.tabWidget.setCurrentIndex(0)


    def connectSignalsSlots(self):
        self.buttonBox.accepted.connect(self.addRule)
        self.comboBox_actionOf.currentTextChanged.connect(self.queryAttr)
        self.comboBox_attribute.currentTextChanged.connect(self.queryAttr)
        self.radioButton_changeAttr.clicked.connect(self.changeAttr)
        self.radioButton_chooseAction.clicked.connect(self.chooseActionOrDoctrine)
        self.radioButton_chooseDoctrine.clicked.connect(self.chooseActionOrDoctrine)
        self.radioButton_modifyState.clicked.connect(self.modifyState)
    def modifyState(self):
        self.tabWidget.hide()
    def chooseActionOrDoctrine(self):
        self.tabWidget.show()
        self.tabWidget.setCurrentIndex(0)
    def addRule(self):
        self.rule = []
        self.rule.append(self.comboBox_State.currentText())
        self.rule.append(self.lineEdit_condition.text())
        if self.radioButton_chooseDoctrine.isChecked():
            self.rule.append(self.comboBox_Doctrine.currentText())
        elif self.radioButton_chooseAction.isChecked():
            self.rule.append(self.comboBox_Action_2)


        self.rule.append(self.comboBox_actionOf.currentText())
        self.rule.append(self.lineEdit_matchActionOfEntity.text())
        self.data.append(self.rule)

    def queryAttr(self):
        attrs = TypeDBClient.queryAttr(self.comboBox_actionOf.currentText(), self.comboBox_attribute.currentText())
        print(attrs)
        self.lineEdit_attrOldVal.setText(str(attrs))

    def changeAttr(self):
        self.tabWidget.show()
        self.tabWidget.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
