"""
    - версия от 03.03.2017 - исправил вылеты
    - версия от 01.03.20017 - готов прототип
    - версия от 23.02.2017 - значительно переработан GUI,
                             программа разделена на несколько модулей
    - версия от 20.02.2017 - первый прототип

"""

import  sys, os
import Archivist
import JsonDataBase
from BiometricSDK.sdk import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QVideoWidget

class Window(QWidget):

    _Constant_recognition = 0.8

    
    # конструктор формы
    def __init__(self):
        super().__init__()
        self._Client = Biometric_Client(url='https://expasoft.com', port=2133,
                                        subscription_key='9fc9474b4bd16b492276eee41763a3cb')
        self.imgName = os.getcwd() + "\img\currentPhoto.jpg"
        self.imgName0 = os.getcwd() + "\img\currentPhoto0.jpg"
        self.imgName1 = os.getcwd() + "\img\dbPhoto0.jpg"
        self.setObjectName("FormMain")
        self.setWindowTitle("БиоСКУД Watchman")
        self.resize(1024, 600)

        self.groupBoxCamera = QtWidgets.QGroupBox(self)
        self.groupBoxCamera.setObjectName("groupBoxCamera")
        self.groupBoxCamera.setTitle("")
        self.groupBoxCamera.setGeometry(QtCore.QRect(10, 10, 500, 371))
        
        self.labelCameraTitle = QtWidgets.QLabel(self.groupBoxCamera)
        self.labelCameraTitle.setObjectName("labelCameraTitle")
        self.labelCameraTitle.setText("Изображение с камеры")
        self.labelCameraTitle.setGeometry(QtCore.QRect(160, 10, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelCameraTitle.setFont(font)
        
        self.CameraStream = QVideoWidget(self)
        self.CameraStream.setObjectName("videoCameraStream")
        self.CameraStream.setGeometry(QtCore.QRect(10, 50, 481, 261))
        self.CameraStream.setMinimumSize(QtCore.QSize(241, 0))
       
        self.pushButtonRecognition = QtWidgets.QPushButton(self.groupBoxCamera)
        self.pushButtonRecognition.setObjectName("pushButtonRecognition")
        self.pushButtonRecognition.setText("Распознать")
        self.pushButtonRecognition.setGeometry(QtCore.QRect(10, 310, 481, 51))
        self.pushButtonRecognition.clicked.connect(self.identifyPersonBegin)
        
        self.pushButtonLog = QtWidgets.QPushButton(self)
        self.pushButtonLog.setObjectName("pushButtonLog")
        self.pushButtonLog.setText("Журнал")
        self.pushButtonLog.setGeometry(QtCore.QRect(10, 460, 121, 61))
        self.pushButtonLog.clicked.connect(self.OpenLogFile)
        
        self.pushButtonDb = QtWidgets.QPushButton(self)
        self.pushButtonDb.setObjectName("pushButtonDb")
        self.pushButtonDb.setText("База данных")
        self.pushButtonDb.setGeometry(QtCore.QRect(10, 390, 121, 61))
        self.pushButtonDb.clicked.connect(self.OpenArchivist)
        
        self.groupBoxRecognition = QtWidgets.QGroupBox(self)
        self.groupBoxRecognition.setObjectName("groupBoxRecognition")
        self.groupBoxRecognition.setTitle("")
        self.groupBoxRecognition.setGeometry(QtCore.QRect(520, 10, 500, 581))

        self.pushButtonExit = QtWidgets.QPushButton(self)
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.pushButtonExit.setText("Выйти")
        self.pushButtonExit.setGeometry(QtCore.QRect(10, 530, 121, 61))
        self.pushButtonExit.clicked.connect(self.ExitProgream)

        self.labelPersonName = QtWidgets.QLabel(self.groupBoxRecognition)
        self.labelPersonName.setObjectName("labelPersonName")
        self.labelPersonName.setText("")
        self.labelPersonName.setGeometry(QtCore.QRect(20, 320, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelPersonName.setFont(font)
        
        self.labelCurrentPhoto = QtWidgets.QLabel(self.groupBoxRecognition)
        self.labelCurrentPhoto.setObjectName("labelCurrentPhoto")
        self.labelCurrentPhoto.setText("")
        self.labelCurrentPhoto.setGeometry(QtCore.QRect(10, 40, 241, 261))
        self.labelCurrentPhoto.setMinimumSize(QtCore.QSize(241, 0))
        self.labelCurrentPhoto.setAlignment(QtCore.Qt.AlignCenter)
        
        self.labelPersonJob = QtWidgets.QLabel(self.groupBoxRecognition)
        self.labelPersonJob.setObjectName("labelPersonJob")
        self.labelPersonJob.setText("")
        self.labelPersonJob.setGeometry(QtCore.QRect(20, 360, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelPersonJob.setFont(font)

        self.labelPersonInf = QtWidgets.QLabel(self.groupBoxRecognition)
        self.labelPersonInf.setObjectName("labelPersonJob")
        self.labelPersonInf.setText("")
        self.labelPersonInf.setGeometry(QtCore.QRect(20, 400, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelPersonInf.setFont(font)
        
        self.labelAccess = QtWidgets.QLabel(self.groupBoxRecognition)
        self.labelAccess.setObjectName("labelAccess")
        self.labelAccess.setText("<html><head/><body><p align=\"center\">Допущен</p></body></html>")
        self.labelAccess.setGeometry(QtCore.QRect(10, 490, 481, 81))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(76, 197, 32))
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        self.labelAccess.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelAccess.setFont(font)
        self.labelAccess.setAcceptDrops(False)
        self.labelAccess.setAutoFillBackground(True)
        self.labelAccess.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelAccess.setFrameShadow(QtWidgets.QFrame.Plain)
        self.labelAccess.setTextFormat(QtCore.Qt.AutoText)
        self.labelAccess.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)

        self.labelDbPhoto = QtWidgets.QLabel(self.groupBoxRecognition)
        self.labelDbPhoto.setObjectName("labelDbPhoto")
        self.labelDbPhoto.setText("")
        self.labelDbPhoto.setGeometry(QtCore.QRect(250, 40, 241, 261))
        self.labelDbPhoto.setMinimumSize(QtCore.QSize(241, 0))
        self.labelDbPhoto.setAlignment(QtCore.Qt.AlignCenter)
        
        self.labelCurrentPhotoTitle = QtWidgets.QLabel(self.groupBoxRecognition)
        self.labelCurrentPhotoTitle.setObjectName("labelCurrentPhotoTitle")
        self.labelCurrentPhotoTitle.setText("Текущее фото")
        self.labelCurrentPhotoTitle.setGeometry(QtCore.QRect(80, 10, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelCurrentPhotoTitle.setFont(font)

        self.labelDbPhotoTitle = QtWidgets.QLabel(self.groupBoxRecognition)
        self.labelDbPhotoTitle.setObjectName("labelDbPhotoTitle")
        self.labelDbPhotoTitle.setText("Фото в базе")
        self.labelDbPhotoTitle.setGeometry(QtCore.QRect(320, 10, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelDbPhotoTitle.setFont(font)

        self.device = QCamera.availableDevices()[0]
        self.camera = QCamera(self.device)
        self.camera.setViewfinder(self.CameraStream)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.imageCapture=QCameraImageCapture(self.camera)
        self.imageCapture.imageSaved.connect(self.identifyPersonEnd)
        self.camera.start()

    # идентификация человека (фото)
    def identifyPersonBegin(self):
        if self.imageCapture.isReadyForCapture():
            #imgName = os.getcwd() + "\img\currentPhoto.jpg"
            self.camera.searchAndLock()
            self.imageCapture.capture(self.imgName)
            self.camera.unlock()

    # идентификация человека (алгоритм)
    def identifyPersonEnd(self):

        self._Client.get_aligned_faces(self.imgName, "img\currentPhoto")
        
        id_person = self._Client.identify_profile_by_face(self.imgName0, 1, 0).pop("result")[0]
        self._Client.get_profile_image(id_person['profile_id'], id_person['image_id'],self.imgName1)
        self.labelCurrentPhoto.setPixmap(QtGui.QPixmap(self.imgName0))
        self.labelDbPhoto.setPixmap(QtGui.QPixmap(self.imgName1))

        profile = JsonDataBase.GetInfo(id_person['profile_id'])
        if profile != None:
            self.labelPersonName.setText(profile['name'])
            self.labelPersonJob.setText(profile['tag'])
        else:
            self.labelPersonName.setText(profile[''])
            self.labelPersonJob.setText(profile[''])

        if id_person['score'] > self._Constant_recognition :
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(255, 22, 46))
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
            self.labelAccess.setPalette(palette)
            self.labelAccess.setText("<html><head/><body><p align=\"center\">Недопущен</p></body></html>")
        else:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(76, 197, 32))
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
            self.labelAccess.setPalette(palette)
            self.labelAccess.setText("<html><head/><body><p align=\"center\">Допущен</p></body></html>")
        self.labelPersonInf.setText('id= ' + str(id_person['profile_id'])+' score= '+str(id_person['score']))

    # открыть управление базой данных
    def OpenArchivist(self):
        self.archivist = Archivist.Window()
        self.archivist.show()

    # открыть файл логов
    def OpenLogFile(self):
        os.system("log.txt")

    # выйти из программы
    def ExitProgream(self):
        self.camera.stop()
        self.close()

# запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
