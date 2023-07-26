import sys
import sqlite3
import pickle
import markdown
from datetime import datetime

from gimnasio.modelos.Clientes import Clientes
from gimnasio.modelos.Cliente import Cliente

import os
import re

from .GUI.gimnasio_principal import Ui_Gimnasio
from .GUI.agregar_cliente import Ui_Agregar_cliente
from .GUI.remover_cliente import Ui_Clientes_remover
from .GUI.cambiar_info_cliente import Ui_Cambiar_info_cliente
from .GUI.buscar_informacion import Ui_Buscar_informacion_cliente
from .GUI.entrar_gimnasio import Ui_Entrar_gimnasio

from .GUI.cambiar_objetivo import Ui_Ingresar_objetivo
from .GUI.cambiar_patologias import Ui_ActualizarPatologias
from .GUI.cambiar_inscripcion import Ui_Ingresar_inscripcion
from .GUI.cambiar_foto import Ui_ActualizarFoto

from PyQt5.QtWidgets import (QMainWindow, QWidget,QDialog, QApplication,QFileDialog, QInputDialog,
                             QMessageBox,QLabel, QVBoxLayout, QTreeView, QPushButton, QFileSystemModel)
from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QDate, QTime, QDateTime, QTimer, QUrl, QThread
from PyQt5.QtGui import QPixmap, QIntValidator, QCursor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent

