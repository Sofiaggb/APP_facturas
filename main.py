# rmdir /s /q C:\xampp\htdocs\MIS_PROYECTOS\SISTEMA_FACTURACION\SistemaFacturacion
# python -3.12 -m venv SistemaFacturacion
#  $

import customtkinter as ctk
import os
from PIL import Image, ImageDraw, ImageTk
from views.facturas import Facturas
from views.buscador import Buscador
from views.form_fact import form

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class AplicacionPantallaCompleta(ctk.CTkToplevel):
    def __init__(self, parent,data_user):
        super().__init__(parent)
        self.app=self
        self.data_user= data_user
        # self.app = app
        # self.app=ctk.CTkToplevel(app)
        self.app.title("Almacenamiento de Facturas")
        self.app.geometry("1350x700+0+0")
        self.login_window=parent
        print(data_user)


        # Crear un frame para el menú lateral
        side_menu = ctk.CTkFrame(master=self.app, corner_radius=0)
        side_menu.pack(side="left", fill="y")
        # Obtén la ruta del directorio actual (donde se encuentra tu script)
        self.image_path = os.path.join(os.path.dirname(__file__), "img/logo.jpg")
        # self.image_path = "C:\xampp\htdocs\MIS_PROYECTOS\SISTEMA_FACTURACION\img\logo.jpg"
        # Abre la imagen original
        self.original_image = Image.open(self.image_path)
        # Crea una máscara para la forma circular
        self.mask = Image.new('L', self.original_image.size, 0)
        self.draw = ImageDraw.Draw(self.mask) 
        self.draw.ellipse((0, 0) + self.original_image.size, fill=255)
        # Aplica la máscara a la imagen original
        self.rounded_image = Image.new("RGBA", self.original_image.size)
        self.rounded_image.paste(self.original_image, mask=self.mask)
        # Crea un objeto CTkImage
        self.imagen= ctk.CTkImage(light_image=self.rounded_image, size=(100, 100))
        
        # Muestra la imagen en un CTkLabel
        self.etiqueta_imagen = ctk.CTkLabel(side_menu, image=self.imagen, text="")
        self.etiqueta_imagen.pack(pady=(30,0))

        # usuario 
        user = ctk.CTkLabel(master=side_menu, text=data_user["user"], font=("Arial", 26))
        user.pack(pady=(20,10), padx=0)
        # self.imagen = imagen

        # Crear los botones 
        if self.data_user["user"] == "superAdmin" or self.data_user["user"] == "admin":
            button0 = ctk.CTkButton(master=side_menu, text="Movimientos de Usuarios", width=200, 
                                    height=50, font=("Arial", 16), fg_color="#4824B7",
                                    command=self.usuarios)
            button0.pack(pady=(10,0), padx=0)

        if self.data_user["user"] == "superAdmin":
            button6 = ctk.CTkButton(master=side_menu, text="Eliminar Usuarios", width=200, 
                                    height=50, font=("Arial", 16), fg_color="#4824B7",
                                    command=self.administrar_usuarios)
            button6.pack(pady=(10,0), padx=0)
           
        button2 = ctk.CTkButton(master=side_menu, text="Facturas 📄",corner_radius=0, width=300, height=50, font=("Arial", 16), fg_color="#323232",
                                    command=self.mostrar_facturas)
        
        if self.data_user["user"] == "superAdmin" or self.data_user["user"] == "admin":
            button1 = ctk.CTkButton(master=side_menu, text="Agregar",corner_radius=0, width=300, height=50, font=("Arial", 16), fg_color="#323232",
                                    command=self.open_form)
            button1.pack(pady=(70,0), padx=0)

            button2.pack(pady=0, padx=0)
        else:

            button2.pack(pady=(70,0), padx=0)
        
        button3 = ctk.CTkButton(master=side_menu, text="Buscador 🔍",corner_radius=0, width=300, height=50, font=("Arial", 16), fg_color="#323232",
                                command=self.mostrar_buscador)
        button3.pack(pady=0, padx=0)


        button4 = ctk.CTkButton(master=side_menu, text="Papelera 🗑️",corner_radius=0, width=300, height=50, font=("Arial", 16), fg_color="#323232",
                                command=self.mostrar_papelera)
        button4.pack(pady=0, padx=0)
        # Crear un frame para los botones
        buttons_frame = ctk.CTkFrame(master=side_menu)
        buttons_frame.pack(side='bottom', fill='x', pady=0, padx=0)

        button5 = ctk.CTkButton(master=buttons_frame, text="i",corner_radius=200, 
                                width=50, height=50, font=("Times New Roman", 24), 
                                fg_color="#323232", command=self.infromacion)
        button5.pack(side='left', fill='x', pady=0, padx=(20,20))
        # Botón de Cerrar Sesión
        button_logout = ctk.CTkButton(master=buttons_frame, text="Cerrar Sesión 🚪",
                                       corner_radius=0, width=230, height=50,
                                         font=("Arial", 14), fg_color="#323232",
                                         command= self.cerrar_sesion)
        button_logout.pack(side='left', fill='x', pady=0, padx=0)

        self.facturas_section = Facturas(self.app, data_user= self.data_user)

        self.current_section = self.facturas_section

        # Configurar el evento de cierre para llamar a self.cerrar_ventanas
        self.app.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)

    def cerrar_ventanas(self):
        # Cierra ambas ventanas
        self.app.destroy()
        self.login_window.destroy()

    def cerrar_sesion(self):
        from controllers.users_controller import cerrar_sesion
        from views.messages import ConfirmacionEliminar

        def callback(respuesta):
            if respuesta:
                cerrar_sesion(self.app, self.data_user["ID"])
                
                self.app.destroy()
                self.login_window.deiconify()
        
           # Crear y mostrar la ventana de confirmación
        ventana_confirmacion = ConfirmacionEliminar(self, callback, "¿Estás seguro de querer cerrar sesión?")
        ventana_confirmacion.mainloop()
        print("Sesión cerrada")

    
    def open_form(self):
        form(self.app, facturas_section=self.facturas_section)
        
    def mostrar_facturas(self):
        if self.current_section:
            self.current_section.hide()
        self.facturas_section.actualizar_interfaz()
        self.facturas_section.show()
        self.current_section = self.facturas_section
    
    def mostrar_buscador(self):
        
        self.buscador_section = Buscador(self.app, self.data_user)
        if self.current_section:
            self.current_section.hide()
        self.buscador_section.show()
        self.current_section = self.buscador_section

    def mostrar_papelera(self):
        self.papelera_section = Facturas(self.app, self.data_user, True)

        if self.current_section:
            self.current_section.hide()
        self.papelera_section.actualizar_interfaz()
        self.papelera_section.show()
        self.current_section = self.papelera_section

    def usuarios(self):
        from views.usuario import Usuario
        Usuario(self.app)

    def administrar_usuarios(self):
        from views.eliminar_usuario import eliminarUsuario
        eliminarUsuario(self.app)

    def infromacion(self):
        from views.info import Info
        Info(self.app)

# app =ctk.CTk()
# AplicacionPantallaCompleta(app,"holi")

# app.mainloop()