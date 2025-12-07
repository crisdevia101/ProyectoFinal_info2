from PyQt5.QtWidgets import QApplication
import sys
import resources_rc


from modelo.modelo_1 import Model
from controlador.controlador_login import ControladorLogin
from vista.vista import LoginView


def main():
    app = QApplication(sys.argv)

    model = Model()

    login_view = LoginView()

    controlador_login = ControladorLogin(login_view, model)

    controlador_login.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


