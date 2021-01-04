# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'iter_1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1013, 808)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.generateWatershedBtn = QtWidgets.QPushButton(self.centralwidget)
        self.generateWatershedBtn.setGeometry(QtCore.QRect(0, 30, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.generateWatershedBtn.setFont(font)
        self.generateWatershedBtn.setObjectName("generate_watershed_btn")
        self.generateWatershedBtn.setText("Generate Watershed")

        self.generateStreamsBtn = QtWidgets.QPushButton(self.centralwidget)
        self.generateStreamsBtn.setGeometry(QtCore.QRect(0, 80, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.generateStreamsBtn.setFont(font)
        self.generateStreamsBtn.setObjectName("generate_streams_btn")
        self.generateStreamsBtn.setText("Generate Streams")

        self.openDemBtn = QtWidgets.QPushButton(self.centralwidget)
        self.openDemBtn.setGeometry(QtCore.QRect(350, 280, 291, 151))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.openDemBtn.setFont(font)
        self.openDemBtn.setObjectName("open_dem_btn")
        self.openDemBtn.setText("OPEN DEM")

        self.xLabel = QtWidgets.QLabel(self.centralwidget)
        self.xLabel.setGeometry(QtCore.QRect(10, 160, 161, 41))
        self.xLabel.setObjectName("x_label")
        self.xLabel.setText("X: ")

        self.yLabel = QtWidgets.QLabel(self.centralwidget)
        self.yLabel.setGeometry(QtCore.QRect(10, 210, 161, 41))
        self.yLabel.setObjectName("y_label")
        self.yLabel.setText("Y: ")

        self.dem_name = QtWidgets.QLabel(self.centralwidget)
        self.dem_name.setGeometry(QtCore.QRect(10, 0, 261, 21))
        self.dem_name.setObjectName("label_3")
        self.dem_name.setText("DEM Name:")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1013, 21))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionNone = QtWidgets.QAction(MainWindow)
        self.actionNone.setObjectName("actionNone")
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.actionNone)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionNone.setText(_translate("MainWindow", "None"))

