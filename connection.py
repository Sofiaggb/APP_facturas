# python -m venv SistemaFacturacion    (crear un entorno virtual)
# deactivate    (desactivar el entorno virtual)
import mysql.connector

class connection_bd:
    def __init__(self):
        self.connection= mysql.connector.connect(
            host= "localhost",
            user="sofia",
            password="sofia",
            database="caromac"
        )
        self.cursor= self.connection.cursor()
