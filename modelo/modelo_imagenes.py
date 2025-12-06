# Aquí es para las funciones para DICOM, JPG/PNG, cortes y MIP 🙃
import os
import csv
import numpy as np
import pydicom
import nibabel as nib
import cv2

class ModeloImagenes:
    
    def __init__(self):
        self.volumen = None
        self.meta = None

    # =============== CARGA DE IMÁGENES MÉDICAS ==================
    def cargar_dicom_carpeta(self, carpeta, aplicar_hu=True):
        archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta)
                    if f.lower().endswith(".dcm")]

        if not archivos:
            raise Exception("No hay archivos .dcm en la carpeta.")

        slices = [pydicom.dcmread(f) for f in archivos]

        # Ordenar cortes
        try:
            slices.sort(key=lambda s: int(s.InstanceNumber))
        except:
            pass

        self.meta = slices[0]

        volumen = np.stack([s.pixel_array for s in slices]).astype(np.int16)

        # Conversión a HU
        if aplicar_hu:
            slope = float(getattr(self.meta, "RescaleSlope", 1.0))
            intercept = float(getattr(self.meta, "RescaleIntercept", 0.0))
            volumen = volumen * slope + intercept

        self.volumen = volumen.astype(np.int16)
        return self.volumen

    def cargar_nifti(self, ruta):
        img = nib.load(ruta)
        data = img.get_fdata()

        if data.ndim == 4:
            data = data[..., 0]

        # reorganizar a (Z, Y, X)
        if data.shape[2] < data.shape[0]:
            data = np.transpose(data, (2, 0, 1))

        self.volumen = data.astype(np.float32)
        self.meta = img.header
        return self.volumen

    def cargar_imagen_2d(self, ruta):
        img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise Exception("No se pudo cargar la imagen 2D.")
        return img

    # =============== METADATA A CSV ==================
    def guardar_metadata_csv(self, ruta_csv="resultados/metadata_imagenes.csv"):
        os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)

        campos = [
            "PatientName", "PatientID", "PatientSex", "PatientAge",
            "StudyDate", "StudyTime", "StudyDescription",
            "Modality", "SeriesDescription"
        ]

        fila = {}

        if hasattr(self.meta, "__dict__"):
            for c in campos:
                fila[c] = str(getattr(self.meta, c, ""))
        else:
            fila = {c: "" for c in campos}

        existe = os.path.exists(ruta_csv)
        with open(ruta_csv, "a", newline="", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            if not existe:
                writer.writeheader()
            writer.writerow(fila)

    # =============== CORTES 3D ==================
    def normalizar(self, img):
        mn, mx = np.min(img), np.max(img)
        if mx - mn == 0:
            return np.zeros_like(img, dtype=np.uint8)
        img = (img - mn) / (mx - mn)
        return (img * 255).astype(np.uint8)

    def corte_axial(self, idx):
        return self.normalizar(self.volumen[idx, :, :])

    def corte_sagital(self, idx):
        return self.normalizar(self.volumen[:, :, idx])

    def corte_coronal(self, idx):
        return self.normalizar(self.volumen[:, idx, :])

    def generar_mip(self):
        mip = np.max(self.volumen, axis=0)
        return self.normalizar(mip)

    # =============== PROCESAMIENTO JPG/PNG ==================
    def filtro_gauss(self, img):
        return cv2.GaussianBlur(img, (5, 5), 0)

    def binarizar_otsu(self, img):
        _, b = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return b

    def umbralizar(self, img, t=128):
        _, b = cv2.threshold(img, t, 255, cv2.THRESH_BINARY)
        return b

    def erosion(self, img):
        k = np.ones((3, 3), np.uint8)
        return cv2.erode(img, k, 1)

    def dilatacion(self, img):
        k = np.ones((3, 3), np.uint8)
        return cv2.dilate(img, k, 1)

    def canny(self, img):
        return cv2.Canny(img, 100, 200)
