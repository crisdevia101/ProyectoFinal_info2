import scipy.io
import numpy as np
import pandas as pd
import time
import os

class ModeloSenales:

    def __init__(self):
        self.data = None
        self.fs = 250  

    def cargar_mat(self, path):
        """Carga mat y devuelve array 2D (canales x muestras) o None"""
        try:
            mat = scipy.io.loadmat(path)
            # imprimir keys para debug opcional
            print("DEBUG modelo.cargar_mat keys:", list(mat.keys()))
            data = None
            for key, val in mat.items():
                if not key.startswith("__"):
                    try:
                        arr = np.array(val, dtype=float)
                        if arr.size == 0:
                            continue
                        data = arr
                        print("DEBUG: usando clave:", key, "shape:", data.shape)
                        break
                    except Exception:
                        continue
            if data is None:
                print("WARN modelo.cargar_mat: no se encontró variable válida en .mat")
                return None

            data = np.squeeze(data)
            data = np.atleast_2d(data)

            # si tiene >2 dims, intentar aplanar conservando canales en primer dim
            if data.ndim > 2:
                try:
                    data = data.reshape(data.shape[0], -1)
                except Exception:
                    data = np.atleast_2d(data.flatten())

            # orientación: si filas > columnas y columnas pequeñas => probablemente (muestras x canales)
            if data.shape[0] > data.shape[1] and data.shape[1] < 100:
                data = data.T

            return data
        except Exception as e:
            print("ERROR modelo.cargar_mat:", e)
            return None

    def fft_analisis(self, senal, fs):
        """Calcula FFT y devuelve (DataFrame, ruta_csv). Mantiene orden de frecuencia."""
        try:
            if senal is None or senal.size == 0:
                return pd.DataFrame(), ""

            senal = np.asarray(senal, dtype=float)
            n = senal.size

            fft_vals = np.fft.fft(senal)
            fft_abs = np.abs(fft_vals)[:n // 2]
            fft_abs = fft_abs / n
            if n > 1:
                fft_abs[1:] = fft_abs[1:] * 2

            freqs = np.fft.fftfreq(n, 1.0 / fs)[:n // 2]

            df = pd.DataFrame({
                "Frecuencia (Hz)": freqs,
                "Magnitud": fft_abs
            })

            ts = int(time.time())
            filename = f"resultados_fft_{ts}.csv"
            try:
                df.to_csv(filename, index=False)
            except Exception as e:
                print("WARN no se pudo guardar CSV FFT:", e)
                filename = ""

            return df, filename
        except Exception as e:
            print("ERROR modelo.fft_analisis:", e)
            return pd.DataFrame(), ""

    def desviacion_estandar(self, data, eje=1):
        try:
            arr = np.asarray(data, dtype=float)
            return np.std(arr, axis=eje)
        except Exception as e:
            print("ERROR modelo.desviacion_estandar:", e)
            return np.array([])
