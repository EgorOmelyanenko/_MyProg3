"""
    - версия от 03.03.2017 - большой рефакторинг
    - версия от 01.03.20017 - небольшой рефакторинг
    - версия от 20.02.2017 - первый прототип

"""

import sys, os, time, datetime, json
import JsonDataBase
from BiometricSDK.sdk import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QVideoWidget
from os import path
from JsonDataBase import *
class Window(QWidget):


    # конструктор формы
    def __init__(self):
        super().__init__()
        self._Client = Biometric_Client(url='https://expasoft.com', port=2133,
                                        subscription_key='9fc9474b4bd16b492276eee41763a3cb')

        self.resize(800, 600)
        self.setObjectName("FormMain")
        self.setWindowTitle("БиоСКУД Archivist")

        self.labelHumans = QtWidgets.QLabel(self)
        self.labelHumans.setObjectName("labelHumans")
        self.labelHumans.setText("Профили сотрудников")
        self.labelHumans.setGeometry(QtCore.QRect(80, 15, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelHumans.setFont(font)

        self.labelPhotos = QtWidgets.QLabel(self)
        self.labelPhotos.setObjectName("labelPhotos")
        self.labelPhotos.setText("Фото сотрудника")
        self.labelPhotos.setGeometry(QtCore.QRect(390, 15, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelPhotos.setFont(font)

        self.listViewHumans = QtWidgets.QListWidget(self)
        self.listViewHumans.setObjectName("listViewHumans")
        self.listViewHumans.setGeometry(QtCore.QRect(10, 50, 291, 531))
        self.listViewHumans.setIconSize(QtCore.QSize(200, 200))
        self.listViewHumans.itemClicked.connect(self.LoadProfile)

        self.listViewPhotos = QtWidgets.QListWidget(self)
        self.listViewPhotos.setObjectName("listViewPhotos")
        self.listViewPhotos.setGeometry(QtCore.QRect(310, 50, 291, 281))
        self.listViewPhotos.setIconSize(QtCore.QSize(150, 150))

        self.labelName = QLabel(self)
        self.labelName.setText("ФИО:")
        self.labelName.move(310, 355)

        self.lineName=QLineEdit(self)
        self.lineName.resize(140,25)
        self.lineName.move(350,350)



        self.labelTag=QLabel(self)
        self.labelTag.setText("Пост:")
        self.labelTag.move(310,385)

        self.lineTag = QLineEdit(self)
        self.lineTag.resize(140, 25)
        self.lineTag.move(350, 380)

        self.pushButtonAddProfile = QtWidgets.QPushButton(self)
        self.pushButtonAddProfile.setGeometry(QtCore.QRect(310, 420, 181, 51))
        self.pushButtonAddProfile.setObjectName("pushButtonAddProfile")
        self.pushButtonAddProfile.setText("Добавить профиль")
        self.pushButtonAddProfile.clicked.connect(self.AddProfile)

        self.pushButtonUpdateProfile = QtWidgets.QPushButton(self)
        self.pushButtonUpdateProfile.setGeometry(QtCore.QRect(310, 475, 181, 51))
        self.pushButtonUpdateProfile.setObjectName("pushButtonAddProfile")
        self.pushButtonUpdateProfile.setText("Обновить профиль")
        self.pushButtonUpdateProfile.clicked.connect(self.UpdateProfile)

        self.pushButtonDelProfile = QtWidgets.QPushButton(self)
        self.pushButtonDelProfile.setGeometry(QtCore.QRect(310, 530, 181, 51))
        self.pushButtonDelProfile.setObjectName("pushButtonDelProfile")
        self.pushButtonDelProfile.setText("Удалить профиль")
        self.pushButtonDelProfile.clicked.connect(self.DelProfile)

        self.CameraStream = QVideoWidget(self)
        self.CameraStream.setObjectName("videoCameraStream")
        self.CameraStream.setGeometry(QtCore.QRect(610, 25, 180, 200))

        self.device = QCamera.availableDevices()[0]
        self.camera = QCamera(self.device)
        self.camera.setViewfinder(self.CameraStream)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.imageCapture=QCameraImageCapture(self.camera)
        self.imageCapture.imageSaved.connect(self.AddPhotoEnd)
        self.camera.start()

        self.pushButtonAddPhoto = QtWidgets.QPushButton(self)
        self.pushButtonAddPhoto.setObjectName("pushButtonAddPhoto")
        self.pushButtonAddPhoto.setText("Добавить фото")
        self.pushButtonAddPhoto.setGeometry(QtCore.QRect(610, 225, 181, 51))
        self.pushButtonAddPhoto.clicked.connect(self.AddPhotoBegin)

        self.pushButtonDelPhoto = QtWidgets.QPushButton(self)
        self.pushButtonDelPhoto.setObjectName("pushButtonDelPhoto")
        self.pushButtonDelPhoto.setText("Удалить фото")
        self.pushButtonDelPhoto.setGeometry(QtCore.QRect(610, 280, 181, 51))
        self.pushButtonDelPhoto.clicked.connect(self.DelPhoto)

        self.LoadProfiles()

 # загружаем список сотрудников
    def LoadProfiles(self):
        self.listViewHumans.clear()
        AllProfiles = self._Client.get_profiles_ids()['result']
        if len(AllProfiles) != 0:
            for profile in AllProfiles:
                item = QtWidgets.QListWidgetItem()
                #item.setText(str(profile))
                if (GetInfo(str(profile))!=None):
                    item.setText(GetInfo(str(profile))["name"])
                item.setToolTip(str(profile))

                AllPhoto = self._Client.get_profile_images_ids(profile)['result']
                if len(AllPhoto) != 0:
                    FileName = "img/" + str(profile) + '-' + str(AllPhoto[0]) + '.jpg'
                    self._Client.get_profile_image(profile, AllPhoto[0], FileName)
                    item.setIcon(QtGui.QIcon(FileName))
                self.listViewHumans.addItem(item)

    # загружаем профиль
    def LoadProfile(self, item):
        self.listViewPhotos.clear()
        #idProfile = int(item.text())
        idProfile = int(item.toolTip())
        AllPhoto = self._Client.get_profile_images_ids(idProfile)['result']
        for photo in AllPhoto:
            FileName = "img/" + str(idProfile) + '-' + str(photo) + '.jpg'
            self._Client.get_profile_image(idProfile, photo, FileName)

            item = QtWidgets.QListWidgetItem()
            item.setText(str(photo))
            item.setIcon(QtGui.QIcon(FileName))
            self.listViewPhotos.addItem(item)
        infoProfile = JsonDataBase.GetInfo(idProfile)
        if infoProfile != None:
            self.lineName.setText(infoProfile['name'])
            self.lineTag.setText(infoProfile['tag'])
        else:
            self.lineName.setText("")
            self.lineTag.setText("")
        
    # добавляем профиль
    def AddProfile(self):
        profile_name = self.lineName.text()
        profile_post = self.lineTag.text()
        Id_Profile = self._Client.add_profile(profile_name, '01.01.1111', 'm', tags="").pop('result')
        JsonDataBase.AddInfo(Id_Profile, profile_name,'01.01.1111',"m", profile_post)
        self.LoadProfiles()

    # обновляем профиль
    def UpdateProfile(self):
        Id_Profile = self.listViewHumans.currentItem().toolTip()
        profile_name = self.lineName.text()
        profile_post = self.lineTag.text()
        if (JsonDataBase.GetInfo(Id_Profile)!=None):
            JsonDataBase.UpdateInfo(Id_Profile, name=profile_name, tag=profile_post)
        else:
            JsonDataBase.AddInfo(Id_Profile, name=profile_name, tag=profile_post)
        self.LoadProfiles()

    # удаляем профиль
    def DelProfile(self):
        Id_Profile = self.listViewHumans.currentItem().toolTip()
        self._Client.delete_profile(Id_Profile)
        JsonDataBase.DelInfo(Id_Profile)
        self.LoadProfiles()

    # добавляем фото
    def AddPhotoBegin(self):
        if self.imageCapture.isReadyForCapture():
            imgName = os.getcwd() + "\img\currentPhoto.jpg"
            self.camera.searchAndLock()
            self.imageCapture.capture(imgName)
            self.camera.unlock()
        
    def AddPhotoEnd(self):
        print(0)
        imgName = os.getcwd() + "\img\currentPhoto.jpg"
        imgName0 = os.getcwd() + "\img\currentPhoto0.jpg"
        idProfile = int(self.listViewHumans.currentItem().toolTip())
        self._Client.get_aligned_faces(imgName, "img\currentPhoto")
        self._Client.enroll_profile_face(idProfile, imgName0)
        self.LoadProfile(self.listViewHumans.currentItem())
                
    # удаляем фото
    def DelPhoto(self):
        #Id_Profile = self.listViewHumans.currentItem().text()
        Id_Profile = self.listViewHumans.currentItem().toolTip()
        Id_Photo = self.listViewPhotos.currentItem().text()
        self._Client.delete_image(Id_Profile, Id_Photo)
        self.LoadProfile(self.listViewHumans.currentItem())

# запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
