from PyQt5.QtGui import QPixmap, QImage
from modelo.modelo_imagenes import ModeloImagenes


class CtrlVisor3D:

    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloImagenes()

        self.vista.SliderAxial.valueChanged.connect(self.actualizar_axial)
        self.vista.SliderSagital.valueChanged.connect(self.actualizar_sagital)
        self.vista.SliderCoronal.valueChanged.connect(self.actualizar_coronal)
        self.vista.MIP.clicked.connect(self.generar_mip)

    # ========= CARGA DE VOLUMEN =========
    def cargar_volumen(self, volumen):
        self.modelo.volumen = volumen

        Z, Y, X = volumen.shape

        self.vista.SliderAxial.setMaximum(Z - 1)
        self.vista.SliderCoronal.setMaximum(Y - 1)
        self.vista.SliderSagital.setMaximum(X - 1)

        self.actualizar_axial(0)
        self.actualizar_sagital(0)
        self.actualizar_coronal(0)

    def cargar_dicom(self, carpeta):
        vol = self.modelo.cargar_dicom_carpeta(carpeta)
        self.cargar_volumen(vol)
        self.modelo.guardar_metadata_csv()

    def cargar_nifti(self, ruta):
        vol = self.modelo.cargar_nifti(ruta)
        self.cargar_volumen(vol)
        self.modelo.guardar_metadata_csv()

    # ========= ACTUALIZACIÓN DE IMÁGENES =========
    def _mostrar(self, img_array, label):
        h, w = img_array.shape
        qimg = QImage(img_array.data, w, h, w, QImage.Format_Grayscale8)
        label.setPixmap(QPixmap.fromImage(qimg.copy()))

    def actualizar_axial(self, idx):
        if self.modelo.volumen is None:
            return
        s = self.modelo.corte_axial(idx)
        self._mostrar(s, self.vista.Axial)

    def actualizar_sagital(self, idx):
        if self.modelo.volumen is None:
            return
        s = self.modelo.corte_sagital(idx)
        self._mostrar(s, self.vista.Sagital)

    def actualizar_coronal(self, idx):
        if self.modelo.volumen is None:
            return
        s = self.modelo.corte_coronal(idx)
        self._mostrar(s, self.vista.Coronal)

    def generar_mip(self):
        if self.modelo.volumen is None:
            return
        mip = self.modelo.generar_mip()
        self._mostrar(mip, self.vista.ImagenMIP)

