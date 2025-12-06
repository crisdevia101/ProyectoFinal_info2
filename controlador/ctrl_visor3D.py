import os
from PyQt5.QtGui import QPixmap
from modelo.mysql_manager import MySQLManager

class CtrlVisor3D:
    def __init__(self, vista):
        self.vista = vista
        self.db = MySQLManager()

        self.volumen = None
        self.conectar_eventos()

    def conectar_eventos(self):
        self.vista.SliderAxial.valueChanged.connect(self.actualizar_axial)
        self.vista.SliderSagital.valueChanged.connect(self.actualizar_sagital)
        self.vista.SliderCoronal.valueChanged.connect(self.actualizar_coronal)
        self.vista.MIP.clicked.connect(self.generar_mip)

    def cargar_volumen(self, volumen):
        self.volumen = volumen

        self.vista.SliderAxial.setMaximum(volumen.shape[0] - 1)
        self.vista.SliderSagital.setMaximum(volumen.shape[1] - 1)
        self.vista.SliderCoronal.setMaximum(volumen.shape[2] - 1)

        self.db.registrar_actividad(
            usuario="DaniSL",
            tipo="Cargar volumen",
            detalles=f"Dimensiones: {volumen.shape}"
        )

    def actualizar_axial(self, valor):
        if self.volumen is None:
            return
        print(f"Corte axial → slice {valor}")

    def actualizar_sagital(self, valor):
        if self.volumen is None:
            return
        print(f"Corte sagital → slice {valor}")

    def actualizar_coronal(self, valor):
        if self.volumen is None:
            return
        print(f"Corte coronal → slice {valor}")

    def generar_mip(self):
        if self.volumen is None:
            print("No hay volumen cargado para MIP.")
            return

        print("Generando MIP…")

        self.db.registrar_actividad(
            usuario="DaniSL",
            tipo="Generar MIP"
        )

        ruta = os.path.join(os.path.dirname(__file__), "..", "images", "negro.jpg")
        ruta = os.path.abspath(ruta)
        self.vista.ImagenMIP.setPixmap(QPixmap(ruta))

