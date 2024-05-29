import customtkinter as ctk
from controllers.facturas_controller import get_factura

class factura(ctk.CTkToplevel):
    def __init__(self,parent, id, tipo, facturas_section):
        super().__init__(parent)
        # self.parent = parent  # Guarda una referencia a la ventana principal
        self.facturas_section = facturas_section
        # self.app = self
        self.attributes('-topmost' , True)
        self.title("Factura")
        self.geometry("500x600+150+0") #tamaño de la ventana
        self.resizable(False, False)
        self.scroll = ctk.CTkScrollableFrame(master=self,fg_color="#140540", width=500, height=600)
        self.scroll.pack(expand = True,  fill="both")

 # Consulta la información de la factura desde la base de datos
        self.factura_info = get_factura(id, tipo)
        if self.factura_info:
            self.crear_factura_layout(self.factura_info)
        else:
            self.crear_error_layout()

    def crear_factura_layout(self, factura_info):
        # Crear widgets para mostrar la información de la factura
        ctk.CTkLabel(self.scroll, text="Factura", font=("Arial", 24, "bold")).pack(pady=10)

        ctk.CTkLabel(self.scroll, text=f"Nro: {factura_info["nro_fact"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        ctk.CTkLabel(self.scroll, text=f"Fecha de Emisión: {factura_info["fecha_emision_fact"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        ctk.CTkLabel(self.scroll, text=f"Tipo: {factura_info["tipo_fact"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        ctk.CTkLabel(self.scroll, text=f"Descripción: {factura_info["descripción_fact"]}",  wraplength=420, font=("Arial", 16)).pack(anchor="w", padx=20)

        
        ctk.CTkLabel(self.scroll, text="Cliente/Proveedor:", font=("Arial", 18, "bold")).pack(anchor="w", pady=(10, 0), padx=20)
        ctk.CTkLabel(self.scroll, text=f"Nombre: {factura_info["cliente"]["nombre"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        ctk.CTkLabel(self.scroll, text=f"RIF/CI: {factura_info["cliente"]["rif"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        ctk.CTkLabel(self.scroll, text=f"Dirección: {factura_info["cliente"]["dirección"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        ctk.CTkLabel(self.scroll, text=f"Teléfono: {factura_info["cliente"]["teléfono"]}", font=("Arial", 16)).pack(anchor="w", padx=20)

        if factura_info["tipo_fact"] in ["Servicios Públicos",  "Impuestos"]:
            ctk.CTkLabel(self.scroll, text=factura_info["tipo_fact"], font=("Arial", 18, "bold")).pack(anchor="center", pady=(10, 0), padx=20)
            
            # Crear un frame para la tabla de productos
            table_frame = ctk.CTkFrame(self.scroll, bg_color="transparent", fg_color="transparent", height=50)
            table_frame.pack(pady=10, padx=20, fill="both", expand=True)

            # Añadir encabezados de columna
            ctk.CTkLabel(table_frame, text="Descripción", font=("Arial", 16, "bold"), width=200).grid(row=0, column=0, padx=10, pady=5)
            ctk.CTkLabel(table_frame, text="Monto", font=("Arial", 16, "bold")).grid(row=0, column=1, padx=10, pady=5)
            ctk.CTkLabel(table_frame, text="Mes", font=("Arial", 16, "bold")).grid(row=0, column=2, padx=10, pady=5)

        # Añadir los productos en filas
            for index, item in enumerate(factura_info["servicios_impuestos"]):
                ctk.CTkLabel(table_frame, text=item['descripcion_serv_impto'], font=("Arial", 16), wraplength=200, anchor="w", justify="left").grid(row=index+1, column=0, padx=10, pady=5)
                ctk.CTkLabel(table_frame, text=item['monto_serv_impto'], font=("Arial", 16)).grid(row=index+1, column=1, padx=10, pady=5)
                ctk.CTkLabel(table_frame, text=item['meses_serv_impto'], font=("Arial", 16)).grid(row=index+1, column=2, padx=10, pady=5)
       
        else:
            ctk.CTkLabel(self.scroll, text="Productos:", font=("Arial", 18, "bold")).pack(anchor="w", pady=(10, 0), padx=20)
            
            # Crear un frame para la tabla de productos
            table_frame = ctk.CTkScrollableFrame(self.scroll, bg_color="transparent", fg_color="transparent")
            table_frame.pack(pady=10, padx=20, fill="both", expand=True)

            # Añadir encabezados de columna
            ctk.CTkLabel(table_frame, text="Descripción", font=("Arial", 16, "bold"), width=200).grid(row=0, column=0, padx=10, pady=5)
            ctk.CTkLabel(table_frame, text="Precio", font=("Arial", 16, "bold")).grid(row=0, column=1, padx=10, pady=5)
            ctk.CTkLabel(table_frame, text="Cantidad", font=("Arial", 16, "bold")).grid(row=0, column=2, padx=10, pady=5)

            # Añadir los productos en filas
            for index, producto in enumerate(factura_info["productos"]):
                ctk.CTkLabel(table_frame, text=producto['descripción_pdt'], font=("Arial", 16), wraplength=200, anchor="w", justify="left").grid(row=index+1, column=0, padx=10, pady=5)
                ctk.CTkLabel(table_frame, text=producto['precio_pdt'], font=("Arial", 16)).grid(row=index+1, column=1, padx=10, pady=5)
                ctk.CTkLabel(table_frame, text=producto['cantidad_pdt'], font=("Arial", 16)).grid(row=index+1, column=2, padx=10, pady=5)


        # Agregar montos, IVA y neto
        montos_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        montos_frame.pack(anchor="e", padx=30)

        ctk.CTkLabel(montos_frame, text=f"Monto Neto: {factura_info["monto_neto"]}", font=("Arial", 16), anchor="w", justify="left").pack(pady=0, padx=5, anchor="w")
        ctk.CTkLabel(montos_frame, text=f"IVA: {factura_info["IVA"]}", font=("Arial", 16), anchor="w", justify="left").pack(pady=0, padx=5, anchor="w")
        ctk.CTkLabel(montos_frame, text=f"Monto Total: {factura_info["monto_total"]}", font=("Arial", 16), anchor="w", justify="left").pack(pady=0, padx=5, anchor="w")

         # Agregar los botones Eliminar y Editar al final
        buttons_frame = ctk.CTkFrame(self.scroll, bg_color="transparent", fg_color="transparent")
        buttons_frame.pack(anchor="center", padx=20, pady=(0,10))

        delete_button = ctk.CTkButton(buttons_frame, text="Eliminar",  font=("Arial", 16),
                                      command=self.on_delete,
                                       fg_color="#9B0202", hover_color="#DC0F0F",height=40, width=80)
        delete_button.pack(side="left", padx=20, pady=10)

        edit_button = ctk.CTkButton(buttons_frame, text="Editar",  font=("Arial", 16),
                                     command=self.on_edit,
                                     fg_color="#002b5b", hover_color="#0C59E1",height=40, width=80)
        edit_button.pack(side="left", padx=20, pady=10)

    def on_delete(self):
        from .messages import ConfirmacionEliminar
        from controllers.facturas_controller import delete
        
        self.attributes('-topmost' , False)

        # Si el usuario hace clic en "Sí", ejecutar la función de eliminación
        def callback(respuesta):
            if respuesta:
                delete(self.scroll,self.factura_info["ID"],self.factura_info["tipo_fact"])
                # Cerrar la ventana de la factura
                self.destroy()
                if self.facturas_section:
                    self.facturas_section.hide()
                
                # Recargar la pantalla principal después de un tiempo  # Retraso de 5 segundos
                self.facturas_section.actualizar_interfaz()
           # Crear y mostrar la ventana de confirmación
        ventana_confirmacion = ConfirmacionEliminar(self, callback)
        ventana_confirmacion.mainloop()

         



    def on_edit(self):
        from views.form_fact import form
        self.attributes('-topmost' , False)
        form(self.scroll, factura_info=self.factura_info)

    def crear_error_layout(self):
        ctk.CTkLabel(self, text="Error al obtener la información de la factura", fg_color="red").pack(pady=20)

    def reload_main_screen(self):
    # Aquí va el código para recargar la pantalla principal
        pass