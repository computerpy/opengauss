# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subject.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(725, 605)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(70, 40, 561, 501))
        self.frame.setStyleSheet("QFrame{border-top-left-radius:80px;\n"
"border-top-right-radius:80px;\n"
"border-bottom-left-radius:80px;\n"
"border-bottom-right-radius:80px;\n"
"background-color: rgba(66, 96, 207, 180);}\n"
"\n"
"QLabel{background-color: rgba(66, 96, 207, 0)}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(150, 50, 280, 30))
        self.label.setMinimumSize(QtCore.QSize(280, 30))
        self.label.setMaximumSize(QtCore.QSize(280, 30))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(140, 110, 291, 42))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(90, 40))
        self.pushButton.setMaximumSize(QtCore.QSize(90, 40))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(90, 40))
        self.pushButton_2.setMaximumSize(QtCore.QSize(90, 40))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.layoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.layoutWidget_2.setGeometry(QtCore.QRect(460, 30, 68, 32))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton_7.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_7.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_7.setStyleSheet("border-image: url(:/pic/minus.png);")
        self.pushButton_7.setText("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_11.addWidget(self.pushButton_7)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton_4.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_4.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_4.setStyleSheet("border-image: url(:/pic/close.png);")
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_11.addWidget(self.pushButton_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 725, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "请选择考试科目"))
        self.pushButton.setText(_translate("MainWindow", "python"))
        self.pushButton_2.setText(_translate("MainWindow", "数学"))
import exp_qrc_rc
