from PyQt5.QtWidgets import (
    QFileDialog, QMessageBox, QTableWidgetItem, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import cv2
import time

from vista.vista import MainWindowView
from controlador.controlador_visor3D import ControladorVisor3D


class ControladorPrincipal:
    def _setup_graph(self, container_widget):
        """Inicializa una figura de Matplotlib y la incrusta en un QWidget.
        Si el container_widget es None devuelve None."""
        try:
            if container_widget is None:
                return None

            fig = Figure(figsize=(5, 3))
            canvas = FigureCanvas(fig)

            try:
                if container_widget.layout():
                    for i in reversed(range(container_widget.layout().count())):
                        w = container_widget.layout().itemAt(i).widget()
                        if w:
                            w.setParent(None)
            except Exception:
                pass

            layout = QVBoxLayout(container_widget)
            layout.addWidget(canvas)
            layout.setContentsMargins(0, 0, 0, 0)

            return canvas
        except Exception as e:
            print("ERROR _setup_graph:", e)
            return None


    def __init__(self, view, model, usuario):
        self.view = view
        self.model = model
        self.usuario = usuario

        # Señales
        self.datos_senal = None
        self.fs = getattr(self.model, "fs", 250)  
        self._df_actual = None

        # Imágenes
        self.imagen_original = None  
        self.imagen_procesada = None

        # Timer para cámara
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)

        self.btnCargarMAT = getattr(self.view, "CargarMAT", None)
        self.comboCanal   = getattr(self.view, "BoxCanal", None)
        self.comboEje     = getattr(self.view, "ComboBoxEje", None)
        self.tablaFreq    = getattr(self.view, "tablaFrecuencias", None)
        self.widgetCanal  = getattr(self.view, "widgetGraficaCanal", None)
        self.widgetHisto  = getattr(self.view, "widgetGraficaHistograma", None)
        self.btnGraficarCanal = getattr(self.view, "botonGraficarCanal", None)
        self.btnGraficarHisto = getattr(self.view, "botonGraficarHisto", None)

        # BOTONES DE IMAGEN
        self.btnCargarImagen = getattr(self.view, "BotonCargarImagen", None)
        self.btnNormalizar   = getattr(self.view, "Normalizar", None)
        self.btnFiltrar      = getattr(self.view, "Filtrar", None)
        self.btnBinarizar    = getattr(self.view, "Binarizar", None)
        self.btnUmbralizar   = getattr(self.view, "Umbralizar", None)
        self.btnMorfologia   = getattr(self.view, "Morfologia", None)
        self.btnBordes       = getattr(self.view, "DeteccionBordes", None)
        self.btnComparar     = getattr(self.view, "Comparar", None)

        # DIAGNÓSTICO
        print("DEBUG: Widgets señales:")
        print(" btnCargarMAT:", self.btnCargarMAT)
        print(" comboCanal (BoxCanal):", self.comboCanal)
        print(" comboEje:", self.comboEje)
        print(" tablaFrecuencias:", self.tablaFreq)
        print(" widgetGraficaCanal:", self.widgetCanal)
        print(" widgetGraficaHistograma:", self.widgetHisto)
        print(" botonGraficarCanal:", self.btnGraficarCanal)
        print(" botonGraficarHisto:", self.btnGraficarHisto)
        print(" modelo.fs:", self.fs)
        print(" BotonCargarImagen:", self.btnCargarImagen)
        print(" BotonNormalizar:", self.btnNormalizar)
        print(" BotonFiltrar:", self.btnFiltrar)
        print(" BotonBinarizar:", self.btnBinarizar)
        print(" BotonUmbralizar:", self.btnUmbralizar)
        print(" BotonMorfologia:", self.btnMorfologia)
        print(" BotonBordes:", self.btnBordes)
        print(" BotonComparar:", self.btnComparar)

        if self.widgetCanal is None:
            try:
                self.widgetCanal = QWidget(self.view)
                self.widgetCanal.setGeometry(20, 120, 480, 260)
                self.widgetCanal.setObjectName("widgetGraficaCanal_auto")
                self.widgetCanal.show()
                print("widgetGraficaCanal no existe en UI: creado dinámicamente.")
            except Exception as e:
                print("ERROR creando widgetGraficaCanal dinámico:", e)
                self.widgetCanal = None

        if self.widgetHisto is None:
            try:
                self.widgetHisto = QWidget(self.view)
                self.widgetHisto.setGeometry(520, 120, 480, 260)
                self.widgetHisto.setObjectName("widgetGraficaHistograma_auto")
                self.widgetHisto.show()
                print("widgetGraficaHistograma no existe en UI: creado dinámicamente.")
            except Exception as e:
                print("ERROR creando widgetGraficaHistograma dinámico:", e)
                self.widgetHisto = None

        # Inicializar canvas
        self.canvas_canal = self._setup_graph(self.widgetCanal)
        self.canvas_histo = self._setup_graph(self.widgetHisto)

        # Conexiones de señales
        if self.btnCargarMAT:
            self.btnCargarMAT.clicked.connect(self.load_mat_logic)

        if self.btnGraficarCanal:
            self.btnGraficarCanal.clicked.connect(self.actualizar_canal_y_fft)


        if self.btnGraficarHisto:
            self.btnGraficarHisto.clicked.connect(self.graficar_histograma_std)

        if self.comboCanal:
            try:
                self.comboCanal.currentIndexChanged.disconnect()
            except Exception:
                pass
            self.comboCanal.currentIndexChanged.connect(self.actualizar_canal_y_fft)

        # Widgets de cámara
        self.labelCamara     = getattr(self.view, "Camara", None)
        self.btnIniciarCam   = getattr(self.view, "BotonIniciarCamara", None)
        self.btnCapturarFoto = getattr(self.view, "BotonCapturarFoto", None)
        self.btnApagarCam    = getattr(self.view, "BotonApagarCam", None)

        if self.btnIniciarCam:
            self.btnIniciarCam.clicked.connect(self.start_camera)
        if self.btnCapturarFoto:
            self.btnCapturarFoto.clicked.connect(self.capture_photo)
        if self.btnApagarCam:
            self.btnApagarCam.clicked.connect(self.stop_camera)

        # Cargar imagen
        if self.btnCargarImagen:
            self.btnCargarImagen.clicked.connect(self.load_image)
        else:
            print("WARN: BotonCargarImagen no encontrado en la UI.")

        # BOTÓN VISOR 3D
        self.btnVisor3D = getattr(self.view, "AbrirVisor3D", None)

        if self.btnVisor3D:
            self.btnVisor3D.clicked.connect(self.open_visor3d)
        else:
            print("WARN: BotonVisor3D no encontrado en la UI.")


        # BOTONES DE PROCESADO
        if self.btnNormalizar:
            self.btnNormalizar.clicked.connect(self.procesar_normalizar)
        if self.btnFiltrar:
            self.btnFiltrar.clicked.connect(self.procesar_filtrar)
        if self.btnBinarizar:
            self.btnBinarizar.clicked.connect(self.procesar_binarizar)
        if self.btnUmbralizar:
            self.btnUmbralizar.clicked.connect(self.procesar_umbralizar)
        if self.btnMorfologia:
            self.btnMorfologia.clicked.connect(self.procesar_morfologia)
        if self.btnBordes:
            self.btnBordes.clicked.connect(self.procesar_bordes)
        if self.btnComparar:
            self.btnComparar.clicked.connect(self.comparar_imagenes)

        # WIDGETS CSV / TABLA
        self.btnCargarCSV = getattr(self.view, "botonCargarCSV", None)
        self.tablaCSV     = getattr(self.view, "tablaDatosCSV", None)
        self.btnGraficarCols = getattr(self.view, "botonGraficarCols", None)
        self.combosCols = [
            getattr(self.view, "comboBoxCol1", None),
            getattr(self.view, "comboBoxCol2", None),
            getattr(self.view, "comboBoxCol3", None),
            getattr(self.view, "comboBoxCol4", None)
        ]
        self.widgetCSV = getattr(self.view, "widgetGraficas", None)
        self.canvas_csv = self._setup_graph(self.widgetCSV)

        if self.btnCargarCSV:
            self.btnCargarCSV.clicked.connect(self.load_csv_logic)
        if self.btnGraficarCols:
            self.btnGraficarCols.clicked.connect(self.plot_csv_logic)


    # MÉTODOS DE SEÑALES (MAT / FFT)
    def load_mat_logic(self):
        """Carga el archivo .mat, asegura su forma 2D y prepara los widgets de señales."""
        try:
            path, _ = QFileDialog.getOpenFileName(self.view, "Abrir MAT", "", "Archivos MAT (*.mat)")
            if not path:
                print("DEBUG: usuario canceló abrir MAT")
                return

            print("DEBUG: cargando .mat desde:", path)
            datos = self.model.cargar_mat(path)

            print("DEBUG: cargar_mat devolvió:", type(datos), getattr(datos, "shape", None))

            if datos is None:
                QMessageBox.warning(self.view, "Error", "No se pudo cargar el archivo .mat (None).")
                self.datos_senal = None
                return

            datos = np.squeeze(datos)
            datos = np.atleast_2d(datos)

            if datos.ndim > 2:
                try:
                    datos = datos.reshape(datos.shape[0], -1)
                except Exception:
                    datos = np.atleast_2d(datos.flatten())

            if datos.shape[0] > datos.shape[1] and datos.shape[1] < 100:
                datos = datos.T

            self.datos_senal = datos
            n_canales = datos.shape[0]

            print("DIAGNÓSTICO: Señal cargada. Forma final:", self.datos_senal.shape, "Canales:", n_canales)

            if self.comboCanal:
                try:
                    self.comboCanal.blockSignals(True)
                    self.comboCanal.clear()
                    self.comboCanal.addItems([f"Canal {i+1}" for i in range(n_canales)])
                    self.comboCanal.blockSignals(False)
                except Exception as e:
                    print("ERROR llenando BoxCanal:", e)
            else:
                print("WARN: BoxCanal no existe en la vista.")

            if self.comboEje:
                try:
                    self.comboEje.clear()
                    self.comboEje.addItems(["Eje 0 (Entre Canales)", "Eje 1 (En el Tiempo)"])
                except Exception as e:
                    print("ERROR llenando ComboBoxEje:", e)

            if self.tablaFreq is not None:
                try:
                    self.tablaFreq.setRowCount(0)
                    self.tablaFreq.setColumnCount(0)
                except Exception as e:
                    print("ERROR limpiando tablaFrecuencias:", e)

            if n_canales > 0:
                try:
                    if self.comboCanal:
                        self.comboCanal.setCurrentIndex(0)
                except Exception:
                    pass
                self.actualizar_canal_y_fft()
            else:
                print("WARN: No se detectaron canales en el archivo .mat")

        except Exception as e:
            print("ERROR load_mat_logic:", e)
            QMessageBox.critical(self.view, "Error", f"Error al cargar MAT: {e}")

    def actualizar_canal_y_fft(self):
        """Grafica la señal del canal seleccionado y calcula/grafica su FFT."""
        try:
            if self.datos_senal is None:
                print("DEBUG actualizar_canal_y_fft: datos_senal es None")
                return

            idx = 0
            if self.comboCanal:
                idx = self.comboCanal.currentIndex()
            else:
                print("WARN: BoxCanal inexistente, usaremos índice 0")

            if idx is None or idx < 0 or idx >= self.datos_senal.shape[0]:
                print("WARN: índice de canal inválido:", idx)
                return

            signal = self.datos_senal[idx, :].astype(float)
            print(f"DEBUG: graficando canal {idx}, samples={signal.size}")

            if self.canvas_canal:
                try:
                    fig_canal = self.canvas_canal.figure
                    fig_canal.clear()
                    ax = fig_canal.add_subplot(111)
                    ax.plot(signal, color='#0055ff', linewidth=0.8)
                    ax.set_title(f"Señal en el Tiempo - Canal {idx + 1}")
                    ax.set_xlabel("Muestras")
                    ax.grid(True, linestyle='--', alpha=0.6)
                    self.canvas_canal.draw()
                except Exception as e:
                    print("ERROR dibujando canvas_canal:", e)

            if not hasattr(self.model, "fft_analisis"):
                print("ERROR: modelo no tiene fft_analisis")
                return

            df_fft, ruta = self.model.fft_analisis(signal, self.fs)
            print("DEBUG: fft_analisis devolvió df shape:", getattr(df_fft, "shape", None), " ruta:", ruta)

            if df_fft is None or df_fft.empty:
                print("DIAGNÓSTICO: La FFT no devolvió datos. La tabla de frecuencias está vacía.")
                if self.tablaFreq:
                    self.tablaFreq.setRowCount(0)
                return

            try:
                freqs = df_fft.iloc[:, 0].values
                mags = df_fft.iloc[:, 1].values
            except Exception as e:
                print("ERROR extrayendo columnas df_fft:", e)
                if self.tablaFreq: self.tablaFreq.setRowCount(0)
                return

            if self.tablaFreq:
                try:
                    limit = min(50, len(freqs))
                    self.tablaFreq.setRowCount(limit)
                    self.tablaFreq.setColumnCount(2)
                    self.tablaFreq.setHorizontalHeaderLabels(["Frecuencia (Hz)", "Magnitud"])
                    for i in range(limit):
                        self.tablaFreq.setItem(i, 0, QTableWidgetItem(f"{freqs[i]:.4f}"))
                        self.tablaFreq.setItem(i, 1, QTableWidgetItem(f"{mags[i]:.6e}"))
                    print("DIAGNÓSTICO: Tabla de frecuencias cargada con éxito.")
                except Exception as e:
                    print("ERROR llenando tablaFrecuencias:", e)
                    QMessageBox.critical(self.view, "Error UI", "Fallo al llenar la tabla de frecuencias.")
            else:
                print("WARN: tablaFrecuencias no existe en UI; no se muestra tabla")

            if self.canvas_histo:
                try:
                    fig_histo = self.canvas_histo.figure
                    fig_histo.clear()
                    ax = fig_histo.add_subplot(111)
                    ax.plot(freqs, mags, color='#ff0055')
                    ax.set_title(f"Espectro FFT - Canal {idx + 1}")
                    ax.set_xlabel("Frecuencia (Hz)")
                    ax.grid(True)
                    self.canvas_histo.draw()
                except Exception as e:
                    print("ERROR dibujando canvas_histo:", e)

        except Exception as e:
            print("ERROR actualizar_canal_y_fft:", e)


    # HISTOGRAMA STD

    def graficar_histograma_std(self):
        if self.datos_senal is None:
            QMessageBox.warning(self.view, "STD", "Primero cargue un archivo .mat.")
            return

        eje_idx = 0
        if self.comboEje and "1" in self.comboEje.currentText():
            eje_idx = 1

        std_data = self.model.desviacion_estandar(self.datos_senal, eje=eje_idx)

        if self.canvas_histo:
            try:
                fig_histo = self.canvas_histo.figure
                fig_histo.clear()
                ax = fig_histo.add_subplot(111)
                ax.hist(std_data, bins=30, edgecolor="black", alpha=0.7)
                if eje_idx == 1:
                    ax.set_title("Histograma de Desviación Estándar por Canal")
                    ax.set_xlabel("Valor STD")
                else:
                    ax.set_title("Histograma de Desviación Estándar por Muestra de Tiempo")
                    ax.set_xlabel("Valor STD")
                ax.grid(True, alpha=0.3)
                self.canvas_histo.draw()
            except Exception as e:
                print("ERROR graficar_histograma_std (dibujar):", e)

    
    # IMAGEN: CARGAR, PROCESAR Y MOSTRAR
    def load_image(self):
        """Carga imagen y la muestra en VistaPreviaImagen (grayscale si es 2D)."""
        print(">>> load_image ejecutado")
        filtros = (
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.dcm *.nii *.nii.gz);;"
            "DICOM (*.dcm);;"
            "NIFTI (*.nii *.nii.gz);;"
            "JPEG (*.jpg *.jpeg);;"
            "PNG (*.png);;"
            "BMP (*.bmp)"
        )
        path, _ = QFileDialog.getOpenFileName(self.view, "Abrir imagen", "", filtros)
        print("Ruta seleccionada:", path)
        if not path:
            return

        img = self.model.cargar_imagen(path)
        if img is None:
            QMessageBox.warning(self.view, "Imagen", "Error al cargar imagen")
            return

        self.imagen_original = img.copy()
        self.imagen_procesada = img.copy()

        self._mostrar_img(self.imagen_procesada)

    def _mostrar_img(self, img):
        """Muestra la imagen (grayscale o BGR) en el widget VistaPreviaImagen."""
        lbl = getattr(self.view, "VistaPreviaImagen", None)
        if lbl is None or img is None:
            print("WARN: VistaPreviaImagen no existe o img es None")
            return

        try:
            if len(img.shape) == 2:
                h, w = img.shape
                # asegurar uint8
                if img.dtype != np.uint8:
                    arr = img.astype(np.float32)
                    arr -= arr.min()
                    if arr.max() > 0:
                        arr = (arr / arr.max()) * 255.0
                    img_u8 = arr.astype(np.uint8)
                else:
                    img_u8 = img
                bytes_per_line = w
                qimg = QImage(img_u8.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
            else:
                # color BGR -> convertir a RGB
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch = img_rgb.shape
                bytes_per_line = w * ch
                qimg = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

            lbl.setPixmap(QPixmap.fromImage(qimg).scaled(lbl.width(), lbl.height(), Qt.KeepAspectRatio))
        except Exception as e:
            print("ERROR _mostrar_img:", e)

    # PROCESOS DE IMAGEN
    def procesar_normalizar(self):
        if self.imagen_original is None:
            QMessageBox.warning(self.view, "Procesar", "Cargue una imagen primero")
            return
        try:
            img = self.model.normalizar_imagen(self.imagen_original)
            self.imagen_procesada = img
            self._mostrar_img(img)
        except Exception as e:
            print("ERROR procesar_normalizar:", e)

    def procesar_filtrar(self):
        if self.imagen_original is None:
            QMessageBox.warning(self.view, "Procesar", "Cargue una imagen primero")
            return
        try:
            img = self.model.filtrar_imagen(self.imagen_original)
            self.imagen_procesada = img
            self._mostrar_img(img)
        except Exception as e:
            print("ERROR procesar_filtrar:", e)

    def procesar_binarizar(self):
        if self.imagen_original is None:
            QMessageBox.warning(self.view, "Procesar", "Cargue una imagen primero")
            return
        try:
            img = self.model.binarizar_imagen(self.imagen_original)
            self.imagen_procesada = img
            self._mostrar_img(img)
        except Exception as e:
            print("ERROR procesar_binarizar:", e)

    def procesar_umbralizar(self):
        if self.imagen_original is None:
            QMessageBox.warning(self.view, "Procesar", "Cargue una imagen primero")
            return
        try:
            img = self.model.umbralizar_imagen(self.imagen_original)
            self.imagen_procesada = img
            self._mostrar_img(img)
        except Exception as e:
            print("ERROR procesar_umbralizar:", e)

    def procesar_morfologia(self):
        if self.imagen_original is None:
            QMessageBox.warning(self.view, "Procesar", "Cargue una imagen primero")
            return
        try:
            img = self.model.morfologia(self.imagen_original, "dilatacion")
            self.imagen_procesada = img
            self._mostrar_img(img)
        except Exception as e:
            print("ERROR procesar_morfologia:", e)

    def procesar_bordes(self):
        if self.imagen_original is None:
            QMessageBox.warning(self.view, "Procesar", "Cargue una imagen primero")
            return
        try:
            img = self.model.detectar_bordes(self.imagen_original)
            self.imagen_procesada = img
            self._mostrar_img(img)
        except Exception as e:
            print("ERROR procesar_bordes:", e)


    # COMPARAR IMAGENES: ORIGINAL vs PROCESADA
    def comparar_imagenes(self):
        """Muestra en VistaPreviaImagen un collage con títulos ORIGINAL / PROCESADA."""
        if self.imagen_original is None or self.imagen_procesada is None:
            QMessageBox.warning(self.view, "Comparar", "Debe cargar y procesar una imagen primero")
            return

        try:
            orig = self.imagen_original.copy()
            proc = self.imagen_procesada.copy()

            # Asegurar mismo tamaño
            if orig.ndim != proc.ndim:
                # convertir a 3 canales si uno es grayscale
                if orig.ndim == 2 and proc.ndim == 3:
                    orig = cv2.cvtColor(orig, cv2.COLOR_GRAY2BGR)
                elif proc.ndim == 2 and orig.ndim == 3:
                    proc = cv2.cvtColor(proc, cv2.COLOR_GRAY2BGR)

            if orig.shape != proc.shape:
                proc = cv2.resize(proc, (orig.shape[1], orig.shape[0]))

            font = cv2.FONT_HERSHEY_SIMPLEX
            title_height = 40
            title_bar_orig = 255 * np.ones((title_height, orig.shape[1], 3), dtype=np.uint8)
            title_bar_proc = 255 * np.ones((title_height, proc.shape[1], 3), dtype=np.uint8)
            cv2.putText(title_bar_orig, "ORIGINAL", (10, 28), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(title_bar_proc, "PROCESADA", (10, 28), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

            if orig.ndim == 2:
                orig = cv2.cvtColor(orig, cv2.COLOR_GRAY2BGR)
            if proc.ndim == 2:
                proc = cv2.cvtColor(proc, cv2.COLOR_GRAY2BGR)

            orig_with_title = np.vstack((title_bar_orig, orig))
            proc_with_title = np.vstack((title_bar_proc, proc))
            collage = np.hstack((orig_with_title, proc_with_title))

            lbl = getattr(self.view, "VistaPreviaImagen", None)
            if lbl:
                h, w, ch = collage.shape
                bytes_per_line = w * ch
                qimg = QImage(collage.data, w, h, bytes_per_line, QImage.Format_RGB888)
                lbl.setPixmap(QPixmap.fromImage(qimg).scaled(lbl.width(), lbl.height(), Qt.KeepAspectRatio))
        except Exception as e:
            print("ERROR comparar_imagenes:", e)
            QMessageBox.critical(self.view, "Comparar", f"Error al generar comparación: {e}")

    def open_visor3d(self):
        if not hasattr(self, "visor3d") or self.visor3d is None:
            self.visor3d = ControladorVisor3D(self.model, self.usuario)
        self.visor3d.show()


    # RESTO: CÁMARA / CSV / VISOR 3D 
    def show(self):
        self.view.show()

    # Cámara
    def start_camera(self):
        if not self.model.iniciar_camara():
            QMessageBox.warning(self.view, "Cámara", "No se pudo abrir la cámara")
            return
        self.timer.start(30)

    def _update_frame(self):
        try:
            frame = self.model.leer_frame()
            if frame is None or self.labelCamara is None:
                return
            h, w, ch = frame.shape
            bytes_per_line = w * ch
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.labelCamara.setPixmap(
                QPixmap.fromImage(qimg).scaled(
                    self.labelCamara.width(),
                    self.labelCamara.height(),
                    Qt.KeepAspectRatio
                )
            )
        except Exception as e:
            print("ERROR _update_frame:", e)

    def capture_photo(self):
        path = self.model.capturar_foto(self.usuario)
        if path:
            QMessageBox.information(self.view, "Foto", f"Guardada en:\n{path}")
            self.stop_camera()

    def stop_camera(self):
        try:
            self.timer.stop()
            self.model.apagar_camara()
            if self.labelCamara:
                self.labelCamara.setText("Cámara apagada")
        except Exception as e:
            print("ERROR stop_camera:", e)


    def open_visor3d(self):
        if not hasattr(self, "visor3d") or self.visor3d is None:
            self.visor3d = ControladorVisor3D(self.model, self.usuario)
        self.visor3d.show()


    # CSV: carga y graficado de columnas
    def load_csv_logic(self):
        print("CLIC EN CARGAR CSV")
        path, _ = QFileDialog.getOpenFileName(self.view, "Abrir CSV", "", "Archivos CSV (*.csv)")
        if not path:
            return

        try:
            df = self.model.cargar_csv(path)
            if df is None:
                return

            self._df_actual = df
            columnas = list(df.columns)

            if self.tablaCSV:
                self.tablaCSV.setRowCount(min(len(df), 100))
                self.tablaCSV.setColumnCount(len(columnas))
                self.tablaCSV.setHorizontalHeaderLabels(columnas)
                for i in range(min(len(df), 100)):
                    for j, val in enumerate(df.iloc[i]):
                        self.tablaCSV.setItem(i, j, QTableWidgetItem(str(val)))

            columnas_numericas = [
                col for col in columnas
                if pd.api.types.is_numeric_dtype(df[col])
            ]
            self._columnas_numericas = columnas_numericas

            print("Columnas numéricas detectadas:", columnas_numericas)

            for cb in self.combosCols:
                if cb is not None:
                    cb.blockSignals(True)
                    cb.clear()
                    cb.addItem("Ninguna")
                    cb.addItems(columnas_numericas)
                    cb.blockSignals(False)

        except Exception as e:
            print(f" Error CSV: {e}")


    def plot_csv_logic(self):
        if not hasattr(self, "_df_actual") or self._df_actual is None:
            QMessageBox.warning(self.view, "Atención", "Primero cargue un archivo CSV")
            return

        columnas_a_graficar = [cb.currentText() for cb in self.combosCols if cb and cb.currentText() not in ["", "Ninguna"]]

        if not columnas_a_graficar:
            QMessageBox.warning(self.view, "Atención", "Seleccione al menos una columna.")
            return

        if self.canvas_csv:
            ax = self.canvas_csv.figure.add_subplot(111)
            ax.clear()

            for col in columnas_a_graficar:
                try:
                    datos = pd.to_numeric(self._df_actual[col], errors='coerce').dropna()
                    if not datos.empty:
                        ax.plot(datos.values, label=col, alpha=0.8)
                except Exception as e:
                    print(f"Error al graficar columna {col}: {e}")

            ax.legend()
            ax.set_title("Gráfica de Columnas Tabulares")
            ax.grid(True)
            self.canvas_csv.draw()
