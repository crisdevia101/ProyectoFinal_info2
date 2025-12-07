from PyQt5.QtWidgets import QMessageBox
from controlador.controlador_ventanamain import ControladorPrincipal
from vista.vista import MainWindowView

class ControladorLogin:
    def __init__(self, vista, model):
        self.vista = vista
        self.model = model

        self.inputUser = self.vista.Usuario
        self.inputPass = self.vista.Password
        self.btnLogin = self.vista.botonIngresar

        self.inputUser.returnPressed.connect(self._focus_pass)
        self.inputPass.returnPressed.connect(self.btnLogin.click)

        self.btnLogin.clicked.connect(self.handle_login)

    def _focus_pass(self):
        self.inputPass.setFocus()

    def show(self):
        self.vista.show()


    def handle_login(self):
        usuario = self.inputUser.text().strip()
        clave   = self.inputPass.text().strip()

        print(">>> DEBUG LOGIN")
        print("USUARIO DIGITADO:", usuario)
        print("CLAVE DIGITADA:", clave)

        if self.model.validar_usuario(usuario, clave):
            print("VALIDACIÓN XML: OK")

            self.model.registrar_actividad(usuario, "login")

            if hasattr(self.vista, "limpiarCampos"):
                self.vista.limpiarCampos()

            # CREAR VENTANA PRINCIPAL
            vista_principal = MainWindowView()
            self.main_ctrl = ControladorPrincipal(vista_principal, self.model, usuario)
            self.main_ctrl.show()

            self.vista.close()

        else:
            print("VALIDACIÓN XML: FALLÓ")
            QMessageBox.warning(self.vista, "Error", "Usuario o contraseña incorrectos")
            self.inputPass.clear()



