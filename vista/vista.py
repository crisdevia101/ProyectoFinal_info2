
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QWidget, QMainWindow,
    QLineEdit, QPushButton, QLabel, QSlider,
    QTableWidget, QComboBox
)
import resources_rc

#Ventana login
class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("vista/login.ui", self)

        self.inputUser = self.findChild(QLineEdit, "Usuario")
        self.inputPass = self.findChild(QLineEdit, "Password")
        self.btnLogin  = self.findChild(QPushButton, "botonIngresar")

    def limpiarCampos(self):
        self.inputUser.clear()
        self.inputPass.clear()


#Ventana_principal
class MainWindowView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("vista/ventana_principal.ui", self)

        self.setStyleSheet("""
        #centralwidget {
            background-image: url(:/images/images/fondo_negro.jpg);
            background-repeat: no-repeat;
            background-position: center;
        }
        """)

        # Botones imagenes
        self.btnCargarDICOM = self.findChild(QPushButton, "BotonCargarImagen")
        self.Normalizar = self.findChild(QPushButton, "Normalizar")
        self.Filtrar = self.findChild(QPushButton, "Filtrar")
        self.Binarizar = self.findChild(QPushButton, "Binarizar")
        self.Umbralizar = self.findChild(QPushButton, "Umbralizar")
        self.Morfologia = self.findChild(QPushButton, "Morfologia")
        self.DeteccionBordes = self.findChild(QPushButton, "DeteccionBordes")
        self.Comparar = self.findChild(QPushButton, "Comparar")
        self.AbrirVisor3D = self.findChild(QPushButton, "AbrirVisor3D")

         # 3. CSV
        self.botonCargarCSV = self.findChild(QPushButton, "botonCargarCSV")
        if self.botonCargarCSV is None:
             self.botonCargarCSV = self.findChild(QPushButton, "btnCargarCSV")

        self.tablaDatosCSV = self.findChild(QTableWidget, "tablaDatosCSV")
        self.botonGraficarCols = self.findChild(QPushButton, "botonGraficarCols")
        
        # Combos (si no los encuentra, no crashea)
        self.comboBoxCol1 = self.findChild(QComboBox, "comboBoxCol1")
        self.comboBoxCol2 = self.findChild(QComboBox, "comboBoxCol2")
        self.comboBoxCol3 = self.findChild(QComboBox, "comboBoxCol3")
        self.comboBoxCol4 = self.findChild(QComboBox, "comboBoxCol4")
        self.widgetGraficas = self.findChild(QWidget, "widgetGraficas")

        # 4. Señales
        self.CargarMAT = self.findChild(QPushButton, "CargarMAT")
        # Resto de objetos
        self.tablaFrecuencias = self.findChild(QTableWidget, "tablaFrecuencias")
        self.ComboBoxCanal = self.findChild(QComboBox, "ComboBoxCanal")
        self.ComboBoxEje = self.findChild(QComboBox, "ComboBoxEje")
        self.botonGraficarCanal = self.findChild(QPushButton, "botonGraficarCanal")
        self.botonGraficarHisto = self.findChild(QPushButton, "botonGraficarHisto")
        self.widgetGraficaCanal = self.findChild(QWidget, "widgetGraficaCanal")
        self.widgetGraficaHistograma = self.findChild(QWidget, "widgetGraficaHistograma")


    def limpiarTablas(self):
        self.tableCSV.clearContents()
        self.tableCSV.setRowCount(0)
        self.tableFFT.clearContents()
        self.tableFFT.setRowCount(0)


# Ventana visor3D
class ImageViewerView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("vista/visor3D.ui", self)

        # Sliders de navegación 3D
        self.sliderAxial = self.findChild(QSlider, "SliderAxial")
        self.sliderSagital = self.findChild(QSlider, "SliderSagital")
        self.sliderCoronal = self.findChild(QSlider, "SliderCoronal")

        # Labels de imágenes
        self.labelAxial = self.findChild(QLabel, "Axial")
        self.labelSagital = self.findChild(QLabel, "Sagital")
        self.labelCoronal = self.findChild(QLabel, "Coronal")

        # Botón MIP (si existe)
        try:
            self.btnMIP = self.findChild(QPushButton, "MIP")
        except:
            self.btnMIP = None

    def limpiarVisor(self):
        self.labelAxial.clear()
        self.labelSagital.clear()
        self.labelCoronal.clear()

