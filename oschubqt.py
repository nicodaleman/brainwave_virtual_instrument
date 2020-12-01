import numpy as np
import pandas as pd
import os
import time
from pythonosc import udp_client
from pythonosc.udp_client import SimpleUDPClient


from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import QFileDialog

# '''
# Read Data
# '''
# eeg_data = pd.read_csv('testdata.csv', delimiter=";", decimal=",")
# eeg_data = eeg_data.astype(float)
# eeg_data_clean = eeg_data.drop(eeg_data.index[0:4])

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
        MainWindow.resize(350, 338)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 260, 301, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(10, 0, 121, 21))
        self.label_title.setObjectName("label_title")
        self.label_parameter = QtWidgets.QLabel(self.centralwidget)
        self.label_parameter.setGeometry(QtCore.QRect(20, 130, 141, 20))
        self.label_parameter.setObjectName("label_parameter")
        self.checkBox_panratio = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_panratio.setGeometry(QtCore.QRect(20, 240, 86, 20))
        self.checkBox_panratio.setObjectName("checkBox_panratio")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(200, 220, 113, 32))
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
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 62, 211, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_ipaddress = QtWidgets.QLabel(self.layoutWidget1)
        self.label_ipaddress.setObjectName("label_ipaddress")
        self.horizontalLayout_2.addWidget(self.label_ipaddress)
        self.lineEdit_ipaddress = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_ipaddress.setObjectName("lineEdit_ipaddress")
        self.horizontalLayout_2.addWidget(self.lineEdit_ipaddress)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 92, 213, 31))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_portnumber = QtWidgets.QLabel(self.layoutWidget2)
        self.label_portnumber.setObjectName("label_portnumber")
        self.horizontalLayout_3.addWidget(self.label_portnumber)
        self.lineEdit_portnumber = QtWidgets.QLineEdit(self.layoutWidget2)
        self.lineEdit_portnumber.setObjectName("lineEdit_portnumber")
        self.horizontalLayout_3.addWidget(self.lineEdit_portnumber)
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 150, 84, 77))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_modfreq = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_modfreq.setChecked(True)
        self.radioButton_modfreq.setObjectName("radioButton_modfreq")
        self.verticalLayout.addWidget(self.radioButton_modfreq)
        self.radioButton_index = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_index.setObjectName("radioButton_index")
        self.verticalLayout.addWidget(self.radioButton_index)
        self.radioButton_ratio = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_ratio.setObjectName("radioButton_ratio")
        self.verticalLayout.addWidget(self.radioButton_ratio)
        self.radioButton_decay = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_decay.setObjectName("radioButton_decay")
        self.verticalLayout.addWidget(self.radioButton_decay)
        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(250, 70, 76, 47))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_speed = QtWidgets.QLabel(self.layoutWidget4)
        self.label_speed.setObjectName("label_speed")
        self.verticalLayout_2.addWidget(self.label_speed)
        self.box_speed = QtWidgets.QSpinBox(self.layoutWidget4)
        self.box_speed.setMinimum(20)
        self.box_speed.setMaximum(10000)
        self.box_speed.setProperty("value", 1000)
        self.box_speed.setObjectName("box_speed")
        self.verticalLayout_2.addWidget(self.box_speed)
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
        self.label_parameter.setText(_translate("MainWindow", "Instrument Parameter"))
        self.checkBox_panratio.setText(_translate("MainWindow", "Pan Ratio"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.label_dataset.setText(_translate("MainWindow", "Dataset"))
        self.pushButton_openfile.setText(_translate("MainWindow", "Browse"))
        self.label_ipaddress.setText(_translate("MainWindow", "IP Address"))
        self.lineEdit_ipaddress.setText(_translate("MainWindow", "127.0.0.1"))
        self.lineEdit_ipaddress.setPlaceholderText(_translate("MainWindow", "127.0.0.1"))
        self.label_portnumber.setText(_translate("MainWindow", "Port Number"))
        self.lineEdit_portnumber.setText(_translate("MainWindow", "5510"))
        self.lineEdit_portnumber.setPlaceholderText(_translate("MainWindow", "5510"))
        self.radioButton_modfreq.setText(_translate("MainWindow", "Mod Freq"))
        self.radioButton_index.setText(_translate("MainWindow", "Index"))
        self.radioButton_ratio.setText(_translate("MainWindow", "Ratio"))
        self.radioButton_decay.setText(_translate("MainWindow", "Decay"))
        self.label_speed.setText(_translate("MainWindow", "Speed (ms)"))


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
                #time.sleep(1) #delay
                self.progressBar.setValue ((i * 100) / self.eeg_data_clean.shape[0])

                for j in range(8):
                    msg_freq = "/Brainwave_Virtual_Instrument/Synth/Channel_%d/modFreq" % (j+1) #reads each value of a row and creates osc message with that value
                    value_freq = (20 + ((40*int(((j+1) * 0.5)+0.5)))) + row[j]
                    client.send_message(msg_freq, value_freq)
                    print (value_freq)


                # for k in range (8):
                #     msg_pan = "/BrainwaveVirtualInstrument/Synth/Channel_%d/pan" % (k+1)
                #     value_pan = (row[int(k/2)+2]) * 0.25 #scale 0.5 for 0-1 pan range, scale 0.25 for skew data values
                #     client.send_message(msg_freq, value_freq )
                #     #print (msg_pan, value_pan)

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










# In[ ]:





# In[ ]:
