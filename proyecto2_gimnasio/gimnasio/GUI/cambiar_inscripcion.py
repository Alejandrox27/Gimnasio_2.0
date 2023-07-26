# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cambiar_inscripcion.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Ingresar_inscripcion(object):
    def setupUi(self, Ingresar_inscripcion):
        Ingresar_inscripcion.setObjectName("Ingresar_inscripcion")
        Ingresar_inscripcion.resize(323, 114)
        Ingresar_inscripcion.setMinimumSize(QtCore.QSize(323, 114))
        Ingresar_inscripcion.setMaximumSize(QtCore.QSize(323, 114))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/imagenes/lapiz_editar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Ingresar_inscripcion.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Ingresar_inscripcion)
        self.gridLayout.setObjectName("gridLayout")
        self.lay_ver_principal = QtWidgets.QVBoxLayout()
        self.lay_ver_principal.setObjectName("lay_ver_principal")
        self.lbl_ingrese_nueva_inscripcion = QtWidgets.QLabel(Ingresar_inscripcion)
        self.lbl_ingrese_nueva_inscripcion.setStyleSheet("font: 11pt \"Gill Sans MT\";")
        self.lbl_ingrese_nueva_inscripcion.setObjectName("lbl_ingrese_nueva_inscripcion")
        self.lay_ver_principal.addWidget(self.lbl_ingrese_nueva_inscripcion)
        self.lay_hor_objetivos = QtWidgets.QHBoxLayout()
        self.lay_hor_objetivos.setObjectName("lay_hor_objetivos")
        self.rdb_dia = QtWidgets.QRadioButton(Ingresar_inscripcion)
        self.rdb_dia.setStyleSheet("QRadioButton {\n"
"  background-color: transparent;\n"
"  padding: 4px;\n"
"  color: #333333;\n"
"font: 9pt \"Gill Sans MT\";\n"
"}\n"
"QRadioButton::indicator {\n"
"  width: 12px;\n"
"  height: 12px;\n"
"  border-radius: 5px;\n"
"}\n"
"\n"
"QRadioButton:indicator:checked:hover{\n"
"  background-color: rgb(34, 34, 255);\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"  border: 1px solid #999999;\n"
"  background-color: #FFFFFF;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover:unchecked {\n"
"  border: 1px solid rgb(32, 54, 255);\n"
"  background-color: #FFFFFF;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"  border: 1px solid rgb(0, 0, 0);\n"
"  background-color: rgb(139, 49, 184);\n"
"} ")
        self.rdb_dia.setObjectName("rdb_dia")
        self.btn_group_inscripcion = QtWidgets.QButtonGroup(Ingresar_inscripcion)
        self.btn_group_inscripcion.setObjectName("btn_group_inscripcion")
        self.btn_group_inscripcion.addButton(self.rdb_dia)
        self.lay_hor_objetivos.addWidget(self.rdb_dia)
        self.rdb_mes = QtWidgets.QRadioButton(Ingresar_inscripcion)
        self.rdb_mes.setStyleSheet("QRadioButton {\n"
"  background-color: transparent;\n"
"  padding: 4px;\n"
"  color: #333333;\n"
"font: 9pt \"Gill Sans MT\";\n"
"}\n"
"QRadioButton::indicator {\n"
"  width: 12px;\n"
"  height: 12px;\n"
"  border-radius: 5px;\n"
"}\n"
"\n"
"QRadioButton:indicator:checked:hover{\n"
"  background-color: rgb(34, 34, 255);\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"  border: 1px solid #999999;\n"
"  background-color: #FFFFFF;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover:unchecked {\n"
"  border: 1px solid rgb(32, 54, 255);\n"
"  background-color: #FFFFFF;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"  border: 1px solid rgb(0, 0, 0);\n"
"  background-color: rgb(139, 49, 184);\n"
"} ")
        self.rdb_mes.setObjectName("rdb_mes")
        self.btn_group_inscripcion.addButton(self.rdb_mes)
        self.lay_hor_objetivos.addWidget(self.rdb_mes)
        self.rdb_anual = QtWidgets.QRadioButton(Ingresar_inscripcion)
        self.rdb_anual.setStyleSheet("QRadioButton {\n"
"  background-color: transparent;\n"
"  padding: 4px;\n"
"  color: #333333;\n"
"font: 9pt \"Gill Sans MT\";\n"
"}\n"
"QRadioButton::indicator {\n"
"  width: 12px;\n"
"  height: 12px;\n"
"  border-radius: 5px;\n"
"}\n"
"\n"
"QRadioButton:indicator:checked:hover{\n"
"  background-color: rgb(34, 34, 255);\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"  border: 1px solid #999999;\n"
"  background-color: #FFFFFF;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover:unchecked {\n"
"  border: 1px solid rgb(32, 54, 255);\n"
"  background-color: #FFFFFF;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"  border: 1px solid rgb(0, 0, 0);\n"
"  background-color: rgb(139, 49, 184);\n"
"} ")
        self.rdb_anual.setObjectName("rdb_anual")
        self.btn_group_inscripcion.addButton(self.rdb_anual)
        self.lay_hor_objetivos.addWidget(self.rdb_anual)
        self.lay_ver_principal.addLayout(self.lay_hor_objetivos)
        self.btn_agregar_inscripcion = QtWidgets.QPushButton(Ingresar_inscripcion)
        self.btn_agregar_inscripcion.setObjectName("btn_agregar_inscripcion")
        self.lay_ver_principal.addWidget(self.btn_agregar_inscripcion)
        self.gridLayout.addLayout(self.lay_ver_principal, 0, 0, 1, 1)

        self.retranslateUi(Ingresar_inscripcion)
        QtCore.QMetaObject.connectSlotsByName(Ingresar_inscripcion)

    def retranslateUi(self, Ingresar_inscripcion):
        _translate = QtCore.QCoreApplication.translate
        Ingresar_inscripcion.setWindowTitle(_translate("Ingresar_inscripcion", "Nueva inscripción"))
        self.lbl_ingrese_nueva_inscripcion.setText(_translate("Ingresar_inscripcion", "Ingrese la nueva inscripción:"))
        self.rdb_dia.setText(_translate("Ingresar_inscripcion", "DIA"))
        self.rdb_mes.setText(_translate("Ingresar_inscripcion", "MES"))
        self.rdb_anual.setText(_translate("Ingresar_inscripcion", "AÑO"))
        self.btn_agregar_inscripcion.setText(_translate("Ingresar_inscripcion", "Agregar"))
