import customtkinter as ctk
from views.esta_vacio import vacio, papelera_vacia
from controllers.facturas_controller import get_facturas, get_papelera_facts, busqueda
from views.factura import factura

class Tarjeta(ctk.CTkFrame):
    def __init__(self, parent,id, tipo, nro, descripcion, fecha_emision,command=None, max_width=200, padding=(10, 10)):
        super().__init__(parent, border_width=2, border_color="gray", cursor="hand2", fg_color="transparent", bg_color="transparent")
        self.id = id
        self.command = command
        self.titulo = nro
        self.tipo = tipo
        self.descripcion = descripcion
        self.fecha_emision= fecha_emision

        # Frame interno para añadir padding
        self.inner_frame = ctk.CTkFrame(self, bg_color="transparent", fg_color="transparent")
        self.inner_frame.pack(padx=padding[0], pady=padding[1], fill="both", expand=True)

        self.titulo_label = ctk.CTkLabel(self.inner_frame, text=f"Nro: {nro}", font=("Arial", 16, "bold"), wraplength=max_width, anchor="w")
        self.titulo_label.pack(pady=(0,5), padx=5, fill="both")

        self.tipo_label = ctk.CTkLabel(self.inner_frame, text=f"Tipo: {tipo}", font=("Arial", 14), wraplength=max_width, anchor="w")
        self.tipo_label.pack(pady=(0, 5), padx=5, fill="both")

        self.descripcion_label = ctk.CTkLabel(self.inner_frame, text=f"Motivo: {descripcion}", font=("Arial", 12), wraplength=max_width, anchor="w")
        self.descripcion_label.pack(pady=5, padx=5, fill="both")

        self.fecha_emision_label = ctk.CTkLabel(self.inner_frame, text=f"Fecha de Emisión: {fecha_emision}", font=("Arial", 12), wraplength=max_width, anchor="w")
        self.fecha_emision_label.pack(pady=5, padx=5, fill="both")

        self.bind("<Button-1>", self.on_click)
        self.titulo_label.bind("<Button-1>", self.on_click)
        self.tipo_label.bind("<Button-1>", self.on_click)
        self.descripcion_label.bind("<Button-1>", self.on_click)
        self.fecha_emision_label.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if self.command:
            self.command(self.id, self.tipo)

class Facturas:
    def __init__(self, app, data_user, is_papelera=False,is_buscador=False, val_buscador=None):
        self.app=app
        self.data_user= data_user
        self.is_papelera=is_papelera
        self.is_buscador=is_buscador
        self.val_buscador=val_buscador

        if self.is_papelera:
            self.tarjetas_data = get_papelera_facts(self.app)

        elif self.is_buscador:
            self.tarjetas_data = busqueda(self.app, self.val_buscador)

        else:
            self.tarjetas_data = get_facturas(self.app)
                # self.tarjetas_data = {}
            if not self.tarjetas_data:
                self.frame_vacio =vacio(self.app)
            else:
                self.actualizar_interfaz()
            # self.scroll_frame_facturas = ctk.CTkScrollableFrame(self.app)
            # self.scroll_frame_facturas.pack(side="right", fill="both", expand=True)

            # self.create_tarjetas()

    def create_tarjetas(self):

        columns = 3  # Número de columnas antes de saltar a la siguiente fila
        row = 0
        col = 0
        max_width = 250  # Ancho máximo para las tarjetas

        for data in self.tarjetas_data:
            tarjeta = Tarjeta(self.scroll_frame_facturas, data["id"], data["tipo"],data["nro"], data["descripcion"],data["fecha"], self.on_tarjeta_click, max_width=max_width, padding=(20, 20))
            tarjeta.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def show(self):
        if not self.tarjetas_data:
             self.frame_vacio.show()
        else:
            self.scroll_frame_facturas.pack(fill="both", expand=True)

    def hide(self):
         if not self.tarjetas_data:
             self.frame_vacio.hide()
         else:
            self.scroll_frame_facturas.pack_forget()

    def on_tarjeta_click(self, id, tipo):
         factura(self.app, id, tipo, self, self.data_user, self.is_papelera)
    
    def actualizar_interfaz(self):
        # Destruir el scroll_frame actual si existe
        if hasattr(self, 'scroll_frame'):
            self.scroll_frame_facturas.destroy()

        # Obtener los datos actualizados de las facturas
        if self.is_papelera:
            self.tarjetas_data = get_papelera_facts(self.app)
            # self.tarjetas_data = {}
            if not self.tarjetas_data:
                self.frame_vacio =papelera_vacia(self.app)
            else:
                # Crear un nuevo scroll_frame y poblarlo con las tarjetas actualizadas
                self.scroll_frame_facturas = ctk.CTkScrollableFrame(self.app)
                self.scroll_frame_facturas.pack(side="right", fill="both", expand=True)
                self.create_tarjetas()

        elif self.is_buscador:
            self.tarjetas_data = busqueda(self.app, self.val_buscador)
            if not self.tarjetas_data:
                self.frame_vacio =papelera_vacia(self.app, is_buscador=True)
            else:
                # # Crear un nuevo scroll_frame y poblarlo con las tarjetas actualizadas
                self.scroll_frame_facturas = ctk.CTkScrollableFrame(self.app,  fg_color="transparent",  bg_color="transparent")
                self.scroll_frame_facturas.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)
                self.create_tarjetas()
            
        else:
            self.tarjetas_data = get_facturas(self.app)
            if not self.tarjetas_data:
                self.frame_vacio =vacio(self.app)
            else:
                # Crear un nuevo scroll_frame y poblarlo con las tarjetas actualizadas
                self.scroll_frame_facturas = ctk.CTkScrollableFrame(self.app)
                self.scroll_frame_facturas.pack(side="right", fill="both", expand=True)
                self.create_tarjetas()
