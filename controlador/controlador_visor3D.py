from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

import numpy as np
import cv2
import datetime

from vista.vista import ImageViewerView


class ControladorVisor3D:
    def __init__(self, model, usuario):
        print(">>> ControladorVisor3D cargado correctamente <<<")

        self.view = ImageViewerView()
        self.model = model
        self.usuario = usuario
        self.volume = None
        self.meta = None

        # Botones
        self.btnLoad = getattr(self.view, "BotonCargarDICOM", None)
        if self.btnLoad:
            self.btnLoad.clicked.connect(self.load_dicom_folder)

        self.btnMIP = getattr(self.view, "MIP", None)
        if self.btnMIP:
            self.btnMIP.clicked.connect(self.generate_mip)

        # Sliders
        self.sliderAxial = getattr(self.view, "SliderAxial", None)
        self.sliderSagital = getattr(self.view, "SliderSagital", None)
        self.sliderCoronal = getattr(self.view, "SliderCoronal", None)

        if self.sliderAxial:
            self.sliderAxial.valueChanged.connect(self.update_axial)
        if self.sliderSagital:
            self.sliderSagital.valueChanged.connect(self.update_sagital)
        if self.sliderCoronal:
            self.sliderCoronal.valueChanged.connect(self.update_coronal)

    
    def show(self):
        self.view.show()

    def _resize_like_axial(self, img):
        h, w = img.shape

        if w < 100:  
            scale = 3  
            img = cv2.resize(img, (w * scale, h * scale), interpolation=cv2.INTER_LINEAR)

        return img

    def _add_title(self, img, title):
        title_h = 35
        w = img.shape[1]
        bar = np.zeros((title_h, w), dtype=np.uint8)
        cv2.putText(bar, title, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, 255, 2, cv2.LINE_AA)
        return np.vstack((bar, img))

    def _array_to_qpixmap(self, arr, lbl):
        # Normalizar intensidades
        a = np.nan_to_num(arr)
        a = a - a.min()
        if a.max() > 0:
            a = (a / a.max()) * 255.0
        a = a.astype(np.uint8)

        target_w = lbl.width()
        target_h = lbl.height()

        # Resize manteniendo calidad
        a_resized = cv2.resize(a, (target_w, target_h), interpolation=cv2.INTER_AREA)

        # Convertir a QPixmap
        qimg = QImage(a_resized.data, target_w, target_h, target_w, QImage.Format_Grayscale8)
        return QPixmap.fromImage(qimg)


    # Cargar archivo
    def load_dicom_folder(self):
        folder = QFileDialog.getExistingDirectory(self.view, "Seleccionar carpeta DICOM")
        if not folder:
            return

        try:
            vol, meta, csv_path = self.model.cargar_estudio_dicom(folder)
        except Exception as e:
            QMessageBox.warning(self.view, "Error", f"No se pudo cargar el volumen.\n\n{e}")
            return

        self.volume = vol
        self.meta = meta

        print(">>> Volumen cargado. Forma =", vol.shape)

        self.model.registrar_actividad(self.usuario, "cargar_estudio_dicom", folder)

        # configurar sliders
        if self.sliderAxial:
            self.sliderAxial.setMinimum(0)
            self.sliderAxial.setMaximum(vol.shape[0] - 1)
            self.sliderAxial.setValue(vol.shape[0] // 2)

        if self.sliderSagital:
            self.sliderSagital.setMinimum(0)
            self.sliderSagital.setMaximum(vol.shape[2] - 1)
            self.sliderSagital.setValue(vol.shape[2] // 2)

        if self.sliderCoronal:
            self.sliderCoronal.setMinimum(0)
            self.sliderCoronal.setMaximum(vol.shape[1] - 1)
            self.sliderCoronal.setValue(vol.shape[1] // 2)

        # actualizar vistas iniciales
        self.update_axial()
        self.update_sagital()
        self.update_coronal()


    def update_axial(self):
        if self.volume is None:
            return

        i = self.sliderAxial.value()
        img = self.volume[i, :, :]
        
        img = self._add_title(img, f"Axial - Slice: {i}")

        lbl = getattr(self.view, "labelAxial", None)
        if lbl:
            pix = self._array_to_qpixmap(img, lbl)
            lbl.setPixmap(pix)

    def update_sagital(self):
        if self.volume is None:
            return

        i = self.sliderSagital.value()
        img = self.volume[:, :, i]
        
        img = self._add_title(img, f"Sagital - Slice: {i}")

        lbl = getattr(self.view, "labelSagital", None)
        if lbl:
            pix = self._array_to_qpixmap(img, lbl)
            lbl.setPixmap(pix)

    def update_coronal(self):
        if self.volume is None:
            return

        i = self.sliderCoronal.value()
        img = self.volume[:, i, :]

        img = self._add_title(img, f"Coronal - Slice: {i}")

        lbl = getattr(self.view, "labelCoronal", None)
        if lbl:
            pix = self._array_to_qpixmap(img, lbl)
            lbl.setPixmap(pix)


    # MIP
    def generate_mip(self):
        if self.volume is None:
            QMessageBox.warning(self.view, "MIP", "No hay volumen cargado.")
            return

        mip = self.model.mip(self.volume, eje=0)

        mip = self._add_title(mip, "MIP (Maxima Intensidad Proyectada)")


        lbl = getattr(self.view, "ImagenMIP", None)
        
        if not lbl:
             QMessageBox.warning(self.view, "Error MIP", "No se encontró el widget 'ImagenMIP'.")
             return

        pix = self._array_to_qpixmap(mip, lbl)

        
        if lbl:
            lbl.setPixmap(pix.scaled(lbl.width(), lbl.height(), Qt.KeepAspectRatio))

        out = f"mip_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(out, mip)

        self.model.registrar_actividad(self.usuario, "mip_generada", out)