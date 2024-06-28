import customtkinter as ctk
from controllers.users_controller import movimientos

class Usuario(ctk.CTkToplevel):
    def __init__(self, parent ):
        super().__init__(parent)
        self.app = self
        # self.data_user= data_user
        self.parent = parent # Guarda una referencia a la ventana principal
        self.app.title("Usuario")
        self.app.geometry("450x400+150+150") #tamaño de la ventana
        self.app.resizable(False, False) # bloqueo de redimencion de la ventana, alto y ancho
        self.app.attributes('-topmost' , True)
        ctk.CTkLabel(self.app, text="Movimientos de los Usuarios", font=("Arial", 16, "bold")).pack( padx=10, pady=10)

 # Crear un frame para la tabla
        table_frame = ctk.CTkScrollableFrame(self.app, height=400, width=450, fg_color="transparent")
        table_frame.pack(padx=(20,0))

#  datos de los movimientos de usuarios
        self.sesions_data= movimientos(self.app)

        # Añadir encabezados de columna
        ctk.CTkLabel(table_frame, text="Usuario", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(table_frame, text="Fecha de Entrada", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(table_frame, text="Fecha de Salida", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10, pady=10)

        for index, sesion in enumerate(self.sesions_data):
            ctk.CTkLabel(table_frame, text=sesion["usuario"], font=("Arial", 12)).grid(row=index+1, column=0, padx=10, pady=5)
            ctk.CTkLabel(table_frame, text=sesion["fecha_entrada"], font=("Arial", 12)).grid(row=index+1, column=1, padx=10, pady=5)
            ctk.CTkLabel(table_frame, text=sesion["fecha_salida"], font=("Arial", 12)).grid(row=index+1, column=2, padx=10, pady=5)
