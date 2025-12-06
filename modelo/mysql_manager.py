import mysql.connector

class MySQLManager:
    def __init__(self):
        try:
            # esta es con mi usuario y mi contraseña de mysql
            self.conn = mysql.connector.connect(
                host="127.0.0.1",
                user="DaniSL",         
                password="BioinFo512", 
                database="PMDA_DB",
                port=3306
            )
            self.cursor = self.conn.cursor()
            print("Conexión a MySQL exitosa ")
            self.crear_tabla()
        except mysql.connector.Error as err:
            self.conn = None
            self.cursor = None
            print(f"[ERROR MYSQL] No se pudo conectar: {err}")

    def crear_tabla(self):
        if self.cursor is None:
            print("[ERROR MYSQL] No hay cursor para crear tabla")
            return
        query = """
        CREATE TABLE IF NOT EXISTS registro_actividad (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descripcion VARCHAR(255),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(query)
        self.conn.commit()
        print("Tabla 'registro_actividad' lista")

