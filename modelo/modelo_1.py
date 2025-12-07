import os
import cv2
import numpy as np
import pandas as pd
import mysql.connector
import xml.etree.ElementTree as ET
from datetime import datetime
import pydicom
import nibabel as nib
from scipy.io import loadmat
from scipy.signal import butter, filtfilt
import csv


class Model:

    def __init__(self):

        # ----------------------------
        # Carpetas principales del proyecto
        # ----------------------------
        self.carpeta_usuarios = "usuarios"
        self.carpeta_estudios = "estudios"
        self.carpeta_fft = "resultados_fft"
        self.carpeta_hist = "histogramas"

        for c in [self.carpeta_usuarios, self.carpeta_estudios, self.carpeta_fft, self.carpeta_hist]:
            os.makedirs(c, exist_ok=True)

        # ----------------------------
        # Archivo XML para login
        # ----------------------------
        self.archivo_xml = "usuarios.xml"

        # ----------------------------
        # Base de datos MySQL
        # ----------------------------
        self._conectar_mysql()
        self._crear_tabla_logs()

        # ----------------------------
        # Webcam
        # ----------------------------
        self.cap = None

        # Imagen actual para procesamiento
        self.imagen = None


    # ====================================================================
    #                          LOGIN (XML)
    # ====================================================================

    def validar_usuario(self, username, password):
        tree = ET.parse(self.archivo_xml)
        root = tree.getroot()

        usuarios = root.find("usuarios").findall("usuario")

        for u in usuarios:
            user_xml = u.find("nombre").text.strip()
            pass_xml = u.find("password").text.strip()

            if user_xml == username and pass_xml == password:
                return True

        return False

    # ====================================================================
    #                   BASE DE DATOS (MySQL)
    # ====================================================================

    def _conectar_mysql(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="proyecto_info2"
            )
            self.cursor = self.db.cursor()
        except:
            try:
                temp = mysql.connector.connect(host="localhost", user="root", password="")
                cur = temp.cursor()
                cur.execute("CREATE DATABASE proyecto_info2")
                temp.close()

                self.db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="proyecto_info2"
                )
                self.cursor = self.db.cursor()
            except Exception as e:
                print("⚠ ERROR MYSQL:", e)
                self.db = None

    def _crear_tabla_logs(self):
        if self.db is None:
            return
        query = """
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(100),
            fecha DATETIME,
            tipo_actividad VARCHAR(255),
            ruta_archivo VARCHAR(500)
        )
        """
        self.cursor.execute(query)
        self.db.commit()

    def registrar_actividad(self, usuario, tipo, ruta=""):
        if self.db is None:
            return
        query = """
        INSERT INTO logs (usuario, fecha, tipo_actividad, ruta_archivo)
        VALUES (%s, %s, %s, %s)
        """
        valores = (usuario, datetime.now(), tipo, ruta)
        self.cursor.execute(query, valores)
        self.db.commit()

    # ====================================================================
    #                        CÁMARA WEB (OpenCV)
    # ====================================================================

    def iniciar_camara(self):
        print(">>> intentando abrir camara...")
        self.cap = cv2.VideoCapture(0)
        print(">>> cap:", self.cap)
        print(">>> abierto:", self.cap.isOpened())
        return self.cap.isOpened()

    def leer_frame(self):
        if self.cap is None:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def capturar_foto(self, usuario):
        ret, frame = self.cap.read()
        if not ret:
            return None

        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        path = os.path.join(self.carpeta_usuarios, f"{usuario}.png")
        cv2.imwrite(path, gris)

        self.registrar_actividad(usuario, "captura_foto", path)

        return path

    def apagar_camara(self):
        if self.cap:
            self.cap.release()
            self.cap = None

    # ====================================================================
    #              PROCESAMIENTO DE IMÁGENES JPG/PNG/DICOM/NIFTI
    # ====================================================================

    def guardar_imagen_actual(self, img):
        self.imagen = img

    def cargar_imagen(self, path):
        ext = os.path.splitext(path)[1].lower()

        try:
            # --------------------------- JPG / PNG / BMP ---------------------------
            if ext in [".jpg", ".jpeg", ".png", ".bmp"]:
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                self.imagen = img
                return img

            # --------------------------- DICOM ---------------------------
            if ext == ".dcm":
                d = pydicom.dcmread(path)
                img = d.pixel_array.astype(np.int16)

                img = self.normalizar_hu(img)
                self.imagen = img
                return img

            # --------------------------- NIFTI (.nii .gz) ---------------------------
            if ext in [".nii", ".gz"]:
                vol, _ = self.cargar_nifti(path)

                corte = vol[:, :, vol.shape[2] // 2]
                corte = (corte - corte.min()) / (corte.max() - corte.min()) * 255
                corte = corte.astype("uint8")

                self.imagen = corte
                return corte

            return None

        except Exception as e:
            print("ERROR cargar_imagen:", e)
            return None

    # -------------- Procesamiento solicitado -----------------

     # ====================================================================
    #              PROCESAMIENTO DE IMÁGENES (SIEMPRE DESDE ORIGINAL)
    # ====================================================================

    # Normalización
    def normalizar_imagen(self, img):
        return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

    # Binarización simple
    def binarizar_imagen(self, img, t=128):
        _, binaria = cv2.threshold(img, t, 255, cv2.THRESH_BINARY)
        return binaria

    # Detección de bordes
    def detectar_bordes(self, img):
        return cv2.Canny(img, 50, 150)

    # Umbralización simple
    def umbralizar_imagen(self, img, t=128):
        _, out = cv2.threshold(img, t, 255, cv2.THRESH_BINARY)
        return out

    # Morfología
    def morfologia(self, img, tipo="dilatacion"):
        kernel = np.ones((5, 5), np.uint8)
        if tipo == "erosion":
            return cv2.erode(img, kernel)
        elif tipo == "apertura":
            return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        elif tipo == "cierre":
            return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return cv2.dilate(img, kernel)

    # Filtro (puedes cambiar kernel si deseas)
    def filtrar_imagen(self, img):
        return cv2.GaussianBlur(img, (5, 5), 0)

    # ====================================================================
    #                   DICOM + NIFTI + VISUALIZACIÓN 3D
    # ====================================================================

    def cargar_estudio_dicom(self, carpeta):
        rutas = sorted([os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith(".dcm")])

        volumen = []
        metadatos = None

        for r in rutas:
            d = pydicom.dcmread(r)
            px = d.pixel_array.astype(np.int16)
            slope = float(getattr(d, "RescaleSlope", 1))
            intercept = float(getattr(d, "RescaleIntercept", 0))

            img_hu = px * slope + intercept
            volumen.append(img_hu)

            if metadatos is None:
                metadatos = {
                    "StudyDate": getattr(d, "StudyDate", ""),
                    "StudyTime": getattr(d, "StudyTime", ""),
                    "Modality": getattr(d, "Modality", ""),
                    "StudyDescription": getattr(d, "StudyDescription", ""),
                    "SeriesTime": getattr(d, "SeriesTime", "")
                }

        volumen = np.array(volumen)

        csv_path = os.path.join(self.carpeta_estudios, "metadatos_estudio.csv")
        with open(csv_path, "w", newline="") as f:
            w = csv.writer(f)
            for k, v in metadatos.items():
                w.writerow([k, v])

        return volumen, metadatos, csv_path

    def cargar_nifti(self, path):
        img = nib.load(path)
        return img.get_fdata(), {}

    def corte_axial(self, vol, i): return vol[i, :, :]
    def corte_sagital(self, vol, i): return vol[:, :, i]
    def corte_coronal(self, vol, i): return vol[:, i, :]

    def mip(self, vol, eje=0):
        return np.max(vol, axis=eje)

    def normalizar_hu(self, img):
        img = np.clip(img, -1024, 1500)
        img = (img - img.min()) / (img.max() - img.min()) * 255
        return img.astype(np.uint8)

    # ====================================================================
    #                  SEÑALES BIOMÉDICAS (MAT + FFT)
    # ====================================================================

    def cargar_mat(self, path):
        data = loadmat(path)
        for k, v in data.items():
            if isinstance(v, np.ndarray):
                return v.squeeze()
        return None

    def fft(self, señal):
        Y = np.abs(np.fft.fft(señal))
        return Y[:len(Y)//2]

    def filtro_pasabajas(self, señal, fc=10, fs=100):
        b, a = butter(4, fc/(fs/2), btype="low")
        return filtfilt(b, a, señal)

    def fft_analisis(self, senal, fs=100):
        N = len(senal)
        Y = np.abs(np.fft.fft(senal))[:N//2]
        freqs = np.fft.fftfreq(N, d=1/fs)[:N//2]

        df = pd.DataFrame({
            "Frecuencia (Hz)": freqs,
            "Magnitud": Y
        })

        path = os.path.join(self.carpeta_fft, f"fft_{datetime.now().strftime('%H%M%S')}.csv")
        df.to_csv(path, index=False)

        return df, path

    def desviacion_estandar(self, senal, eje=0):
        return np.std(senal, axis=eje)

    # ====================================================================
    #                          CSV TABULAR
    # ====================================================================

    def cargar_csv(self, path):
        try:
            df = pd.read_csv(path)
            return df
        except:
            return None

    def obtener_columnas(self, df):
        return list(df.columns)

    def extraer_columna(self, df, columna):
        return df[columna] if columna in df.columns else None

    def dataframe_a_lista(self, df):
        return df.values.tolist()

    def guardar_log_csv(self, usuario, path):
        self.registrar_actividad(usuario, "cargar_csv", path)