class Gimnasio(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.clientes = Clientes()
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_Gimnasio()
        self.ui.setupUi(self)
        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        
        self.ui.mni_agregar_nuevo.triggered.connect(self.agregar_nuevo_cliente)
        self.ui.mni_remover.triggered.connect(self.remover_cliente)
        self.ui.mni_cambiar_info_cliente.triggered.connect(self.cambiar_info_cliente)
        self.ui.mni_consultar_cliente.triggered.connect(self.buscar_info_cliente)
        self.ui.mni_entrar.triggered.connect(self.entrar_gimnasio)
        self.ui.mni_creador.triggered.connect(self.creador)
        self.ui.mni_version.triggered.connect(self.version)
        self.ui.mni_guardar.triggered.connect(self.guardar_datos_gui)
        self.ui.mni_cargar.triggered.connect(self.cargar_datos_gui)
        self.ui.mni_salir.triggered.connect(self.close)
        
        self.show()
        
    def cargar_imagenes_cache(self):
        self.imagenes_cache_thread = CargarImagenesCacheThread(self.clientes)
        self.imagenes_cache_thread.start()
    
    def agregar_nuevo_cliente(self):
        self.gui = Agregar_cliente(self.clientes)
        self.ui.mdi_principal.addSubWindow(self.gui)
        self.gui.show()
        
    def remover_cliente(self):
        self.gui = Remover_cliente(self.clientes)
        self.ui.mdi_principal.addSubWindow(self.gui)
        self.gui.show()
        
    def cambiar_info_cliente(self):
        self.gui = Cambiar_info_cliente(self.clientes)
        self.ui.mdi_principal.addSubWindow(self.gui)
        self.gui.show()
        
    def buscar_info_cliente(self):
        self.gui = Buscar_info_cliente(self.clientes)
        self.ui.mdi_principal.addSubWindow(self.gui)
        self.gui.show()
        
    def entrar_gimnasio(self):
        self.gui = Entrar_gimnasio(self.clientes)
        self.ui.mdi_principal.addSubWindow(self.gui)
        self.gui.show()
        
    def creador(self):
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle('Creador')
        mensaje.setText(markdown.markdown('Programa creador por **Aleandro mejia**'))
        mensaje.setIcon(QMessageBox.Information)
        mensaje.exec_()
    
    def version(self):
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle('Versión')
        mensaje.setText(markdown.markdown('Programa hecho en **PyQt5**\n\nVersión: **2.0**'))
        mensaje.setIcon(QMessageBox.Information)
        mensaje.exec_()
    
    def guardar_datos_gui(self):
        """
        función que permite guardar los datos de los clientes
        de una base de datos seleccionada o una nueva.
        """
        confirmacion = QMessageBox()
        texto = '¿Quiere guardar los datos de los clientes?'
        confirmacion.setText(texto)
        confirmacion.setIcon(QMessageBox.Question)
        confirmacion.setWindowTitle('Guardar')
        confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        boton_yes = confirmacion.button(QMessageBox.Yes)
        
        confirmacion.exec_()
        
        if confirmacion.clickedButton() == boton_yes:
            self.gui = ExploradorArchivosGuardar(self.clientes)
            self.gui.show()

    def cargar_datos_gui(self):
        """
        función que permite cargar los datos de los clientes
        de una base de datos seleccionada.
        """
        confirmacion = QMessageBox()
        texto = '¿Quiere cargar los datos de los clientes?'
        confirmacion.setText(texto)
        confirmacion.setIcon(QMessageBox.Question)
        confirmacion.setWindowTitle('Guardar')
        confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        boton_yes = confirmacion.button(QMessageBox.Yes)
        
        confirmacion.exec_()
        
        if confirmacion.clickedButton() == boton_yes:
            self.gui = ExploradorArchivosCargar()
            self.gui.show()
            
            
            self.gui.treeview.doubleClicked.connect(self.archivo_seleccionado)
        else:  
            return False
    
    def archivo_seleccionado(self, index: QModelIndex):
        """
        función que toma el index del archivo seleccionado,
        lo convierte en una ruta y se conecta a una base de datos,
        en donde seguido se cargan los datos en una lista de clientes
        y en un diccionario de promedios.
        """
        self.clientes.clientes.clear()
        
        self.ruta_seleccionada = self.gui.model.filePath(index)
        
        conexion = sqlite3.connect(self.ruta_seleccionada)
        cursor = conexion.cursor()
        sql = 'SELECT * FROM clientes'
        clientes = cursor.execute(sql)
        
        for e in clientes:
            cliente = {'id': 0, 'nombre': '', 'objetivo': '', 'patologias': '', 'inscripcion': None, 'fecha_final': None, 'permiso': None, 'foto': None}
            for i, c in enumerate(e):
                if i == 0:
                    cliente['id'] = c
                if i == 1:
                    cliente['nombre'] = c
                if i == 2:
                    cliente['objetivo'] = c
                if i == 3:
                    cliente['patologias'] = c
                if i == 4:
                    cliente['inscripcion'] = c
                if i == 5:
                    cliente['fecha_final'] = c
                if i == 6:
                    cliente['permiso'] = c
                if i == 7:
                    cliente['foto'] = c
                    
            cliente = Cliente(cliente['nombre'], str(cliente['id']), cliente['objetivo'], cliente['patologias'],
                              cliente['inscripcion'],cliente['fecha_final'], cliente['permiso'], cliente['foto'])
            
            self.clientes.agregar_clientes(cliente)
        
        self.cargar_imagenes_cache()
            
        self.gui.close()
        
    def closeEvent(self, event):
        """
        función que detecta el evento de cerrar la ventana,
        sí la ventana se cierra se inicializa la función 'guardar_datos_gui',
        para posteriormente cerrarse la ventana.
        """
        
        if len(self.clientes.clientes):
            if self.guardar_datos_gui():
                self.close()

class CargarImagenThread(QThread):
    imageLoaded = pyqtSignal(QPixmap)

    def __init__(self, archivo):
        super().__init__()
        self.archivo = archivo

    def run(self):
        pixmap = QPixmap(self.archivo)
        self.imageLoaded.emit(pixmap)                  

class CargarImagenesCacheThread(QThread):
    imagesLoaded = pyqtSignal()

    def __init__(self, clientes):
        super().__init__()
        self.clientes = clientes

    def run(self):
        for c in self.clientes.clientes:
            self.clientes.convertir_a_normal(c.foto)
        self.imagesLoaded.emit()

class ExploradorArchivosGuardar(QWidget):
    def __init__(self, clientes):
        super().__init__()
        self.clientes = clientes
        self.inicializarGui()
        
    def inicializarGui(self):
        """
        Inicializa la ventana de guardar archivo en base de datos.
        """
        self.setWindowTitle('Guardar en...')
        self.setFixedSize(400, 360)
        
        ruta_absoluta = str(os.path.abspath('gimnasio/database'))
        ruta_absoluta = ruta_absoluta.replace("\\", "/")
        
        layout = QVBoxLayout(self)
        
        self.treeview = QTreeView(self)
        self.model = QFileSystemModel()
        self.model.setRootPath(ruta_absoluta)
        self.treeview.setModel(self.model)
        self.treeview.setRootIndex(self.model.index(self.model.rootPath()))
        
        layout.addWidget(self.treeview)
        
        self.treeview.doubleClicked.connect(self.archivo_seleccionado)
        
        boton = QPushButton('Nuevo', self)
        boton.clicked.connect(self.nuevo)
        layout.addWidget(boton)
        
    def archivo_seleccionado(self, index: QModelIndex):
        ruta_seleccionada = self.model.filePath(index)
        
        self.guardar_datos_en_base(ruta_seleccionada)
        
    def nuevo(self):
        """
        Crea una nueva base de datos con el nombre que le coloque el usuario,
        crea una tabla de 'clientes' sí la base no está creada aún
        y solo agrega los datos sí ya está creada.
        """
        patron = r'[a-zA-Z]+'
        regex = re.compile(patron)
        nombre, ok = QInputDialog.getText(self, 'Guardar datos...','Escriba el nombre del archivo donde se guardará la información')
        
        if ok:
            nombre = nombre.strip()
            if len(nombre) == 0:
                mensaje = QMessageBox()
                mensaje.setText('Inserte un nombre para su base de datos')
                mensaje.setIcon(QMessageBox.Warning)
                mensaje.setWindowTitle('Guardar')
                mensaje.exec_()
                self.guadar_datos_gui(self.clientes)
                return
            
            if regex.match(nombre):
                
                nombre_archivo = f'gimnasio/database/{nombre}.db'
                
            else:
                mensaje = QMessageBox()
                mensaje.setText('Inserte un nombre valido para su base de datos')
                mensaje.setIcon(QMessageBox.Warning)
                mensaje.setWindowTitle('Guardar')
                mensaje.exec_()
                self.guardar_datos_gui(self.clientes)
                return
                
            
            if not os.path.exists(nombre_archivo):
                try:
                    conexion = sqlite3.connect(nombre_archivo)
                    cursor = conexion.cursor()
                    sql_clientes = '''CREATE TABLE clientes (
                        ID INTEGER PRIMARY KEY NOT NULL,
                        nombre TEXT NOT NULL,
                        objetivo TEXT NOT NULL,
                        patologias TEXT,
                        inscripcion TEXT,
                        fechaFinal TEXT,
                        permiso TEXT,
                        foto BLOB NOT NULL
                        )'''
                    cursor.execute(sql_clientes)
                    
                    for e in self.clientes.clientes:
                        id = int(e.identidad)
                        nombre = str(e.nombre)
                        objetivo = str(e.objetivo)
                        patologias = str(e.patologias)
                        inscripcion = str(e.inscripcion)
                        fecha_final = str(e.fecha_final)
                        permiso = str(e.permiso)
                        foto = e.foto
                        
                        sql_guardar = "INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                        cursor.execute(sql_guardar, (id, nombre, objetivo, patologias, inscripcion, fecha_final, permiso, foto))
                    
                    cursor.close()
                    conexion.commit()
                    return True
                
                except sqlite3.Error:
                    mensaje = QMessageBox()
                    mensaje.setIcon(QMessageBox.Warning)
                    mensaje.setWindowTitle('Error')
                    mensaje.setText('hubo un error en la creación de base de datos')
                    mensaje.exec_()
                
                finally:
                    conexion.close()
                    self.close()
            else:
                self.guardar_datos_en_base(nombre_archivo)
        
    def guardar_datos_en_base(self, nombre_archivo):
        """
        Guarda los datos de los clientes en una
        base de datos ya creada.
        
        Parameters:
        nombre_archivo = Nombre de la base de datos
        """
        try: 
                    
            conexion = sqlite3.connect(nombre_archivo)
            cursor = conexion.cursor()
            
            sql_borrar = "DELETE FROM clientes"
            cursor.execute(sql_borrar).fetchall()
        
            for e in self.clientes.clientes:
                id = int(e.identidad)
                nombre = str(e.nombre)
                objetivo = str(e.objetivo)
                patologias = str(e.patologias)
                inscripcion = str(e.inscripcion)
                fecha_final = str(e.fecha_final)
                permiso = str(e.permiso)
                foto = e.foto
                
                sql_guardar = "INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(sql_guardar, (id, nombre, objetivo, patologias, inscripcion, fecha_final, permiso, foto))
            
            cursor.close()
            conexion.commit()
        
        except sqlite3.Error:
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Warning)
            mensaje.setWindowTitle('Error')
            mensaje.setText('hubo un error en la creación de base de datos')
            mensaje.exec_()
        
        finally:
            conexion.close()
            self.close()
     
