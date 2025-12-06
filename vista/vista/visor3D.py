import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class Visor3D(QWidget):
    def __init__(self):
        super().__init__()
        ruta_ui = os.path.join(os.path.dirname(__file__), "visor3D.ui")
        uic.loadUi(ruta_ui, self)


