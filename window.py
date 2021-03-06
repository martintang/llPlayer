# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(658, 503)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 12))
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.progress_slider = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_slider.sizePolicy().hasHeightForWidth())
        self.progress_slider.setSizePolicy(sizePolicy)
        self.progress_slider.setOrientation(QtCore.Qt.Horizontal)
        self.progress_slider.setObjectName("progress_slider")
        self.gridLayout.addWidget(self.progress_slider, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start_pause_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_pause_btn.setObjectName("start_pause_btn")
        self.horizontalLayout.addWidget(self.start_pause_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.prev_btn = QtWidgets.QPushButton(self.centralwidget)
        self.prev_btn.setEnabled(False)
        self.prev_btn.setObjectName("prev_btn")
        self.horizontalLayout.addWidget(self.prev_btn)
        self.next_btn = QtWidgets.QPushButton(self.centralwidget)
        self.next_btn.setEnabled(False)
        self.next_btn.setObjectName("next_btn")
        self.horizontalLayout.addWidget(self.next_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.show_mask = QtWidgets.QCheckBox(self.centralwidget)
        self.show_mask.setObjectName("show_mask")
        self.horizontalLayout.addWidget(self.show_mask)
        self.image_stretch = QtWidgets.QCheckBox(self.centralwidget)
        self.image_stretch.setObjectName("image_stretch")
        self.horizontalLayout.addWidget(self.image_stretch)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 658, 23))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        MainWindow.setMenuBar(self.menubar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.menu_file.addAction(self.action_open)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(MainWindow)
        self.prev_btn.clicked.connect(MainWindow.prev_sentence)
        self.next_btn.clicked.connect(MainWindow.next_sentence)
        self.action_open.triggered.connect(MainWindow.open_file)
        self.show_mask.stateChanged['int'].connect(MainWindow.is_show_mask)
        self.progress_slider.valueChanged['int'].connect(MainWindow.move_to)
        self.progress_slider.sliderReleased.connect(MainWindow.start_here)
        self.progress_slider.sliderPressed.connect(MainWindow.slider_press)
        self.start_pause_btn.clicked.connect(MainWindow.start_pause)
        self.image_stretch.stateChanged['int'].connect(MainWindow.is_image_stretch)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "llPlayer"))
        self.label.setText(_translate("MainWindow", "首次加载视频，后台会进行音频断句分析，分析完后“上一句”和“下一句”可用。"))
        self.start_pause_btn.setText(_translate("MainWindow", "开始"))
        self.prev_btn.setText(_translate("MainWindow", "上一句"))
        self.next_btn.setText(_translate("MainWindow", "下一句"))
        self.show_mask.setText(_translate("MainWindow", "遮罩"))
        self.image_stretch.setText(_translate("MainWindow", "画面拉伸"))
        self.menu_file.setTitle(_translate("MainWindow", "&File"))
        self.action_open.setText(_translate("MainWindow", "&Open"))
