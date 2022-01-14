import os

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import csv
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

ruleList = []
doctrineList = []
from io import BytesIO
class doctrine():
    def __init__(self):
        self.state = ""
        self.condition = {}
        self.action = ""
        self.actionOf = {}
        self.actionParam = {}

# class data():
#     def __init__(self):
#         self.entityList = []
#         self.groupList = []
#         self.ruleList = []
#         self.relationList = []

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
        # self.data = data()

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
        self.pushButton_load.clicked.connect(self.load)

    def load(self):
        global entityList
        global doctrineList
        fileName = QFileDialog.getOpenFileName(self, "Open CSV", "C:\\Users\\JudyL\\work\\simpleUI",
                                               "CSV Files (*.csv)")
        # Opening a file
        file = open(fileName[0], 'r')
        reader = csv.reader(file)
        for line in reader:
            if line[0] == "Entity":
                entityList.append(line)
            elif line[0] == "Rule":
                doctrineList.append(line)

        self.lineEdit_loadedFile.setText(fileName[0])


    def isEntityKeyword(self, item):
        if item == "entity" or item == "airplane" or item == "plane" or item == "stpt" or item == "steerpoint":
            return True
        else:
            return False

    def addDoctrineLine(self):
        dialog = NewRuleDialog()
        dialog.exec()

    def openVisual(self):
        dialog = VisualDialog()
        dialog.exec()

class VisualDialog(QDialog, QGLWidget, sim.Ui_SimDialog ):
    def __init__(self, parent=None):
        super().__init__(parent)

        global entityList
        self.entityList = entityList
        loadUi("sim.ui", self)

        self.connectSignalsSlots()


    def connectSignalsSlots(self):
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_load.clicked.connect(self.open)
        self.pushButton_clear.clicked.connect(self.clear)

    def clear(self):
        global entityList
        entityList.clear()
        self.openGLWidget.update()

    def open(self):
        global entityList
        fileName = QFileDialog.getOpenFileName(self, "Open Image", "C:\\Users\\JudyL\\work\\simpleUI",
                                               "CSV Files (*.csv)")
        # Opening a file
        fileName = open(fileName[0], 'r')
        reader = csv.reader(fileName)
        for line in reader:
            entityList.append(line)

    def save(self):
        fileName = QFileDialog.getSaveFileName(self, "Open Image", "C:\\Users\\JudyL\\work\\simpleUI", "CSV Files (*.csv)")
        # Opening a file
        file1 = open(fileName[0], 'w', newline='')

        print(self.entityList)
        wr = csv.writer(file1)
        wr.writerows(self.entityList)

        file1.close()

