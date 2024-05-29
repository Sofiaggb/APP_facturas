# rmdir /s /q C:\xampp\htdocs\MIS_PROYECTOS\SISTEMA_FACTURACION\SistemaFacturacion
# python -3.12 -m venv SistemaFacturacion
#  $

import customtkinter as ctk
import os
from PIL import Image, ImageDraw
from views.facturas import Facturas
from views.buscador import Buscador
from views.form_fact import form

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class AplicacionPantallaCompleta:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Almacenamiento de Facturas")
        self.app.geometry("1350x700+0+0")


        # Crear un frame para el menú lateral
        side_menu = ctk.CTkFrame(master=self.app, corner_radius=0)
        side_menu.pack(side="left", fill="y")
        # Obtén la ruta del directorio actual (donde se encuentra tu script)
        image_path = os.path.join(os.path.dirname(__file__), "img/logo.jpg")

        # Abre la imagen original
        original_image = Image.open(image_path)
        # Crea una máscara para la forma circular
        mask = Image.new('L', original_image.size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + original_image.size, fill=255)
        # Aplica la máscara a la imagen original
        rounded_image = Image.new("RGBA", original_image.size)
        rounded_image.paste(original_image, mask=mask)
        # Crea un objeto CTkImage
        imagen= ctk.CTkImage(light_image=rounded_image, size=(100, 100))

        # Muestra la imagen en un CTkLabel
        etiqueta_imagen = ctk.CTkLabel(side_menu, image=imagen, text="")
        etiqueta_imagen.pack(pady=(30,0))

        # usuario 
        user = ctk.CTkLabel(master=side_menu, text="Admin", font=("Arial", 26))
        user.pack(pady=(20,10), padx=0)

        # Crear los botones 
        button0 = ctk.CTkButton(master=side_menu, text="Usuario", width=200, height=50, font=("Arial", 16), fg_color="#4824B7")
        button0.pack(pady=(10,0), padx=0)

        button1 = ctk.CTkButton(master=side_menu, text="Agregar",corner_radius=0, width=300, height=50, font=("Arial", 16), fg_color="#323232",
                                command=lambda: self.open_form(self.app))
        button1.pack(pady=(70,0), padx=0)

        button2 = ctk.CTkButton(master=side_menu, text="Facturas",corner_radius=0, width=300, height=50, font=("Arial", 16), fg_color="#323232",
                                command=self.mostrar_facturas)
        button2.pack(pady=0, padx=0)
        
        button3 = ctk.CTkButton(master=side_menu, text="Buscador",corner_radius=0, width=300, height=50, font=("Arial", 16), fg_color="#323232",
                                command=self.mostrar_buscador)
        button3.pack(pady=0, padx=0)


        button4 = ctk.CTkButton(master=side_menu, text="Papelera",corner_radius=0, width=300, height=50, font=("Arial", 16), fg_color="#323232")
        button4.pack(pady=0, padx=0)

        
        button5 = ctk.CTkButton(master=side_menu, text="Información General",corner_radius=0, width=300, height=50, font=("Arial", 14), fg_color="#323232")
        button5.pack(side='bottom', fill='x', pady=(10, 0), padx=0)

        self.facturas_section = Facturas(self.app)

        self.current_section = self.facturas_section

        self.app.mainloop()
    
    def open_form(self, app):
        form(app)
        
    def mostrar_facturas(self):
        if self.current_section:
            self.current_section.hide()
        self.facturas_section.actualizar_interfaz()
        self.facturas_section.show()
        self.current_section = self.facturas_section
    
    def mostrar_buscador(self):
        
        self.buscador_section = Buscador(self.app)
        if self.current_section:
            self.current_section.hide()
        self.buscador_section.show()
        self.current_section = self.buscador_section







AplicacionPantallaCompleta()

