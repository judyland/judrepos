# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(633, 526)
        self.widget = QtWidgets.QWidget(MainWindow)
        self.widget.setGeometry(QtCore.QRect(10, 64, 611, 451))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_ui = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Baskerville")
        font.setPointSize(24)
        self.label_ui.setFont(font)
        self.label_ui.setText("")
        self.label_ui.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ui.setObjectName("label_ui")
        self.verticalLayout.addWidget(self.label_ui)
        self.pushButton_openTQL = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_openTQL.setFont(font)
        self.pushButton_openTQL.setObjectName("pushButton_openTQL")
        self.verticalLayout.addWidget(self.pushButton_openTQL)
        self.pushButton_openEntities = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Baskerville")
        font.setPointSize(18)
        self.pushButton_openEntities.setFont(font)
        self.pushButton_openEntities.setObjectName("pushButton_openEntities")
        self.verticalLayout.addWidget(self.pushButton_openEntities)
        self.pushButton_openRules = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_openRules.setFont(font)
        self.pushButton_openRules.setObjectName("pushButton_openRules")
        self.verticalLayout.addWidget(self.pushButton_openRules)
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(222, 10, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Baskerville")
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dialog"))
        self.pushButton_openTQL.setText(_translate("MainWindow", "TQL"))
        self.pushButton_openEntities.setText(_translate("MainWindow", "Entities"))
        self.pushButton_openRules.setText(_translate("MainWindow", "Rules"))
        self.label.setText(_translate("MainWindow", "Hagnash UI"))