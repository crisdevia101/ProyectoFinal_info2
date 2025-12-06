import sys
from PyQt5 import QtWidgets
from vista.visor3D import Visor3D
from controlador.ctrl_visor3D import CtrlVisor3D
import numpy as np


class MainController:
    def __init__(self):
      #crea la ap👌
        self.app = QtWidgets.QApplication(sys.argv)
 
        self.vista_visor = Visor3D()

        self.ctrl_visor = CtrlVisor3D(self.vista_visor)

    def ejecutar(self):
        self.vista_visor.show()
        sys.exit(self.app.exec_())

    def cargar_volumen_prueba(self):
        vol = np.zeros((50, 50, 50))
        self.ctrl_visor.cargar_volumen(vol)

