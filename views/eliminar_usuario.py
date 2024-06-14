import customtkinter as ctk
from controllers.users_controller import get_users

class eliminarUsuario(ctk.CTkToplevel):
    def __init__(self, parent ):
        super().__init__(parent)
        self.app = self
        # self.data_user= data_user
        self.parent = parent # Guarda una referencia a la ventana principal
        self.app.title("Usuarios")
        self.app.geometry("350x300+150+150") #tamaño de la ventana
        self.app.resizable(False, False) # bloqueo de redimencion de la ventana, alto y ancho
        self.app.attributes('-topmost' , True)
        ctk.CTkLabel(self.app, text="Eliminar de los Usuario", font=("Arial", 16, "bold")).pack( padx=10, pady=10)

        # devolver todos los usuarios
        self.table_frame = ctk.CTkScrollableFrame(self.app, height=400, width=450, fg_color="transparent")
        self.table_frame.pack(padx=(50, 0), pady=(10, 10))

        self.actualizar()

    def table_users(self):
        
            # Añadir encabezados de columna
            ctk.CTkLabel(self.table_frame, text="Usuario", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10)

            for index, usuario in enumerate(self.usuarios):
                ctk.CTkLabel(self.table_frame, text=usuario["usuario"], font=("Arial", 12)).grid(row=index+1, column=0, padx=10, pady=5)
                ctk.CTkButton(master=self.table_frame, text="Eliminar", fg_color="#981111", 
                                                hover_color="#D50C0C", 
                                                width=10,
                                                #  command=lambda id_usuario=usuario["ID"]: print(id_usuario
                                                  command=lambda id_usuario=usuario["ID"]: self.borrar_user(id_usuario)
                                                ).grid(row=index+1, column=1, padx=10, pady=5)
    
    def actualizar(self):
              # Eliminar todos los widgets hijos del frame
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Obtener la lista actualizada de usuarios
        self.usuarios = get_users(self.app)

        # Reconstruir la tabla con los nuevos datos
        self.table_users()



    def borrar_user(self, id):
        from controllers.users_controller import delete_user
        from views.messages import ConfirmacionEliminar
        self.app.attributes('-topmost' , False)
        def callback(respuesta):
            if respuesta:
                delete = delete_user(self.app, id)
                if delete:
                    self.actualizar()
        
           # Crear y mostrar la ventana de confirmación
        ventana_confirmacion = ConfirmacionEliminar(self, callback, "¿Estás seguro de eliminar este usuario?")
        ventana_confirmacion.mainloop()
