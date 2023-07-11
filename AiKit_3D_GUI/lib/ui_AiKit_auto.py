# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AiKit_autozCijoy.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_AiKit_UI(object):
    def setupUi(self, AiKit_UI):
        if not AiKit_UI.objectName():
            AiKit_UI.setObjectName(u"AiKit_UI")
        AiKit_UI.resize(1367, 938)
        AiKit_UI.setStyleSheet(u"background-color: rgb(243, 243, 243);")
        self.centralwidget = QWidget(AiKit_UI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.menu_widget = QWidget(self.centralwidget)
        self.menu_widget.setObjectName(u"menu_widget")
        self.menu_widget.setMaximumSize(QSize(16777215, 50))
        self.menu_widget.setStyleSheet(u"background-color: rgb(52, 73, 94);")
        self.gridLayout = QGridLayout(self.menu_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 0, 0, 0)
        self.title = QLabel(self.menu_widget)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet(u"background-color: rgb(255, 255, 255\uff0c200);\n"
"color: rgb(255, 255, 255);")

        self.gridLayout.addWidget(self.title, 0, 1, 1, 1)

        self.logo_lab = QLabel(self.menu_widget)
        self.logo_lab.setObjectName(u"logo_lab")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_lab.sizePolicy().hasHeightForWidth())
        self.logo_lab.setSizePolicy(sizePolicy)
        self.logo_lab.setMinimumSize(QSize(25, 25))
        self.logo_lab.setMaximumSize(QSize(25, 25))
        self.logo_lab.setStyleSheet(u"")
        self.logo_lab.setMargin(-19)

        self.gridLayout.addWidget(self.logo_lab, 0, 0, 1, 1)

        self.min_btn = QPushButton(self.menu_widget)
        self.min_btn.setObjectName(u"min_btn")
        self.min_btn.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.min_btn.sizePolicy().hasHeightForWidth())
        self.min_btn.setSizePolicy(sizePolicy1)
        self.min_btn.setMinimumSize(QSize(30, 30))
        self.min_btn.setMaximumSize(QSize(30, 30))
        self.min_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.min_btn.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u"C:/Users/Administrator/.designer/AiKit_UI_img/min.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.min_btn.setIcon(icon)
        self.min_btn.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.min_btn, 0, 2, 1, 1)

        self.max_btn = QPushButton(self.menu_widget)
        self.max_btn.setObjectName(u"max_btn")
        self.max_btn.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.max_btn.sizePolicy().hasHeightForWidth())
        self.max_btn.setSizePolicy(sizePolicy1)
        self.max_btn.setMinimumSize(QSize(30, 30))
        self.max_btn.setMaximumSize(QSize(30, 30))
        self.max_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.max_btn.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u"C:/Users/Administrator/.designer/AiKit_UI_img/max.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.max_btn.setIcon(icon1)
        self.max_btn.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.max_btn, 0, 3, 1, 1)

        self.close_btn = QPushButton(self.menu_widget)
        self.close_btn.setObjectName(u"close_btn")
        self.close_btn.setMinimumSize(QSize(30, 30))
        self.close_btn.setMaximumSize(QSize(30, 30))
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u"C:/Users/Administrator/.designer/AiKit_UI_img/close.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.close_btn.setIcon(icon2)
        self.close_btn.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.close_btn, 0, 4, 1, 1)


        self.verticalLayout.addWidget(self.menu_widget)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 1367, 881))
        self.scrollAreaWidgetContents_3.setMinimumSize(QSize(1218, 880))
        self.verticalLayout_11 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.body_widget = QWidget(self.scrollAreaWidgetContents_3)
        self.body_widget.setObjectName(u"body_widget")
        self.body_widget.setStyleSheet(u"background-color: rgb(243, 243, 243);")
        self.horizontalLayout = QHBoxLayout(self.body_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.body_left_widget = QWidget(self.body_widget)
        self.body_left_widget.setObjectName(u"body_left_widget")
        self.body_left_widget.setMaximumSize(QSize(400, 700))
        self.body_left_widget.setStyleSheet(u"background-color: rgb(218, 218, 218);")
        self.verticalLayout_8 = QVBoxLayout(self.body_left_widget)
        self.verticalLayout_8.setSpacing(10)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(10, 10, 10, 10)
        self.widget = QWidget(self.body_left_widget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.connect_lab = QLabel(self.widget)
        self.connect_lab.setObjectName(u"connect_lab")
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setWeight(75)
        self.connect_lab.setFont(font1)
        self.connect_lab.setStyleSheet(u"background-color: rgb(255, 255, 255\uff0c200);")

        self.horizontalLayout_2.addWidget(self.connect_lab)

        self.connect_btn = QPushButton(self.widget)
        self.connect_btn.setObjectName(u"connect_btn")
        self.connect_btn.setEnabled(True)
        self.connect_btn.setMinimumSize(QSize(0, 30))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setBold(True)
        font2.setWeight(75)
        self.connect_btn.setFont(font2)
        self.connect_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.connect_btn.setStyleSheet(u"background-color: rgb(39, 174, 96);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 7px;\n"
"border: 2px groove gray;\n"
"border-style: outset;")
        self.connect_btn.setAutoDefault(False)
        self.connect_btn.setFlat(False)

        self.horizontalLayout_2.addWidget(self.connect_btn)


        self.verticalLayout_8.addWidget(self.widget)

        self.widget_2 = QWidget(self.body_left_widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"background-color: rgb(236, 240, 241);")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, 0, 10, 0)
        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.port_lab = QLabel(self.widget_3)
        self.port_lab.setObjectName(u"port_lab")
        font3 = QFont()
        font3.setFamily(u"Arial")
        font3.setBold(False)
        font3.setWeight(50)
        self.port_lab.setFont(font3)
        self.port_lab.setStyleSheet(u"background-color: rgb(255, 255, 255\uff0c200);")

        self.verticalLayout_2.addWidget(self.port_lab)

        self.device_lab = QLabel(self.widget_3)
        self.device_lab.setObjectName(u"device_lab")
        self.device_lab.setFont(font3)
        self.device_lab.setStyleSheet(u"background-color: rgb(255, 255, 255\uff0c200);")

        self.verticalLayout_2.addWidget(self.device_lab)

        self.baud_lab = QLabel(self.widget_3)
        self.baud_lab.setObjectName(u"baud_lab")
        self.baud_lab.setFont(font3)
        self.baud_lab.setStyleSheet(u"background-color: rgb(255, 255, 255\uff0c200);")

        self.verticalLayout_2.addWidget(self.baud_lab)


        self.horizontalLayout_3.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.comboBox_port = QComboBox(self.widget_4)
        self.comboBox_port.addItem("")
        self.comboBox_port.setObjectName(u"comboBox_port")
        self.comboBox_port.setFont(font3)

        self.verticalLayout_3.addWidget(self.comboBox_port)

        self.comboBox_device = QComboBox(self.widget_4)
        self.comboBox_device.addItem("")
        self.comboBox_device.addItem("")
        self.comboBox_device.addItem("")
        self.comboBox_device.addItem("")
        self.comboBox_device.setObjectName(u"comboBox_device")
        self.comboBox_device.setFont(font3)

        self.verticalLayout_3.addWidget(self.comboBox_device)

        self.comboBox_baud = QComboBox(self.widget_4)
        self.comboBox_baud.addItem("")
        self.comboBox_baud.addItem("")
        self.comboBox_baud.setObjectName(u"comboBox_baud")
        self.comboBox_baud.setFont(font3)

        self.verticalLayout_3.addWidget(self.comboBox_baud)


        self.horizontalLayout_3.addWidget(self.widget_4)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)

        self.verticalLayout_8.addWidget(self.widget_2)

        self.widget_5 = QWidget(self.body_left_widget)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.func_lab = QLabel(self.widget_5)
        self.func_lab.setObjectName(u"func_lab")
        self.func_lab.setFont(font1)

        self.horizontalLayout_4.addWidget(self.func_lab)


        self.verticalLayout_8.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.body_left_widget)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setStyleSheet(u"background-color: rgb(236, 240, 241);")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.func_lab_2 = QLabel(self.widget_6)
        self.func_lab_2.setObjectName(u"func_lab_2")
        font4 = QFont()
        font4.setFamily(u"Arial")
        font4.setPointSize(11)
        font4.setBold(True)
        font4.setWeight(75)
        self.func_lab_2.setFont(font4)

        self.horizontalLayout_5.addWidget(self.func_lab_2)

        self.to_origin_btn = QPushButton(self.widget_6)
        self.to_origin_btn.setObjectName(u"to_origin_btn")
        self.to_origin_btn.setMinimumSize(QSize(0, 30))
        font5 = QFont()
        font5.setFamily(u"Arial")
        font5.setBold(True)
        font5.setWeight(75)
        self.to_origin_btn.setFont(font5)
        self.to_origin_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.to_origin_btn.setStyleSheet(u"background-color:rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"border: 2px groove gray;\n"
"border-style: outset;")

        self.horizontalLayout_5.addWidget(self.to_origin_btn)

        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 1)

        self.verticalLayout_8.addWidget(self.widget_6)

        self.widget_7 = QWidget(self.body_left_widget)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setStyleSheet(u"background-color: rgb(236, 240, 241);")
        self.verticalLayout_4 = QVBoxLayout(self.widget_7)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 10, 0, 10)
        self.widget_12 = QWidget(self.widget_7)
        self.widget_12.setObjectName(u"widget_12")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(10, 0, 10, 0)
        self.func_lab_4 = QLabel(self.widget_12)
        self.func_lab_4.setObjectName(u"func_lab_4")
        self.func_lab_4.setFont(font4)

        self.horizontalLayout_6.addWidget(self.func_lab_4)

        self.discern_btn = QPushButton(self.widget_12)
        self.discern_btn.setObjectName(u"discern_btn")
        self.discern_btn.setMinimumSize(QSize(0, 30))
        self.discern_btn.setFont(font5)
        self.discern_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.discern_btn.setStyleSheet(u"background-color:rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"border: 2px groove gray;\n"
"border-style: outset;")

        self.horizontalLayout_6.addWidget(self.discern_btn)

        self.horizontalLayout_6.setStretch(0, 2)
        self.horizontalLayout_6.setStretch(1, 1)

        self.verticalLayout_4.addWidget(self.widget_12)

        self.widget_13 = QWidget(self.widget_7)
        self.widget_13.setObjectName(u"widget_13")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_13)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(10, 0, 10, 0)
        self.func_lab_5 = QLabel(self.widget_13)
        self.func_lab_5.setObjectName(u"func_lab_5")
        font6 = QFont()
        font6.setFamily(u"Arial")
        font6.setPointSize(8)
        font6.setBold(True)
        font6.setWeight(75)
        self.func_lab_5.setFont(font6)
        self.func_lab_5.setStyleSheet(u"color: rgb(136, 136, 136);")

        self.horizontalLayout_7.addWidget(self.func_lab_5)

        self.algorithm_lab = QLabel(self.widget_13)
        self.algorithm_lab.setObjectName(u"algorithm_lab")
        self.algorithm_lab.setFont(font6)
        self.algorithm_lab.setStyleSheet(u"color: rgb(136, 136, 136);\n"
"background-color: rgb(243, 243, 243,200);")

        self.horizontalLayout_7.addWidget(self.algorithm_lab)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 2)

        self.verticalLayout_4.addWidget(self.widget_13)


        self.verticalLayout_8.addWidget(self.widget_7)

        self.widget_8 = QWidget(self.body_left_widget)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setStyleSheet(u"background-color: rgb(236, 240, 241);")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(10, 10, 10, 10)
        self.func_lab_7 = QLabel(self.widget_8)
        self.func_lab_7.setObjectName(u"func_lab_7")
        self.func_lab_7.setFont(font4)

        self.horizontalLayout_8.addWidget(self.func_lab_7)

        self.crawl_btn = QPushButton(self.widget_8)
        self.crawl_btn.setObjectName(u"crawl_btn")
        self.crawl_btn.setMinimumSize(QSize(0, 30))
        self.crawl_btn.setFont(font5)
        self.crawl_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.crawl_btn.setStyleSheet(u"background-color:rgb(41, 128, 185);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"border: 2px groove gray;\n"
"border-style: outset;")

        self.horizontalLayout_8.addWidget(self.crawl_btn)

        self.horizontalLayout_8.setStretch(0, 2)
        self.horizontalLayout_8.setStretch(1, 1)

        self.verticalLayout_8.addWidget(self.widget_8)

        self.label = QLabel(self.body_left_widget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 2))
        self.label.setStyleSheet(u"background-color: rgb(149, 165, 166);")

        self.verticalLayout_8.addWidget(self.label)

        self.widget_18 = QWidget(self.body_left_widget)
        self.widget_18.setObjectName(u"widget_18")
        self.horizontalLayout_13 = QHBoxLayout(self.widget_18)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 11)
        self.func_lab_9 = QLabel(self.widget_18)
        self.func_lab_9.setObjectName(u"func_lab_9")
        self.func_lab_9.setFont(font1)

        self.horizontalLayout_13.addWidget(self.func_lab_9)


        self.verticalLayout_8.addWidget(self.widget_18)

        self.widget_11 = QWidget(self.body_left_widget)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setStyleSheet(u"background-color: rgb(236, 240, 241);")
        self.horizontalLayout_14 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(10, 10, 10, 10)
        self.func_lab_10 = QLabel(self.widget_11)
        self.func_lab_10.setObjectName(u"func_lab_10")
        self.func_lab_10.setFont(font4)

        self.horizontalLayout_14.addWidget(self.func_lab_10)

        self.comboBox_function = QComboBox(self.widget_11)
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.comboBox_function.addItem("")
        self.comboBox_function.setObjectName(u"comboBox_function")
        self.comboBox_function.setMinimumSize(QSize(0, 25))
        font7 = QFont()
        font7.setBold(True)
        font7.setWeight(75)
        self.comboBox_function.setFont(font7)

        self.horizontalLayout_14.addWidget(self.comboBox_function)

        self.horizontalLayout_14.setStretch(0, 1)
        self.horizontalLayout_14.setStretch(1, 2)

        self.verticalLayout_8.addWidget(self.widget_11)


        self.horizontalLayout.addWidget(self.body_left_widget)

        self.body_right_widget = QWidget(self.body_widget)
        self.body_right_widget.setObjectName(u"body_right_widget")
        self.body_right_widget.setMaximumSize(QSize(750, 700))
        self.body_right_widget.setStyleSheet(u"")
        self.verticalLayout_10 = QVBoxLayout(self.body_right_widget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(10, 1, 10, 0)
        self.widget_21 = QWidget(self.body_right_widget)
        self.widget_21.setObjectName(u"widget_21")
        self.widget_21.setMaximumSize(QSize(700, 100))
        self.horizontalLayout_16 = QHBoxLayout(self.widget_21)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(10, 10, 10, 10)
        self.camara_show = QLabel(self.widget_21)
        self.camara_show.setObjectName(u"camara_show")
        self.camara_show.setFont(font1)

        self.horizontalLayout_16.addWidget(self.camara_show)

        self.open_camera_btn = QPushButton(self.widget_21)
        self.open_camera_btn.setObjectName(u"open_camera_btn")
        self.open_camera_btn.setMinimumSize(QSize(0, 30))
        self.open_camera_btn.setFont(font5)
        self.open_camera_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.open_camera_btn.setStyleSheet(u"background-color: rgb(39, 174, 96);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"border: 2px groove gray;\n"
"border-style: outset;")

        self.horizontalLayout_16.addWidget(self.open_camera_btn)

        self.widget_22 = QWidget(self.widget_21)
        self.widget_22.setObjectName(u"widget_22")
        self.widget_22.setMaximumSize(QSize(110, 16777215))

        self.horizontalLayout_16.addWidget(self.widget_22)

        self.language_btn = QPushButton(self.widget_21)
        self.language_btn.setObjectName(u"language_btn")
        self.language_btn.setMinimumSize(QSize(0, 30))
        self.language_btn.setFont(font5)
        self.language_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.language_btn.setStyleSheet(u"background-color: rgb(39, 174, 96);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"border: 2px groove gray;\n"
"border-style: outset;")

        self.horizontalLayout_16.addWidget(self.language_btn)

        self.horizontalLayout_16.setStretch(0, 2)
        self.horizontalLayout_16.setStretch(1, 2)
        self.horizontalLayout_16.setStretch(2, 5)
        self.horizontalLayout_16.setStretch(3, 2)

        self.verticalLayout_10.addWidget(self.widget_21)

        self.prompts_lab = QLabel(self.body_right_widget)
        self.prompts_lab.setObjectName(u"prompts_lab")
        self.prompts_lab.setMinimumSize(QSize(600, 50))
        self.prompts_lab.setMaximumSize(QSize(700, 50))
        font8 = QFont()
        font8.setPointSize(14)
        font8.setBold(True)
        font8.setWeight(75)
        self.prompts_lab.setFont(font8)
        self.prompts_lab.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.prompts_lab.setWordWrap(True)

        self.verticalLayout_10.addWidget(self.prompts_lab)

        self.widget_28 = QWidget(self.body_right_widget)
        self.widget_28.setObjectName(u"widget_28")
        self.widget_28.setMinimumSize(QSize(0, 400))
        self.widget_28.setMaximumSize(QSize(700, 400))
        self.horizontalLayout_20 = QHBoxLayout(self.widget_28)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.widget_29 = QWidget(self.widget_28)
        self.widget_29.setObjectName(u"widget_29")
        self.widget_29.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_20.addWidget(self.widget_29)

        self.show_camera_lab_rgb = QLabel(self.widget_28)
        self.show_camera_lab_rgb.setObjectName(u"show_camera_lab_rgb")
        self.show_camera_lab_rgb.setMinimumSize(QSize(320, 240))
        self.show_camera_lab_rgb.setMaximumSize(QSize(320, 240))
        self.show_camera_lab_rgb.setFont(font7)
        self.show_camera_lab_rgb.setCursor(QCursor(Qt.PointingHandCursor))
        self.show_camera_lab_rgb.setStyleSheet(u"")
        self.show_camera_lab_rgb.setAlignment(Qt.AlignCenter)
        self.show_camera_lab_rgb.setMargin(0)
        self.show_camera_lab_rgb.setIndent(1)

        self.horizontalLayout_20.addWidget(self.show_camera_lab_rgb)

        self.show_camera_lab_depth = QLabel(self.widget_28)
        self.show_camera_lab_depth.setObjectName(u"show_camera_lab_depth")
        self.show_camera_lab_depth.setMinimumSize(QSize(320, 240))
        self.show_camera_lab_depth.setMaximumSize(QSize(320, 240))

        self.horizontalLayout_20.addWidget(self.show_camera_lab_depth)

        self.widget_30 = QWidget(self.widget_28)
        self.widget_30.setObjectName(u"widget_30")
        self.widget_30.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_20.addWidget(self.widget_30)

        self.horizontalLayout_20.setStretch(0, 1)
        self.horizontalLayout_20.setStretch(1, 5)
        self.horizontalLayout_20.setStretch(2, 5)
        self.horizontalLayout_20.setStretch(3, 1)

        self.verticalLayout_10.addWidget(self.widget_28)

        self.widget_23 = QWidget(self.body_right_widget)
        self.widget_23.setObjectName(u"widget_23")
        self.widget_23.setMaximumSize(QSize(700, 16777215))
        self.verticalLayout_9 = QVBoxLayout(self.widget_23)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.widget_24 = QWidget(self.widget_23)
        self.widget_24.setObjectName(u"widget_24")
        self.horizontalLayout_17 = QHBoxLayout(self.widget_24)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(10, 10, 10, 10)
        self.connect_lab_3 = QLabel(self.widget_24)
        self.connect_lab_3.setObjectName(u"connect_lab_3")
        self.connect_lab_3.setFont(font4)

        self.horizontalLayout_17.addWidget(self.connect_lab_3)

        self.widget_25 = QWidget(self.widget_24)
        self.widget_25.setObjectName(u"widget_25")

        self.horizontalLayout_17.addWidget(self.widget_25)

        self.horizontalLayout_17.setStretch(0, 2)
        self.horizontalLayout_17.setStretch(1, 8)

        self.verticalLayout_9.addWidget(self.widget_24)

        self.widget_26 = QWidget(self.widget_23)
        self.widget_26.setObjectName(u"widget_26")
        self.horizontalLayout_18 = QHBoxLayout(self.widget_26)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(10, 10, 10, 10)
        self.current_coord_btn = QPushButton(self.widget_26)
        self.current_coord_btn.setObjectName(u"current_coord_btn")
        self.current_coord_btn.setMinimumSize(QSize(0, 30))
        self.current_coord_btn.setFont(font5)
        self.current_coord_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.current_coord_btn.setStyleSheet(u"background-color: rgb(39, 174, 96);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"border: 2px groove gray;\n"
"border-style: outset;")

        self.horizontalLayout_18.addWidget(self.current_coord_btn)

        self.cuttent_coord_lab = QLabel(self.widget_26)
        self.cuttent_coord_lab.setObjectName(u"cuttent_coord_lab")
        font9 = QFont()
        font9.setFamily(u"Arial")
        font9.setPointSize(15)
        font9.setBold(True)
        font9.setWeight(75)
        self.cuttent_coord_lab.setFont(font9)
        self.cuttent_coord_lab.setStyleSheet(u"")

        self.horizontalLayout_18.addWidget(self.cuttent_coord_lab)

        self.horizontalLayout_18.setStretch(0, 3)
        self.horizontalLayout_18.setStretch(1, 7)

        self.verticalLayout_9.addWidget(self.widget_26)

        self.widget_27 = QWidget(self.widget_23)
        self.widget_27.setObjectName(u"widget_27")
        self.horizontalLayout_19 = QHBoxLayout(self.widget_27)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(10, 10, 10, 10)
        self.image_coord_btn = QPushButton(self.widget_27)
        self.image_coord_btn.setObjectName(u"image_coord_btn")
        self.image_coord_btn.setMinimumSize(QSize(0, 30))
        self.image_coord_btn.setFont(font5)
        self.image_coord_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.image_coord_btn.setStyleSheet(u"background-color: rgb(39, 174, 96);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"border: 2px groove gray;\n"
"border-style: outset;")

        self.horizontalLayout_19.addWidget(self.image_coord_btn)

        self.img_coord_lab = QLabel(self.widget_27)
        self.img_coord_lab.setObjectName(u"img_coord_lab")
        self.img_coord_lab.setFont(font9)
        self.img_coord_lab.setStyleSheet(u"background-color: rgb(255, 255, 255\uff0c200);")

        self.horizontalLayout_19.addWidget(self.img_coord_lab)

        self.horizontalLayout_19.setStretch(0, 3)
        self.horizontalLayout_19.setStretch(1, 7)

        self.verticalLayout_9.addWidget(self.widget_27)


        self.verticalLayout_10.addWidget(self.widget_23)

        self.verticalLayout_10.setStretch(0, 1)
        self.verticalLayout_10.setStretch(1, 1)
        self.verticalLayout_10.setStretch(2, 9)
        self.verticalLayout_10.setStretch(3, 2)

        self.horizontalLayout.addWidget(self.body_right_widget)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 7)

        self.verticalLayout_11.addWidget(self.body_widget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout.addWidget(self.scrollArea)

        AiKit_UI.setCentralWidget(self.centralwidget)

        self.retranslateUi(AiKit_UI)

        self.connect_btn.setDefault(False)


        QMetaObject.connectSlotsByName(AiKit_UI)
    # setupUi

    def retranslateUi(self, AiKit_UI):
        AiKit_UI.setWindowTitle(QCoreApplication.translate("AiKit_UI", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("AiKit_UI", u"Elephant Robotics AI Kits", None))
        self.logo_lab.setText("")
        self.min_btn.setText("")
        self.max_btn.setText("")
        self.close_btn.setText("")
        self.connect_lab.setText(QCoreApplication.translate("AiKit_UI", u"Connection", None))
        self.connect_btn.setText(QCoreApplication.translate("AiKit_UI", u"CONNECT", None))
        self.port_lab.setText(QCoreApplication.translate("AiKit_UI", u"Serial Port", None))
        self.device_lab.setText(QCoreApplication.translate("AiKit_UI", u"Device", None))
        self.baud_lab.setText(QCoreApplication.translate("AiKit_UI", u"Baud", None))
        self.comboBox_port.setItemText(0, QCoreApplication.translate("AiKit_UI", u"no port", None))

        self.comboBox_device.setItemText(0, QCoreApplication.translate("AiKit_UI", u"myCobot 280 for Pi", None))
        self.comboBox_device.setItemText(1, QCoreApplication.translate("AiKit_UI", u"myCobot 280 for M5", None))
        self.comboBox_device.setItemText(2, QCoreApplication.translate("AiKit_UI", u"mechArm 270 for Pi", None))
        self.comboBox_device.setItemText(3, QCoreApplication.translate("AiKit_UI", u"mechArm 270 for M5", None))

        self.comboBox_baud.setItemText(0, QCoreApplication.translate("AiKit_UI", u"1000000", None))
        self.comboBox_baud.setItemText(1, QCoreApplication.translate("AiKit_UI", u"115200", None))

        self.func_lab.setText(QCoreApplication.translate("AiKit_UI", u"Control", None))
        self.func_lab_2.setText(QCoreApplication.translate("AiKit_UI", u"Homing", None))
        self.to_origin_btn.setText(QCoreApplication.translate("AiKit_UI", u"Go", None))
        self.func_lab_4.setText(QCoreApplication.translate("AiKit_UI", u"Recognition", None))
        self.discern_btn.setText(QCoreApplication.translate("AiKit_UI", u"Run", None))
        self.func_lab_5.setText(QCoreApplication.translate("AiKit_UI", u"Algorithm:", None))
        self.algorithm_lab.setText(QCoreApplication.translate("AiKit_UI", u"Algorithm:", None))
        self.func_lab_7.setText(QCoreApplication.translate("AiKit_UI", u"Pick", None))
        self.crawl_btn.setText(QCoreApplication.translate("AiKit_UI", u"Run", None))
        self.label.setText("")
        self.func_lab_9.setText(QCoreApplication.translate("AiKit_UI", u"Algorithm", None))
        self.func_lab_10.setText(QCoreApplication.translate("AiKit_UI", u"Select", None))
        self.comboBox_function.setItemText(0, QCoreApplication.translate("AiKit_UI", u"Color recognition", None))
        self.comboBox_function.setItemText(1, QCoreApplication.translate("AiKit_UI", u"Shape recognition", None))
        self.comboBox_function.setItemText(2, QCoreApplication.translate("AiKit_UI", u"Keypoints", None))
        self.comboBox_function.setItemText(3, QCoreApplication.translate("AiKit_UI", u"yolov5", None))

        self.camara_show.setText(QCoreApplication.translate("AiKit_UI", u"Camera", None))
        self.open_camera_btn.setText(QCoreApplication.translate("AiKit_UI", u"Open", None))
        self.language_btn.setText(QCoreApplication.translate("AiKit_UI", u"\u7b80\u4f53\u4e2d\u6587", None))
        self.prompts_lab.setText("")
        self.show_camera_lab_rgb.setText("")
        self.show_camera_lab_depth.setText("")
        self.connect_lab_3.setText(QCoreApplication.translate("AiKit_UI", u"Display", None))
        self.current_coord_btn.setText(QCoreApplication.translate("AiKit_UI", u"  current coordinates", None))
        self.cuttent_coord_lab.setText("")
        self.image_coord_btn.setText(QCoreApplication.translate("AiKit_UI", u"  image coordinates", None))
        self.img_coord_lab.setText("")
    # retranslateUi

