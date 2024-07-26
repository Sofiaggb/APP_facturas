# python -m venv SistemaFacturacion    (crear un entorno virtual)
# deactivate    (desactivar el entorno virtual)
import mysql.connector
import customtkinter as ctk
from mysql.connector import errorcode

class connection_bd:
    def __init__(self):
        try:

            self.connection= mysql.connector.connect(
                host= "localhost",
                user="root",
                password="",
                database="caromack"
            )
            self.cursor= self.connection.cursor()

        except mysql.connector.Error as err:
            print(err)
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
            else:
                self.show_error_message("No se ha podido conectar a la base de datos", err)
    
    def create_database(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE DATABASE caromack")
            self.connection.database = "caromack"
            self.create_tables()

        except mysql.connector.Error as err:
            self.show_error_message("No se pudo crear la base de datos", err)
    
    def create_tables(self):
        tables = {}
        tables['clientes_proveedores'] = (
            "CREATE TABLE clientes_proveedores ("
            "  ID_cli_pvd INT AUTO_INCREMENT PRIMARY KEY,"
            "  nombre_cli_pvd VARCHAR(100) NOT NULL,"
            "  rif_cli_pvd VARCHAR(15) NOT NULL,"
            "  dirección_cli_pvd VARCHAR(100) NOT NULL,"
            "  telefono_cli_pvd VARCHAR(11) NOT NULL"
            ");"
        )
        tables['productos'] = (
            "CREATE TABLE productos ("
            "  ID_pdt INT AUTO_INCREMENT PRIMARY KEY,"
            "  descripción_pdt VARCHAR(100) NOT NULL,"
            "  precio_pdt DECIMAL(10,2) NOT NULL,"
            "  cantidad_pdt INT NOT NULL"
            ");"
        )
        tables['servicios_e_impuestos'] = (
            "CREATE TABLE servicios_e_impuestos ("
            "  ID_serv_impto INT AUTO_INCREMENT PRIMARY KEY,"
            "  descripcion_serv_impto VARCHAR(100) NOT NULL,"
            "  monto_serv_impto DECIMAL(10,2) NOT NULL"
            ");"
        )
        tables['facturas'] = (
            "CREATE TABLE facturas ("
            "  ID_fact INT AUTO_INCREMENT PRIMARY KEY,"
            "  fecha_emision_fact DATE NOT NULL,"
            "  nro_fact VARCHAR(20) NOT NULL,"
            "  ID_cli_pvd INT NOT NULL,"
            "  tipo_fact VARCHAR(15) NOT NULL,"
            "  descripción_fact VARCHAR(100) NOT NULL,"
            "  monto_neto INT NOT NULL,"
            "  IVA INT NOT NULL,"
            "  monto_total INT NOT NULL,"
            "  is_deleted BOOLEAN NOT NULL,"
            "  FOREIGN KEY (ID_cli_pvd) REFERENCES clientes_proveedores(ID_cli_pvd)"
            ");"
        )
        tables['articulos_por_factura'] = (
            "CREATE TABLE articulos_por_factura ("
            "  ID_articulo INT AUTO_INCREMENT PRIMARY KEY,"
            "  ID_fact INT NOT NULL,"
            "  ID_pdt INT NOT NULL,"
            "  FOREIGN KEY (ID_fact) REFERENCES facturas(ID_fact),"
            "  FOREIGN KEY (ID_pdt) REFERENCES productos(ID_pdt)"
            ");"
        )
        tables['detalles_factura'] = (
            "CREATE TABLE detalles_factura ("
            "  ID_detalles INT AUTO_INCREMENT PRIMARY KEY,"
            "  ID_fact INT NOT NULL,"
            "  ID_serv_impto INT NOT NULL,"
            "  FOREIGN KEY (ID_fact) REFERENCES facturas(ID_fact),"
            "  FOREIGN KEY (ID_serv_impto) REFERENCES servicios_e_impuestos(ID_serv_impto)"
            ");"
        )
        tables['Usuarios'] = (
            "CREATE TABLE Usuarios ("
            "  id_usuario INT AUTO_INCREMENT PRIMARY KEY,"
            "  nombre_usuario VARCHAR(10) NOT NULL UNIQUE,"
            "  contraseña_usuario VARCHAR(50) NOT NULL,"
            "  pregunta1 VARCHAR(50) NOT NULL,"
            "  pregunta2 VARCHAR(50) NOT NULL"
            ");"
        )
        tables['Sesiones'] = (
            "CREATE TABLE Sesiones ("
            "  ID_sesion INT AUTO_INCREMENT PRIMARY KEY,"
            "  ID_usuario INT NOT NULL,"
            "  fecha_acceso DATETIME NOT NULL,"
            "  fecha_salida DATETIME NOT NULL,"
            "  FOREIGN KEY (ID_usuario) REFERENCES Usuarios(id_usuario)"
            ");"
        )

        for table_name, ddl in tables.items():
            try:
                self.cursor.execute(ddl)
            except mysql.connector.Error as err:
                self.show_error_message(f"Error al crear la tabla {table_name}", err)
    

    def show_error_message(self, message, error):
        root = ctk.CTk()
        root.withdraw()
        error_window = ctk.CTkToplevel(root)
        error_window.title("Error")

        label = ctk.CTkLabel(error_window, text=f"{message}: {error}")
        label.pack(padx=20, pady=20)

        button = ctk.CTkButton(error_window, text="OK", command=lambda: self.close_window(root, error_window))
        button.pack(pady=10)

        error_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(root, error_window))


    def close_window(self, root, window):
        window.destroy()
        root.quit()
    