import customtkinter as ctk
import os
from PIL import Image



class vacio:
    def __init__(self, app):
        # Crear el CTkScrollableFrame
        self.scroll_frame =  ctk.CTkScrollableFrame(app)
        self.scroll_frame.pack(side="right", fill="both", expand=True)

        # Ruta actual del archivo
        ruta_actual = os.path.dirname(__file__)
        # Retroceder una carpeta
        image_path = os.path.join(os.path.dirname(ruta_actual), "img/empty.png")
        # Abre la imagen original
        original_image = Image.open(image_path)
        # Obtiene las dimensiones de la imagen original
        ancho, alto = original_image.size
        # Define la caja de recorte (left, upper, right, lower)
        caja_recorte = (0, 0, ancho, alto - 150)

        # Recorta la imagen
        imagen_recortada = original_image.crop(caja_recorte)

          # Crea un objeto CTkImage
        imagen= ctk.CTkImage(light_image=imagen_recortada, size=(600, 450))

        # Muestra la imagen en un CTkLabel
        etiqueta_imagen = ctk.CTkLabel(self.scroll_frame, image=imagen, text="")
        etiqueta_imagen.pack(pady=(30,0))

        button1 = ctk.CTkButton(master=self.scroll_frame, text="Agregar",
                                corner_radius=10, width=200, height=50, 
                                font=("Arial", 16), fg_color="#4824B7",
                                command=lambda: self.open_form(app))
        button1.pack(pady=0, padx=0)

    def open_form(self, app):
        from .form_fact import form

        form(app)

    def show(self):
        self.scroll_frame.pack(fill="both", expand=True)

    def hide(self):
        self.scroll_frame.pack_forget()
        
class papelera_vacia:
    def __init__(self, app, is_buscador=None):

        # Crear el CTkScrollableFrame
        self.scroll_frame =  ctk.CTkScrollableFrame(app, fg_color="transparent", bg_color="transparent")
        self.scroll_frame.pack(side="right", fill="both", expand=True)


        # Ruta actual del archivo
        ruta_actual = os.path.dirname(__file__)

        # Retroceder una carpeta
        if is_buscador:
            image_path = os.path.join(os.path.dirname(ruta_actual), "img/buscador_vacio.png")
        else:
            image_path = os.path.join(os.path.dirname(ruta_actual), "img/pepelera_vacia.png")

        # Abre la imagen original
        original_image = Image.open(image_path)


          # Crea un objeto CTkImage
        imagen= ctk.CTkImage(light_image=original_image, size=[600,600])

        # Muestra la imagen en un CTkLabel
        etiqueta_imagen = ctk.CTkLabel(self.scroll_frame, image=imagen, text="")
        etiqueta_imagen.pack(pady=(30,0))

    def show(self):
        self.scroll_frame.pack(fill="both", expand=True)

    def hide(self):
        self.scroll_frame.pack_forget()
        