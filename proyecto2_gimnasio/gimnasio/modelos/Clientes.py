from datetime import datetime

from PIL import Image
import io
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox

class Clientes():
    def __init__(self):
        self.clientes = []
        self.image_cache = {}

    def agregar_clientes(self, cliente):
        self.clientes.append(cliente)
                
    def buscar_cliente(self,identidad):
        for c in self.clientes:    
            if c.identidad == identidad:
                return c
        return None
    
    def comprobar_fecha_final(self, inscripcion):
        año = int(datetime.strftime(datetime.now(),'%Y'))
        mes = int(datetime.strftime(datetime.now(),'%m'))
        dia = int(datetime.strftime(datetime.now(),'%d'))
        
        hora = int(datetime.strftime(datetime.now(), '%H'))
        minuto = int(datetime.strftime(datetime.now(), '%M'))
        segundo = int(datetime.strftime(datetime.now(), '%S'))
        
        meses_treintaun_dias = [1, 3, 5, 7 , 8, 10, 12]
        meses_treinta_dias = [4, 6, 9, 11]
        mes_veintenueve_ocho_dias = 2
        
        if inscripcion == 'DIA':
            dia += 1
            if int(mes) in meses_treintaun_dias:
                if dia > 31:
                    dia -= 31
                    mes += 1
                    
                if mes > 12:
                    mes -= 12
                    año += 1
            
            if int(mes) in meses_treinta_dias:
                if dia > 30:
                    dia -= 30
                    mes += 1

                if mes > 12:
                    mes -= 12
                    año += 1
                
            if int(mes) == mes_veintenueve_ocho_dias:
                if año % 4 != 0 and año % 100 == 0:
                    if año % 100 == 0 and año % 400 != 0:
                        if dia > 28:
                            dia -= 28
                            mes += 1
                            
                if año % 4 == 0 and año % 100 != 0:
                    if año % 100 == 0 and año % 400 == 0:
                        if dia > 29:
                            dia -= 29
                            mes += 1
                
                if mes > 12:
                    mes -= 12
                    año += 1
        
        if inscripcion == 'MES':
            mes += 1
            
            if mes > 12:
                mes -= 12
                año += 1
            
            if int(mes) in meses_treinta_dias:
                if dia > 30:
                    dia -= 30
                    mes += 1
                
            if int(mes) == mes_veintenueve_ocho_dias:
                if año % 4 != 0 and año % 100 == 0:
                    if año % 100 == 0 and año % 400 != 0:
                        if dia > 28:
                            dia -= 28
                            mes += 1
                            
                if año % 4 == 0 and año % 100 != 0:
                    if año % 100 == 0 and año % 400 == 0:
                        if dia > 29:
                            dia -= 29
                            mes += 1
            
        
        if inscripcion == 'AÑO':
            año += 1
        
        fecha_final = datetime(año,mes,dia, hora, minuto, segundo)
        return fecha_final
         
    def eliminar_cliente(self, cliente):
        self.clientes.remove(cliente)

    def Permiso_de_entrada(self):
        for e in self.clientes:
            if datetime.now() >= e.fecha_final:
                e.permiso = False
                 
    def convertir_a_normal(self, imagen_binaria):
        """
        Función que convierte una imagen binaria
        y la convierte en un QPixmap.

        Parameters:
        imagen_binaria: imagen binaria.

        Returns:
        imagen_normal: QPixmap de la imagen.
        """
        # Verificar si la imagen ya está en caché y devolverla
        if imagen_binaria in self.image_cache:
            return self.image_cache[imagen_binaria]

        imagen_io = io.BytesIO(imagen_binaria)
        imagen_pil = Image.open(imagen_io)

        if imagen_pil.mode != 'RGBA':
            imagen_pil = imagen_pil.convert('RGBA')

        imagen_qt = QImage(imagen_pil.tobytes(), imagen_pil.size[0], imagen_pil.size[1], QImage.Format_RGBA8888)
        imagen_normal = QPixmap.fromImage(imagen_qt)

        # Almacenar la imagen convertida en caché
        self.image_cache[imagen_binaria] = imagen_normal

        return imagen_normal
                
    def convertir_a_binario(self,foto):
        """
        Función que convierte a binario una imagen.
        
        Parameters:
        foto = ruta de la imagen suministrada por el usuario
        
        Returns:
        blob = Imagen en binario.
        None = Sí hubo un error al convertir a binario.
        """
        try:
            with open(foto, 'rb') as f:
                blob = f.read()
                
            return blob
        except:
            mensaje = QMessageBox(self)
            mensaje.setIcon(QMessageBox.Warning)
            mensaje.setWindowTitle('Error')
            mensaje.setText('hubo un error, intentalo de nuevo')
            mensaje.exec_()
            return None