class ExploradorArchivosCargar(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_seleccionada = None
        self.inicializarGui()
        
    def inicializarGui(self):
        """
        Inicializa la ventana de cargar con base de datos
        """
        self.setWindowTitle('Cargar con...')
        self.setFixedSize(400, 360)
        
        ruta_absoluta = str(os.path.abspath('gimnasio/database'))
        ruta_absoluta = ruta_absoluta.replace("\\", "/")
        
        layout = QVBoxLayout(self)
        
        self.treeview = QTreeView(self)
        self.model = QFileSystemModel()
        self.model.setRootPath(ruta_absoluta)
        self.treeview.setModel(self.model)
        self.treeview.setRootIndex(self.model.index(self.model.rootPath()))
        
        layout.addWidget(self.treeview)
                
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
                
class Agregar_cliente(QWidget):
    def __init__(self, clientes):
        super().__init__()
        
        patron = r'^[A-Za-z\s]+$'
        self.regex = re.compile(patron)
        
        self.clientes = clientes
        self.inicializarGui()    
    
    def inicializarGui(self):
        self.ui = Ui_Agregar_cliente()
        self.ui.setupUi(self)  
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setWindowTitle('Mensaje')
        
        self.ui.txt_cedula_ti_2.setValidator(QIntValidator(10000000, 999999999, self))
        
        self.default_pixmap = self.ui.lbl_foto_cliente_2.pixmap()
        
        self.objetivo = None
        
        self.ui.btn_group_objetivo.buttonClicked.connect(self.opcion_seleccionada)
        
        self.ui.btn_agregar_cliente.clicked.connect(self.agregar_cliente)
        
        label = ClickableLabel(self.ui.lbl_foto_cliente_2)
        label.setFixedSize(217, 178)
        label.clicked.connect(self.abrir_foto)
      
    def abrir_foto(self):
        """
        Función que permite al usuario elegir una imagen
        de su computadora y agregarla al 'lbl_foto_agregar'
        para luego ser usada para agregarla en base de datos.
        """
        self.archivo, ok = QFileDialog.getOpenFileName(self, 'Seleccionar archivo de imagen...', 'C:\\','Archivos de imágenes (*.jpg *.png)')
        
        if ok:
            #self.ui.lbl_foto_cliente_2.setPixmap(QPixmap(self.archivo))
            self.mostrar_imagen_subproceso()
    
    def mostrar_imagen_subproceso(self):
        self.cargar_imagen_thread = CargarImagenThread(self.archivo)
        self.cargar_imagen_thread.imageLoaded.connect(self.mostrar_imagen_cargada)
        self.cargar_imagen_thread.start()
    
    def mostrar_imagen_cargada(self, pixmap):
        self.ui.lbl_foto_cliente_2.setPixmap(pixmap)
      
    def agregar_cliente(self):
        nombre = self.ui.txt_nombre_2.text().strip()
        id = self.ui.txt_cedula_ti_2.text()
        
        current_pixmap = self.ui.lbl_foto_cliente_2.pixmap()
        
        if self.ui.txt_otro_objetivo.isEnabled():
            self.objetivo = self.ui.txt_otro_objetivo.text().strip()
        
        if len(nombre) == 0:
            self.mensaje.setText('El campo nombre es obligatorio')
            self.mensaje.exec_()
            return
        
        if self.espacios_seguidos(nombre):
            self.mensaje.setText('El campo nombre no puede tener dos espacios seguidos')
            self.mensaje.exec_()
            return
        
        if not self.regex.match(nombre):
            self.mensaje.setText('El campo nombre no está bien escrito')
            self.mensaje.exec_()
            return
        
        if len(id) == 0:
            self.mensaje.setText('El campo Cedula/T.I es obligatorio')
            self.mensaje.exec_()
            return
        
        cliente = self.clientes.buscar_cliente(id)
        
        if cliente:
            self.mensaje.setText('Ya existe un cliente con ese numero de identidad, inserte otro.')
            self.mensaje.exec_()
            return
        
        if self.objetivo is None:
            self.mensaje.setText('Debes elegir un objetivo.')
            self.mensaje.exec_()
            return
        
        if not self.regex.match(self.objetivo):
            self.mensaje.setText('El objetivo no está bien escrito')
            self.mensaje.exec_()
            return
        
        if self.ui.txt_otro_objetivo.text().strip() == 0 and self.ui.btn_group_objetivo.checkedButton() is None:
            self.mensaje.setText('Debe elegir un objetivo de entre las opciones o agregar otro')
            self.mensaje.exec_()
            return
        
        if self.ui.btn_group_inscripcion.checkedButton() is None:
            self.mensaje.setText('Debe elegir un tipo de inscripción de entre las opciones')
            self.mensaje.exec_()
            return
        
        if current_pixmap.isNull() or current_pixmap.toImage() == self.default_pixmap.toImage():
            self.mensaje.setText('Agrega una imagen')
            self.mensaje.exec_()
            return
        
        patologias = self.ui.txt_patologias_2.toPlainText()
        inscripcion = self.ui.btn_group_inscripcion.checkedButton()
        
        if inscripcion is not None:
            inscripcion = inscripcion.text()
        
        fecha_final = self.clientes.comprobar_fecha_final(inscripcion)
        
        self.foto = self.clientes.convertir_a_binario(self.archivo)
        
        permiso = True
        
        nuevo_cliente = Cliente(nombre, id, str(self.objetivo), str(patologias), str(inscripcion), fecha_final , permiso , self.foto)
        self.clientes.agregar_clientes(nuevo_cliente)
        
        self.mensaje.setText('El cliente ha sido agregado con exito')
        self.mensaje.setIcon(QMessageBox.Information)
        self.mensaje.exec_()
    
    def espacios_seguidos(self, string):
        """
        Esta función toma un string y verifica si hay dos o más espacios seguidos en él.

        Parameters:
        string (str): Texto en el que se quiere buscar espacios seguidos.

        Returns:
        bool: True si encuentra dos o más espacios seguidos en el string, False en caso contrario.
        """

        for i in range(len(string) - 1):
            if string[i] == string[i + 1] == ' ':
                return True

        return False
    
    def opcion_seleccionada(self):
        self.ui.txt_otro_objetivo.setText('')
        self.ui.txt_otro_objetivo.setEnabled(False)
        self.objetivo = self.ui.btn_group_objetivo.checkedButton()
        if self.objetivo is not None:
            self.objetivo = self.objetivo.text()
    
class Remover_cliente(QWidget):
    def __init__(self, clientes):
        super().__init__()
        
        self.clientes = clientes
        
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_Clientes_remover()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setWindowTitle('mensaje')
        
        self.ui.txt_codigo_cliente.setValidator(QIntValidator(10000000, 999999999, self))
        
        self.ui.btn_remover_cliente.clicked.connect(self.remover_cliente)
    
    def remover_cliente(self):
        codigo = self.ui.txt_codigo_cliente.text()
        
        if len(codigo) == 0:
            self.mensaje.setText('El campo codigo es obligatorio')
            self.mensaje.exec_()
            return
        
        cliente = self.clientes.buscar_cliente(codigo)
        
        if cliente is None:
            self.mensaje.setText('No existe un cliente con ese codigo')
            self.mensaje.exec_()
            return
        
        foto_cliente = self.clientes.convertir_a_normal(cliente.foto)
        foto_cliente = foto_cliente.scaled(100, 100)
        nombre_cliente = cliente.nombre
        id = cliente.identidad
        
        confirmacion = QMessageBox(self)
        confirmacion.setText(markdown.markdown(f'¿Quiere eliminar al cliente \n\n**{nombre_cliente}**\n\nde número de identidad: **{id}**?'))
        confirmacion.setIconPixmap(foto_cliente)
        confirmacion.setWindowTitle('Remover')
        confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        boton_yes = confirmacion.button(QMessageBox.Yes)
        
        confirmacion.exec_()
        
        if confirmacion.clickedButton() == boton_yes:
            self.clientes.eliminar_cliente(cliente)
            
            self.mensaje.setText('Se ha eliminado el cliente')
            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.exec_()
        
class Cambiar_info_cliente(QWidget):
    def __init__(self, clientes):
        super().__init__()
        
        patron = r'^[A-Za-z\s]+$'
        self.regex = re.compile(patron)
        
        self.clientes = clientes
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_Cambiar_info_cliente()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setWindowTitle('mensaje')
        
        self.ui.txt_identidad_cedula.setValidator(QIntValidator(10000000, 999999999, self))
        
        self.ui.btn_nombre.clicked.connect(self.cambiar_nombre)
        self.ui.btn_id.clicked.connect(self.cambiar_id)
        self.ui.btn_objetivo.clicked.connect(self.cambiar_objetivo)
        self.ui.btn_patologias.clicked.connect(self.cambiar_patologias)
        self.ui.btn_inscripcion.clicked.connect(self.cambiar_inscripcion)
        self.ui.btn_foto.clicked.connect(self.cambiar_foto)
        
    def espacios_seguidos(self, string):
        """
        Esta función toma un string y pasa por cada uno de sus elementos,
        sí hay dos o más espacios seguidos en el string devuelve True,
        si no hay más de dos espacios seguidos en el string devuelve False.
        
        Parameters:
        string: texto que se quiere buscar espacios seguidos
        
        Returns:
        True: si encuentra dos o más espacios seguidos en el string
        False: si no encuentra dos o más espacios seguidos
        """
        
        lista_texto = []
        for l in string:
            lista_texto.append(l)
        index1 = ''
        index2 = ''
        
        for e in lista_texto:
            index1 = e
            if index1 == index2 and index1 == ' ':
                return True
            index2 = e
        return False
        
    def cambiar_nombre(self):
        identidad = self.ui.txt_identidad_cedula.text()
        
        if len(identidad) == 0:
            self.mensaje.setText('Inserte el codigo del cliente a actualizar sus datos')
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        cliente = self.clientes.buscar_cliente(identidad)
        
        if cliente is None:
            self.mensaje.setText(markdown.markdown(f'El cliente con codigo **{identidad}** no existe'))
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        nombre, ok = QInputDialog.getText(self, 'Cambiar nombre...','Escriba el nombre del cliente...')
        
        if ok:
            nombre = nombre.strip()
            
            if len(nombre) == 0:
                self.mensaje.setText('Inserte un nombre para el cliente')
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.exec_()
                return
            
            if self.espacios_seguidos(nombre):
                self.mensaje.setText('El campo nombre no puede tener dos espacios seguidos')
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.exec_()
                return
        
            if not self.regex.match(nombre):
                self.mensaje.setText('Inserte un nombre valido para cliente')
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.exec_()
                return
            
            cliente.nombre = nombre
            
            self.mensaje.setText('Se agregó el nuevo nombre al cliente con exito')
            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.exec_()
            return
            
    def cambiar_id(self):
        identidad = self.ui.txt_identidad_cedula.text()
        
        if len(identidad) == 0:
            self.mensaje.setText('Inserte el codigo del cliente a actualizar sus datos')
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        cliente = self.clientes.buscar_cliente(identidad)
        
        if cliente is None:
            self.mensaje.setText(markdown.markdown(f'El cliente con codigo **{identidad}** no existe'))
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        id, ok = QInputDialog.getInt(self, 'Cambiar No identidad/cedula...','Escriba el numero de identidad/cedula del cliente...')
        
        if ok:
            if len(str(id)) == 0:
                self.mensaje.setText('Inserte un No de identidad/cedula para el cliente')
                self.mensaje.setIcon(QMessageBox.Warning)
                self.mensaje.exec_()
                return
            
            cliente.identidad = str(id)
            
            self.mensaje.setText('Se agregó el nuevo No de identidad/cedula al cliente con exito')
            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.exec_()
            return
 
    def cambiar_objetivo(self):
        self.objetivo = None
        identidad = self.ui.txt_identidad_cedula.text()
        
        if len(identidad) == 0:
            self.mensaje.setText('Inserte el codigo del cliente a actualizar sus datos')
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        cliente = self.clientes.buscar_cliente(identidad)
        
        if cliente is None:
            self.mensaje.setText(markdown.markdown(f'El cliente con codigo **{identidad}** no existe'))
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        self.gui = Cambiar_objetivo_cliente()
        self.gui.show()
        
        self.gui.ui.btn_agregar.clicked.connect(self.agregar_objetivo)
        self.gui.ui.btn_group_objetivo.buttonClicked.connect(self.objetivo_seleccionado)
        
    def agregar_objetivo(self):
        identidad = self.ui.txt_identidad_cedula.text()
        cliente = self.clientes.buscar_cliente(identidad)
        
        if self.gui.ui.btn_group_objetivo.checkedButton() is not None:
            objetivo = self.gui.ui.btn_group_objetivo.checkedButton()
            self.objetivo = objetivo.text()
            
            cliente.objetivo = self.objetivo
            
            self.gui.close()
            self.mensaje.setText('Se agregó el nuevo objetivo con exito.')
            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.exec_()
            return
            
        otro_objetivo = self.gui.ui.txt_otro_objetivo.text().strip()
        
        if len(otro_objetivo) == 0:
            self.mensaje.setText('debe agregar un objetivo o elegir uno')
            self.mensaje.exec_()
            
        if not self.regex.match(otro_objetivo):
            self.mensaje.setText('debe agregar un objetivo valido')
            self.mensaje.exec_()
            
        self.objetivo = otro_objetivo
            
        cliente.objetivo = self.objetivo
        
        self.gui.close()
        self.mensaje.setText('Se agregó el nuevo objetivo con exito.')
        self.mensaje.setIcon(QMessageBox.Information)
        self.mensaje.exec_()
            
    def objetivo_seleccionado(self):
        self.gui.ui.txt_otro_objetivo.setText('')
        self.gui.ui.txt_otro_objetivo.setEnabled(False)
        
    def cambiar_patologias(self):
        self.patologias = None
        identidad = self.ui.txt_identidad_cedula.text()
        
        if len(identidad) == 0:
            self.mensaje.setText('Inserte el codigo del cliente a actualizar sus datos')
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        cliente = self.clientes.buscar_cliente(identidad)
        
        if cliente is None:
            self.mensaje.setText(markdown.markdown(f'El cliente con codigo **{identidad}** no existe'))
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        self.gui_patologias = Cambiar_patologias_cliente()
        self.gui_patologias.show()
        
        self.gui_patologias.ui.btn_agregar_patologias.clicked.connect(self.agregar_patologias)
    
    def agregar_patologias(self):
        identidad = self.ui.txt_identidad_cedula.text()
        cliente = self.clientes.buscar_cliente(identidad)
        
        patologias = self.gui_patologias.ui.txt_patologias.toPlainText()
        
        cliente.patologias = patologias
        
        self.gui_patologias.close()
        self.mensaje.setText('Se agregaron las nuevas patologias con exito.')
        self.mensaje.setIcon(QMessageBox.Information)
        self.mensaje.exec_()
    
    def cambiar_inscripcion(self):
        identidad = self.ui.txt_identidad_cedula.text()
        
        if len(identidad) == 0:
            self.mensaje.setText('Inserte el codigo del cliente a actualizar sus datos')
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        cliente = self.clientes.buscar_cliente(identidad)
        
        if cliente is None:
            self.mensaje.setText(markdown.markdown(f'El cliente con codigo **{identidad}** no existe'))
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        self.gui_inscripcion = Cambiar_inscripcion_cliente()
        self.gui_inscripcion.show()
        
        self.gui_inscripcion.ui.btn_agregar_inscripcion.clicked.connect(self.agregar_inscripcion)

    def agregar_inscripcion(self):
        identidad = self.ui.txt_identidad_cedula.text()
        cliente = self.clientes.buscar_cliente(identidad)
        inscripcion = self.gui_inscripcion.ui.btn_group_inscripcion.checkedButton()
        inscripcion = inscripcion.text()
        
        if inscripcion is not None:
            cliente.inscripcion = str(inscripcion)
            fecha_final = self.clientes.comprobar_fecha_final(str(inscripcion))
            cliente.fecha_final = fecha_final
            cliente.permiso = True
            
            self.gui_inscripcion.close()
            self.mensaje.setText('Se agregó la nueva inscripción con exito.')
            self.mensaje.setIcon(QMessageBox.Information)
            self.mensaje.exec_()
            return
        else:
            self.gui_inscripcion.close()
            self.mensaje.setText('Elija un tipo de inscripción.')
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
    
    def cambiar_foto(self):
        identidad = self.ui.txt_identidad_cedula.text()
        
        if len(identidad) == 0:
            self.mensaje.setText('Inserte el codigo del cliente a actualizar sus datos')
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        cliente = self.clientes.buscar_cliente(identidad)
        
        if cliente is None:
            self.mensaje.setText(markdown.markdown(f'El cliente con codigo **{identidad}** no existe'))
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        self.gui_foto = Cambiar_foto_cliente(self)
        self.gui_foto.show()
        
        self.foto = self.clientes.convertir_a_normal(cliente.foto)
        self.gui_foto.ui.lbl_foto_cliente.setPixmap(self.foto)
        
        self.gui_foto.ui.label_foto.clicked.connect(self.elegir_foto)
        self.gui_foto.ui.btn_agregar_nueva_foto.clicked.connect(self.agregar_foto)
    
    def elegir_foto(self):
        """
        Función que permite al usuario elegir una imagen
        de su computadora y agregarla al 'lbl_foto_agregar'
        para luego ser usada para agregarla en base de datos.
        """
        self.archivo, ok = QFileDialog.getOpenFileName(self, 'Seleccionar archivo de imagen...', 'C:\\','Archivos de imágenes (*.jpg *.png)')
        
        if ok:
            self.gui_foto.ui.lbl_foto_cliente.setPixmap(QPixmap(self.archivo))
    
    def agregar_foto(self):
        identidad = self.ui.txt_identidad_cedula.text()
        cliente = self.clientes.buscar_cliente(identidad)
        
        foto_cliente = self.gui_foto.ui.lbl_foto_cliente.pixmap()
        
        if self.foto.toImage() == foto_cliente.toImage():
            self.mensaje.setText('Esa foto ya se colocó en el cliente')
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.exec_()
            return
        
        foto_binario = self.clientes.convertir_a_binario(self.archivo)
        
        cliente.foto = foto_binario
        
        self.gui_foto.close()
        self.mensaje.setText('La nueva foto se agregó con exito.')
        self.mensaje.setIcon(QMessageBox.Information)
        self.mensaje.exec_()
            
class Cambiar_objetivo_cliente(QDialog):
    def __init__(self):
        super().__init__()
        
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_Ingresar_objetivo()
        self.ui.setupUi(self)

class Cambiar_patologias_cliente(QDialog):
    def __init__(self):
        super().__init__()
        
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_ActualizarPatologias()
        self.ui.setupUi(self)
  
class Cambiar_inscripcion_cliente(QDialog):  
    def __init__(self):
        super().__init__()
        
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_Ingresar_inscripcion()
        self.ui.setupUi(self)
        
class Cambiar_foto_cliente(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.inicializarGui()
        
    def inicializarGui(self):
        self.ui = Ui_ActualizarFoto()
        self.ui.setupUi(self)

class Buscar_info_cliente(QWidget):
    def __init__(self, clientes):
        super().__init__()
        
        self.clientes = clientes
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setWindowTitle('mensaje')
        
        self.inicializarGui()
    
    def inicializarGui(self):
        self.ui = Ui_Buscar_informacion_cliente()
        self.ui.setupUi(self)
        
        self.ui.txt_cedula_TI.setValidator(QIntValidator(10000000, 999999999, self))
        self.ui.btn_buscar_cliente.clicked.connect(self.buscar_cliente)
    
    def buscar_cliente(self):
        codigo = self.ui.txt_cedula_TI.text()
        
        if len(codigo) == 0:
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.setText('El campo cedula/id es obligatoria')
            self.mensaje.exec_()
            return
            
        cliente = self.clientes.buscar_cliente(str(codigo))
        
        if cliente is None:
            self.mensaje.setIcon(QMessageBox.Warning)
            self.mensaje.setText('No existe un cliente con ese No de identidad/Cedula')
            self.mensaje.exec_()
            return
        
        nombre = cliente.nombre
        objetivo = cliente.objetivo
        patologias = cliente.patologias
        inscripcion = cliente.inscripcion
        fecha_final = cliente.fecha_final
        fecha_final_obj = QDateTime.fromString(str(fecha_final), "yyyy-MM-dd HH:mm:ss")
        fecha = fecha_final_obj.date()
        hora = fecha_final_obj.time()
        permiso = cliente.permiso
        
        fecha_actual = datetime.now()
        fecha_final = datetime.strptime(str(fecha_final), '%Y-%m-%d %H:%M:%S')
        
        if fecha_actual > fecha_final:
            cliente.permiso = False
        
        if cliente.permiso == 'True' or cliente.permiso == True:
            permiso = True
        else:
            permiso = False
        
        foto = self.clientes.convertir_a_normal(cliente.foto)
        
        self.ui.txt_nombre.setText(nombre)
        self.ui.txt_objetivo.setText(objetivo)
        self.ui.txt_patologias.setPlainText(str(patologias))
        self.ui.txt_inscripcion.setText(inscripcion)
        self.ui.lbl_foto.setPixmap(foto)
        self.ui.dat_fecha_final.setDate(fecha)
        self.ui.dat_fecha_final.setTime(hora)
        self.ui.chkentrada_gimnasio.setCheckState(permiso) 
    
class Entrar_gimnasio(QWidget):
    def __init__(self, clientes):
        super().__init__() 
        
        self.clientes = clientes
        
        self.inicializarGui()
    
    def inicializarGui(self):
        self.ui = Ui_Entrar_gimnasio()
        self.ui.setupUi(self)  
        
        timer = QTimer(self)
        timer.timeout.connect(self.tick)
        timer.start(1000)
        
        self.default_foto = self.ui.lbl_foto.pixmap()
        
        fecha_actual = str(datetime.now())
        fecha_actual = fecha_actual[0:fecha_actual.find('.')]
        fecha_actual_obj = QDateTime.fromString(str(fecha_actual), "yyyy-MM-dd HH:mm:ss")
        fecha = fecha_actual_obj.date()
        hora = fecha_actual_obj.time()
        
        self.ui.dat_fecha_actual.setDate(fecha)
        self.ui.dat_fecha_actual.setTime(hora)
        
        self.ui.txt_cedula_TI.setValidator(QIntValidator(self))
        self.ui.txt_cedula_TI.editingFinished.connect(self.mostrar_datos)
    
    def mostrar_datos(self):
        cedula_TI = self.ui.txt_cedula_TI.text()
        
        cliente = self.clientes.buscar_cliente(cedula_TI)
        
        if len(cedula_TI) == 0:
            self.ui.txt_cedula_TI.setText('No ha ingresado nada')
            return
        
        if cliente is None:
            self.ui.txt_cedula_TI.setText('No existe un cliente con esa Cedula/TI')
            QTimer.singleShot(3000, self.clear_text)
            return
        
        nombre = cliente.nombre
        
        fecha_final = cliente.fecha_final
        fecha_final_obj = QDateTime.fromString(str(fecha_final), "yyyy-MM-dd HH:mm:ss")
        
        fecha = fecha_final_obj.date()
        hora = fecha_final_obj.time()
        
        fecha_actual = datetime.now()
        fecha_final = datetime.strptime(str(fecha_final), '%Y-%m-%d %H:%M:%S')
        foto = self.clientes.convertir_a_normal(cliente.foto)
        permiso = cliente.permiso
        
        if fecha_actual > fecha_final:
            cliente.permiso = False
            permiso = False
        
        if permiso == 'True' or permiso == True:
            permiso = True
        else:
            permiso = False
        
        if permiso is False:
            self.ui.txt_cedula_TI.setText(f'El cliente ya terminó con su inscripción ({cliente.inscripcion})')
            QTimer.singleShot(3000, self.clear_text)
            return
        
        self.media_player = QMediaPlayer(self)

        self.playlist = QMediaPlaylist(self)
        self.media_player.setPlaylist(self.playlist)

        media_content = QMediaContent(QUrl.fromLocalFile("gimnasio/audio/silbato.mp3"))
        self.playlist.addMedia(media_content)

        self.media_player.play()

        self.ui.txt_nombre.setText(nombre)
        self.ui.dat_fecha_final.setDate(fecha)
        self.ui.dat_fecha_final.setTime(hora)
        self.ui.chk_permiso_entrada.setCheckState(permiso)
        self.ui.lbl_foto.setPixmap(foto)
        QTimer.singleShot(3000, self.clear_all)
    
    def clear_text(self):
        self.ui.txt_cedula_TI.setText('')
        
    def clear_all(self):
        self.ui.txt_nombre.setText('')
        self.ui.txt_cedula_TI.setText('')
        self.ui.dat_fecha_final.setDate(QDate(2000,1,1))
        self.ui.chk_permiso_entrada.setCheckState(False)
        self.ui.lbl_foto.setPixmap(self.default_foto)
    
    def tick(self):
        hora = QTime.currentTime()
        hora_texto = hora.toString('hh:mm')
        
        self.ui.lcd_hora.display(hora_texto)

def main():
    app = QApplication(sys.argv)
    ventana = Gimnasio()
    sys.exit(app.exec_())        

if __name__ == '__main__':
    main()