# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cambiar_foto.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor


class Ui_ActualizarFoto(object):
    def setupUi(self, ActualizarFoto):
        ActualizarFoto.setObjectName("ActualizarFoto")
        ActualizarFoto.resize(237, 254)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/imagenes/lapiz_editar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ActualizarFoto.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(ActualizarFoto)
        self.gridLayout.setObjectName("gridLayout")
        self.lay_ver_principal = QtWidgets.QVBoxLayout()
        self.lay_ver_principal.setObjectName("lay_ver_principal")
        self.lbl_actualizarFoto = QtWidgets.QLabel(ActualizarFoto)
        self.lbl_actualizarFoto.setStyleSheet("font: 11pt \"Gill Sans MT\";")
        self.lbl_actualizarFoto.setObjectName("lbl_actualizarFoto")
        self.lay_ver_principal.addWidget(self.lbl_actualizarFoto)
        self.lbl_foto_cliente = QtWidgets.QLabel(ActualizarFoto)
        self.lbl_foto_cliente.setMinimumSize(QtCore.QSize(217, 178))
        self.lbl_foto_cliente.setMaximumSize(QtCore.QSize(217, 178))
        self.lbl_foto_cliente.setStyleSheet("background-color: rgba(0,0,0,0);\n"
"border: 2px solid rgba(0, 0, 0, 255);\n"
"border-radius:20px;\n"
"padding:10px 20px 10px 20px;")
        self.lbl_foto_cliente.setText("")
        self.lbl_foto_cliente.setPixmap(QtGui.QPixmap(":/imagenes/agregar.png"))
        self.lbl_foto_cliente.setScaledContents(True)
        self.lbl_foto_cliente.setObjectName("lbl_foto_cliente")
        self.label_foto = ClickableLabel(self.lbl_foto_cliente)
        self.label_foto.setFixedSize(217, 178)
        self.lay_ver_principal.addWidget(self.lbl_foto_cliente)
        self.btn_agregar_nueva_foto = QtWidgets.QPushButton(ActualizarFoto)
        self.btn_agregar_nueva_foto.setObjectName("btn_agregar_nueva_foto")
        self.lay_ver_principal.addWidget(self.btn_agregar_nueva_foto)
        self.gridLayout.addLayout(self.lay_ver_principal, 0, 0, 1, 1)

        self.retranslateUi(ActualizarFoto)
        QtCore.QMetaObject.connectSlotsByName(ActualizarFoto)

    def retranslateUi(self, ActualizarFoto):
        _translate = QtCore.QCoreApplication.translate
        ActualizarFoto.setWindowTitle(_translate("ActualizarFoto", "Actualizar Foto"))
        self.lbl_actualizarFoto.setText(_translate("ActualizarFoto", "Actualizar Foto:"))
        self.btn_agregar_nueva_foto.setText(_translate("ActualizarFoto", "Agregar"))
from gimnasio.images import imagenes_rc

class ClickableLabel(QLabel):
    """
    Clase para convertir un label a clickeable
    """
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.clicked.emit()
        
    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, event):
        self.unsetCursor()             
      