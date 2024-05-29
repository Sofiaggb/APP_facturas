import customtkinter as ctk
from tkinter import  StringVar 

class Buscador:
    def __init__(self, app):

        self.contenedor_frame = ctk.CTkFrame(app, fg_color="transparent")
        self.contenedor_frame.pack(side="right", fill="both", expand=True)

        # Crear el CTkFrame para contener el campo de búsqueda y el botón
        self.top_frame = ctk.CTkFrame(self.contenedor_frame, fg_color="transparent")
        self.top_frame.pack(side="top", fill="x", pady=(40,20) )

        # Variable para almacenar la entrada de búsqueda
        self.var_buscar = StringVar()

        # Crear el campo de búsqueda dentro del CTkFrame
        self.campo_buscar = ctk.CTkEntry(self.top_frame, textvariable=self.var_buscar, placeholder_text="Escribe aquí para buscar", width=400)
        self.campo_buscar.pack(side="left", padx=(250, 0))

        # Crear el botón de búsqueda dentro del CTkFrame
        self.buscar_button = ctk.CTkButton(self.top_frame, text="Buscar", width=70,
                                            fg_color="#4824B7",
                                           command=lambda: self.buscar(self.var_buscar.get()))
        self.buscar_button.pack(side="left", padx=5)

        # Crear el CTkScrollableFrame para los resultados de la búsqueda
        self.scroll_frame = ctk.CTkScrollableFrame(self.contenedor_frame)
        self.scroll_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

    
    def show(self):
        self.contenedor_frame.pack(fill="both", expand=True)

    def hide(self):
        self.contenedor_frame.pack_forget()