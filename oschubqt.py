import numpy as np
import pandas as pd
import os
import time
from pythonosc import udp_client
from pythonosc.udp_client import SimpleUDPClient
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import QFileDialog

'''
Setup ip and port
'''

ip = "127.0.0.1"
port = 5510 #'faust default'
client = SimpleUDPClient(ip, port)  # Create client

'''
PyQt Gui
'''

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(350, 200)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 100, 300, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(10, 0, 121, 21))
        self.label_title.setObjectName("label_title")
        self.label_parameter = QtWidgets.QLabel(self.centralwidget)
        self.label_parameter.setGeometry(QtCore.QRect(20, 130, 141, 20))
        self.label_parameter.setObjectName("label_parameter")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(125, 70, 113, 32))
        self.pushButton_start.setCheckable(True)
        self.pushButton_start.setChecked(False)
        self.pushButton_start.setAutoDefault(False)
        self.pushButton_start.setObjectName("pushButton_start")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 32, 311, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_dataset = QtWidgets.QLabel(self.layoutWidget)
        self.label_dataset.setObjectName("label_dataset")
        self.horizontalLayout.addWidget(self.label_dataset)
        self.lineEdit_dataset = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_dataset.setObjectName("lineEdit_dataset")
        self.horizontalLayout.addWidget(self.lineEdit_dataset)
        self.pushButton_openfile = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_openfile.setObjectName("pushButton_openfile")
        self.horizontalLayout.addWidget(self.pushButton_openfile)
        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(250, 70, 76, 47))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_speed = QtWidgets.QLabel(self.layoutWidget4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 350, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_start.clicked.connect(self.stream_osc_msg)
        self.pushButton_openfile.clicked.connect(self.browse_file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_title.setText(_translate("MainWindow", "OSC Data Streamer"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.label_dataset.setText(_translate("MainWindow", "Dataset"))
        self.pushButton_openfile.setText(_translate("MainWindow", "Browse"))

    '''
    Read Data
    '''

    def browse_file(self):
        print ("pressed button")
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        print('your file %s is loaded' %(os.path.basename(filename[0])))
        self.path = filename[0]
        print (self.path)


        self.eeg_data = pd.read_csv(self.path, delimiter=";", decimal=",")
        self.eeg_data = self.eeg_data.astype(float)
        self.eeg_data_clean = self.eeg_data.drop(self.eeg_data.index[0:4])
        print (self.eeg_data_clean.shape[0])

        self.lineEdit_dataset.setText(os.path.basename(filename[0]))

    '''
    Create OSC messages and stream data
    '''
    def stream_osc_msg(self):
        if self.pushButton_start.isChecked() == True:
            for i in range(self.eeg_data_clean.shape[0]):
                row = self.eeg_data_clean.iloc[i,:].values #prints row as array
                QtTest.QTest.qWait(1000) #in ms
                self.progressBar.setValue ((i * 100) / self.eeg_data_clean.shape[0])

                for j in range(8):
                    msg_freq = "/Brainwave_Virtual_Instrument/Synth/Channel_%d/modFreq" % (j+1) #reads each value of a row and creates osc message with that value
                    value_freq = (20 + ((40*int(((j+1) * 0.5)+0.5)))) + row[j]
                    client.send_message(msg_freq, value_freq)
                    print (value_freq)

                if self.pushButton_start.isChecked() == False:
                    break

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
