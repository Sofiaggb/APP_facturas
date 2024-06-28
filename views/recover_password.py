import customtkinter as ctk
from tkinter import StringVar

class password(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Guarda una referencia a la ventana principal
        # self.app = self
        self.title("Contraseña")
        self.geometry("400x350") #tamaño de la ventana
        self.center_window(parent)
        self.resizable(False, False)
        self.scroll = ctk.CTkScrollableFrame(master=self, width=400, height=350,  fg_color="transparent",  bg_color="transparent")
        self.scroll.pack()

        # variables
        self.respuesta1=StringVar()
        self.respuesta2= StringVar()
        self.user=StringVar()

 # preguntas de recuperacion de contraseña
        self.label_usuario = ctk.CTkLabel(self.scroll, text="Usuario:", font=("Arial", 14))
        self.label_usuario.pack(anchor="w", padx=80, pady=(10,0))

        self.entry_usuario = ctk.CTkEntry(self.scroll,textvariable=self.user, width=200, font=("Arial", 14))
        self.entry_usuario.pack(padx=20, pady=(0,10))

        self.label_contraseña_registro = ctk.CTkLabel(self.scroll,
                                                       text="Responde las siguientes preguntas para poder cambiar tu contraseña", 
                                                       font=("Arial", 14), wraplength=350)
        self.label_contraseña_registro.pack(anchor="w", padx=(30,0), pady=10)

        self.label_contraseña_registro = ctk.CTkLabel(self.scroll, text="¿Animal favorito?", font=("Arial", 14))
        self.label_contraseña_registro.pack(anchor="w", padx=80, pady=0)

        self.entry_contraseña_registro = ctk.CTkEntry(self.scroll, textvariable=self.respuesta1,
                                                       show="", width=200, font=("Arial", 14))
        self.entry_contraseña_registro.pack(padx=20, pady=(0,10))

        self.label_contraseña_registro = ctk.CTkLabel(self.scroll, text="¿Cuál es tu heroe?", font=("Arial", 14))
        self.label_contraseña_registro.pack(anchor="w", padx=80, pady=0)

        self.entry_contraseña_registro = ctk.CTkEntry(self.scroll, textvariable=self.respuesta2,
                                                       show="", width=200, font=("Arial", 14))
        self.entry_contraseña_registro.pack(padx=20, pady=(0,10))
        
        self.boton_registro = ctk.CTkButton(self.scroll, text="Enviar", height=40, width=130,
                                            font=("Arial", 16), fg_color="#4824B7",
                                            command=self.comprobar_respuestas)
        self.boton_registro.pack(padx=20, pady=10)

        self.grab_set()  # Hace que la ventana sea modal

    def comprobar_respuestas(self):
        from controllers.users_controller import verificar_respuestas
        respuestas=verificar_respuestas(self, self.user, self.respuesta1, self.respuesta2)
        if respuestas:
            self.mostrar_cabio_password()
    
    def mostrar_cabio_password(self):
        self.scroll.pack_forget()
        # self.user.set("")
        self.respuesta1.set("")
        self.respuesta2.set("")

        self.scroll_passwords = ctk.CTkScrollableFrame(master=self, width=400, height=300,  fg_color="transparent",  bg_color="transparent")
        self.scroll_passwords.pack()

        self.label_contraseña_registro = ctk.CTkLabel(self.scroll_passwords, text="Nueva Contraseña:", font=("Arial", 14))
        self.label_contraseña_registro.pack(anchor="w", padx=80, pady=(20,0))

        self.entry_contraseña_registro = ctk.CTkEntry(self.scroll_passwords,textvariable=self.respuesta1,
                                                       show="", width=200, font=("Arial", 14))
        self.entry_contraseña_registro.pack(padx=20, pady=(0,20))

        self.label_contraseña_registro = ctk.CTkLabel(self.scroll_passwords, text="Vuelva a ingresar la contraseña:", font=("Arial", 14))
        self.label_contraseña_registro.pack(anchor="w", padx=80, pady=0)

        self.entry_contraseña_registro = ctk.CTkEntry(self.scroll_passwords, textvariable=self.respuesta2,
                                                       show="", width=200, font=("Arial", 14))
        self.entry_contraseña_registro.pack(padx=20, pady=(0,10))

        self.boton_registro = ctk.CTkButton(self.scroll_passwords, text="Guardar", height=40, width=130,
                                            font=("Arial", 16), fg_color="#4824B7",
                                            command=self.change_password)
        self.boton_registro.pack(padx=20, pady=10)

    def change_password(self):
        from controllers.users_controller import cambiar_password
        respuesta = cambiar_password(self, self.user, self.respuesta1, self.respuesta2)
        
        if respuesta:
           self.after(3000, self.destroy)

    def center_window(self, parent):
        # Esperar que la ventana se actualice para obtener sus dimensiones
        self.update_idletasks()
        # Calcular la posición central
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