class NewRuleDialog(QDialog, newRule.Ui_NewRuleDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("newRule.ui", self)
        # creating a line edit
        edit = QLineEdit(self)

        global doctrineList
        # setting line edit
        self.comboBox_State.setLineEdit(edit)
        self.lineEdit_condition.setText('Match $s isa enemy_element has dist<5')
        self.connectSignalsSlots()
        #self.data = appData
        self.doctrine = doctrineList

        entities = TypeDBClient.queryEntities()
        types, relations = TypeDBClient.parseTql('meamnim_elab.tql')
        print(*entities)
        self.comboBox_actionOf.addItems(entities+types+relations)
        self.comboBox_ActionOn.addItems(entities+types+relations)
        self.tabWidget.setCurrentIndex(0)

        for i in self.doctrine:
            self.listWidget_rules.addItem(i[1])


    def connectSignalsSlots(self):
        self.buttonBox.accepted.connect(self.addRule)
        self.comboBox_actionOf.currentTextChanged.connect(self.queryAttr)
        self.comboBox_attribute.currentTextChanged.connect(self.queryAttr)
        self.radioButton_changeAttr.clicked.connect(self.changeAttr)
        self.radioButton_chooseAction.clicked.connect(self.chooseActionOrDoctrine)
        self.radioButton_chooseDoctrine.clicked.connect(self.chooseActionOrDoctrine)
        self.radioButton_modifyState.clicked.connect(self.modifyState)
        self.pushButton_addRuleToDoc.clicked.connect(self.addRuleToDoc)
        #self.pushButton_saveDoctrine.clicked.connect(self.saveDoctrine)
        #self.pushButton_loadDoctrine.clicked.connect(self.loadDoctrine)
        self.pushButton_clear.clicked.connect(self.clear)
        self.listWidget_rules.currentRowChanged.connect(self.loadRule)

    def clear(self):
        self.listWidget_rules.clear()
        self.doctrine.clear()

    def loadRule(self):
        global doctrineList
        ruleType = ""
        newRule = ["Rule", self.lineEdit_ruleName.text(), self.comboBox_State.currentText(),
                   self.lineEdit_condition.text()]
        if self.radioButton_chooseAction.isChecked():
            ruleType = "Action"
        elif self.radioButton_chooseDoctrine.isChecked():
            ruleType = "Doctrine"
        elif self.radioButton_changeAttr.isChecked():
            ruleType = "Attribute"
        elif self.radioButton_modifyState.isChecked():
            ruleType = "State"

        if ruleType == "Action" or ruleType == "Doctrine":
            if self.radioButton_selectEntity.isChecked():
                newRule.append(self.comboBox_ActionOn.currentText())
            elif self.radioButton_insertQuery.isChecked():
                newRule.append(self.lineEdit_matchActionOfEntity)
        elif ruleType == "Attribute":
            newRule.append(self.comboBox_attribute.currentText())
            newRule.append(self.lineEdit_attrOldVal.text())
            newRule.append(self.lineEdit_attrNewVal.text())

        if self.radioButton_selectEnt.isChecked():
            ent = self.comboBox_actionOf.currentText()
        elif self.radioButton_insertQuery.isChecked():
            ent = self.lineEdit_matchActionOfEntity.text()

        newRule.append(ruleType)
        newRule.append(ent)

        self.doctrine.append(newRule)
        self.listWidget_rules.addItem(self.lineEdit_ruleName.text())
        print(newRule)

    # def saveDoctrine(self):
    #     fileName = QFileDialog.getSaveFileName(self, "Open Image", "C:\\Users\\JudyL\\work\\simpleUI", "CSV Files (*.csv)")
    #     # Opening a file
    #     file1 = open(fileName[0], 'a', newline='')
    #
    #     print(self.doctrine)
    #     wr = csv.writer(file1)
    #     wr.writerows(self.doctrine)
    #
    #     file1.close()
    def addRuleToDoc(self):
        global doctrineList
        ruleType = ""
        newRule = ["Rule", self.lineEdit_ruleName.text(), self.comboBox_State.currentText(),
                   self.lineEdit_condition.text()]
        if self.radioButton_chooseAction.isChecked():
            ruleType = "Action"
        elif self.radioButton_chooseDoctrine.isChecked():
            ruleType = "Doctrine"
        elif self.radioButton_changeAttr.isChecked():
            ruleType = "Attribute"
        elif self.radioButton_modifyState.isChecked():
            ruleType = "State"

        if ruleType == "Action" or ruleType == "Doctrine":
            if self.radioButton_selectEntity.isChecked():
                newRule.append(self.comboBox_ActionOn.currentText())
            elif self.radioButton_insertQuery.isChecked():
                newRule.append(self.lineEdit_matchActionOfEntity)
        elif ruleType == "Attribute":
            newRule.append(self.comboBox_attribute.currentText())
            newRule.append(self.lineEdit_attrOldVal.text())
            newRule.append(self.lineEdit_attrNewVal.text())

        if self.radioButton_selectEnt.isChecked():
            ent = self.comboBox_actionOf.currentText()
        elif self.radioButton_insertQuery.isChecked():
            ent = self.lineEdit_matchActionOfEntity.text()

        newRule.append(ruleType)
        newRule.append(ent)

        self.doctrine.append(newRule)
        self.listWidget_rules.addItem(self.lineEdit_ruleName.text())
        print (newRule)

    def modifyState(self):
        self.tabWidget.hide()
    def chooseActionOrDoctrine(self):
        self.tabWidget.show()
        self.tabWidget.setCurrentIndex(0)
    def addRule(self):
        global doctrineList
        doctrineList = self.doctrine

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
