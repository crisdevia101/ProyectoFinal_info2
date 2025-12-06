import mysql.connector

class MySQLManager:
    def __init__(self):

        DB_NAME = "PMDA_DB"
        APP_USER = "Informatica1"
        APP_PASSWORD = "info2025_2"

        try:
            print("\n[MYSQL] Iniciando configuración automática...")

            admin_conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  
                port=3306
            )
            admin_cursor = admin_conn.cursor()

            admin_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
            print(f"[MYSQL] Base de datos '{DB_NAME}' verificada.")

            admin_cursor.execute(f"""
                CREATE USER IF NOT EXISTS '{APP_USER}'@'localhost'
                IDENTIFIED BY '{APP_PASSWORD}';
            """)
            print(f"[MYSQL] Usuario '{APP_USER}' verificado.")

            admin_cursor.execute(f"""
                GRANT ALL PRIVILEGES ON {DB_NAME}.* 
                TO '{APP_USER}'@'localhost';
            """)
            admin_cursor.execute("FLUSH PRIVILEGES;")
            admin_conn.commit()

            admin_cursor.close()
            admin_conn.close()
            print("[MYSQL] Permisos actualizados.\n")

            print("[MYSQL] Conectando con el usuario de la aplicación...")

            self.conn = mysql.connector.connect(
                host="localhost",
                user=APP_USER,
                password=APP_PASSWORD,
                database=DB_NAME,
                port=3306
            )
            self.cursor = self.conn.cursor()

            print("[MYSQL] Conexión exitosa.\n")
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
        print("[MYSQL] Tabla 'registro_actividad' lista.")
