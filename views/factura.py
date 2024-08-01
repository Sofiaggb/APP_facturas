import customtkinter as ctk
from controllers.facturas_controller import get_factura
from views.pdf_factura import PDFGenerator
import re
class factura(ctk.CTkToplevel):
    def __init__(self,parent, id, tipo, facturas_section,data_user, is_papelera=False):
        super().__init__(parent)
        self.parent = parent  # Guarda una referencia a la ventana principal
        self.facturas_section = facturas_section
        self.is_papelera=is_papelera
        self.data_user= data_user["nivel"]
        # self.app = self
        self.attributes('-topmost' , True)
        self.title("Factura")
        self.geometry("500x600+150+0") #tamaño de la ventana
        self.resizable(False, False)
        self.scroll = ctk.CTkScrollableFrame(master=self,fg_color="#140540", width=500, height=600)
        self.scroll.pack(expand = True,  fill="x")

 # Consulta la información de la factura desde la base de datos
        self.factura_info = get_factura(id, tipo)
        if self.factura_info:
            self.crear_factura_layout(self.factura_info)
        else:
            self.crear_error_layout()

    def crear_factura_layout(self, factura_info):
        # Crear widgets para mostrar la información de la factura
        self.factura=ctk.CTkLabel(self.scroll, text="Factura", font=("Arial", 24, "bold")).pack(pady=10)

        self.nro=ctk.CTkLabel(self.scroll, text=f"Nro: {factura_info["nro_fact"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        self.fecha=ctk.CTkLabel(self.scroll, text=f"Fecha de Emisión: {factura_info["fecha_emision_fact"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        self.tipo=ctk.CTkLabel(self.scroll, text=f"Tipo: {factura_info["tipo_fact"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        self.descripcion=ctk.CTkLabel(self.scroll, text=f"Motivo: {factura_info["descripción_fact"]}",  wraplength=420, font=("Arial", 16)).pack(anchor="w", padx=20)

        
        self.cliente=ctk.CTkLabel(self.scroll, text="Cliente/Proveedor:", font=("Arial", 18, "bold")).pack(anchor="w", pady=(10, 0), padx=20)
        self.nombre=ctk.CTkLabel(self.scroll, text=f"Nombre: {factura_info["cliente"]["nombre"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        self.rif=ctk.CTkLabel(self.scroll, text=f"RIF/CI: {factura_info["cliente"]["rif"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        # Mostrar el campo "Teléfono" solo si no está vacío
        if factura_info['cliente']['telefono']:
            self.telefono=ctk.CTkLabel(self.scroll, text=f"Teléfono: {factura_info["cliente"]["telefono"]}", font=("Arial", 16)).pack(anchor="w", padx=20)
        self.direccion=ctk.CTkLabel(self.scroll, text=f"Dirección: {self.clean_text(factura_info["cliente"]["dirección"])}", font=("Arial", 16)).pack(anchor="w", padx=20)
        

        if factura_info["tipo_fact"] in ["Servicios Públicos",  "Impuestos"]:
            self.factipo=ctk.CTkLabel(self.scroll, text=factura_info["tipo_fact"], font=("Arial", 18, "bold")).pack(anchor="center", pady=(5, 0), padx=20)
           # Crear un frame para la tabla de productos
            table_frame = ctk.CTkFrame(self.scroll, bg_color="transparent", fg_color="transparent", height=50)
            table_frame.pack(pady=5, padx=20, fill="both", expand=True)

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
            self.factipo=ctk.CTkLabel(self.scroll, text="Productos", font=("Arial", 18, "bold")).pack(anchor="center", pady=(10, 0), padx=20)
            
            # Crear un frame para la tabla de productos
            table_frame = ctk.CTkScrollableFrame(self.scroll, bg_color="transparent", fg_color="transparent")
            table_frame.pack(pady=5, padx=20, fill="both", expand=True)

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
        montos_frame.pack(anchor="e", padx=30, pady=(10,0))
        if factura_info["tipo_fact"] in ["Compras",  "Ventas"]:
            ctk.CTkLabel(montos_frame, text=f"Monto Neto: {factura_info["monto_neto"]}", font=("Arial", 16), anchor="w", justify="left").pack(pady=0, padx=5, anchor="w")
            ctk.CTkLabel(montos_frame, text=f"IVA: {factura_info["IVA"]}", font=("Arial", 16), anchor="w", justify="left").pack(pady=0, padx=5, anchor="w")
        ctk.CTkLabel(montos_frame, text=f"Monto Total: {factura_info["monto_total"]}", font=("Arial", 16), anchor="w", justify="left").pack(pady=0, padx=5, anchor="w")

         # Agregar los botones Eliminar y Editar al final
        buttons_frame = ctk.CTkFrame(self.scroll, bg_color="transparent", fg_color="transparent")
        buttons_frame.pack(anchor="center", padx=20, pady=(0,10))

        if self.is_papelera:
            delete_button = ctk.CTkButton(buttons_frame, text="Eliminar",  font=("Arial", 16),
                                                command=self.on_delete,
                                                fg_color="#9B0202", hover_color="#DC0F0F",height=40, width=80)
            delete_button.pack(side="left", padx=20, pady=10)
            edit_button = ctk.CTkButton(buttons_frame, text="Recuperar",  font=("Arial", 16),
                                                command=self.on_recover,
                                                fg_color="#9F9011",text_color="#000", hover_color="#DAC40B",height=40, width=90)
            edit_button.pack(side="left", padx=20, pady=10)
        else:
            
            delete_button = ctk.CTkButton(buttons_frame, text="Eliminar",  font=("Arial", 16),
                                                command=self.on_papelera,
                                                fg_color="#9B0202", hover_color="#DC0F0F",height=40, width=80)
            delete_button.pack(side="left", padx=20, pady=10)

            edit_button = ctk.CTkButton(buttons_frame, text="Editar",  font=("Arial", 16),
                                                command=self.on_edit,
                                                fg_color="#002b5b", hover_color="#0C59E1",height=40, width=80)
            edit_button.pack(side="left", padx=20, pady=10)


            self.button = ctk.CTkButton(buttons_frame, text="Generar PDF", height=40,
                                         font=("Arial", 16), command=self.on_generate_pdf)
            self.button.pack(side="left",pady=20)

    def on_generate_pdf(self):
        from views.messages import LoadingPopup
                
        self.attributes('-topmost' , False)
        # Crear la ventana emergente
        self.loading_popup = LoadingPopup(self)
        
        # Iniciar la generación del PDF
        self.pdf_generator = PDFGenerator(self.factura_info, self.update_progress)
        self.pdf_generator.start_pdf_generation()
    
    def update_progress(self, progress):
        from views.messages import VentanaMensaje
        self.loading_popup.progress_bar.set(progress)
        if progress >= 1.0:
            print(progress)
            self.loading_popup.destroy()
            VentanaMensaje(self, "Confirmación", "¡Éxito! El PDF de tu factura ha sido generado correctamente, se encuentra en tu carpeta de descargas")


    def clean_text(self,text):
        # Eliminar caracteres no imprimibles
        return re.sub(r'[^\x20-\x7E]', '', text)
       
    def on_papelera(self):
        from .messages import ConfirmacionEliminar
        from controllers.facturas_controller import papelera
        
        self.attributes('-topmost' , False)

        # Si el usuario hace clic en "Sí", ejecutar la función de eliminación
        def callback(respuesta):
            if respuesta:
                papelera(self.parent,self.factura_info["ID"])
                
                # Cerrar la ventana de la factura
                self.destroy()
                if self.facturas_section:
                    self.facturas_section.hide()
                
                # Recargar la pantalla principal después de un tiempo  # Retraso de 5 segundos
                self.facturas_section.actualizar_interfaz()
           # Crear y mostrar la ventana de confirmación
        ventana_confirmacion = ConfirmacionEliminar(self, callback, "¿Estás seguro de querer eliminar la factura?")
        ventana_confirmacion.mainloop()

    def on_delete(self):
        from .messages import ConfirmacionEliminar
        from controllers.facturas_controller import  delete
        
        self.attributes('-topmost' , False)

        # Si el usuario hace clic en "Sí", ejecutar la función de eliminación
        def callback(respuesta):
            if respuesta:
                delete(self.parent,self.factura_info["ID"],self.factura_info["tipo_fact"])
                # Cerrar la ventana de la factura
                self.destroy()
                if self.facturas_section:
                    self.facturas_section.hide()
                
                # Recargar la pantalla principal después de un tiempo  # Retraso de 5 segundos
                self.facturas_section.actualizar_interfaz()
           # Crear y mostrar la ventana de confirmación
        ventana_confirmacion = ConfirmacionEliminar(self, callback, "¿Estás seguro de querer eliminar la factura definitivamente?")
        ventana_confirmacion.mainloop()         



    def on_edit(self):
        from views.form_fact import form
        self.attributes('-topmost' , False)
        form(self.scroll, factura_info=self.factura_info, 
             facturas_section=self.facturas_section, ventana_fact=self,
             parent_fact=self.parent)


    def on_recover(self):
        from .messages import ConfirmacionEliminar
        from controllers.facturas_controller import  recuperar
        
        self.attributes('-topmost' , False)

        # Si el usuario hace clic en "Sí", ejecutar la función de eliminación
        def callback(respuesta):
            if respuesta:
                recuperar(self.parent,self.factura_info["ID"])
                # Cerrar la ventana de la factura
                self.destroy()
                if self.facturas_section:
                    self.facturas_section.hide()
                
                # Recargar la pantalla principal después de un tiempo  # Retraso de 5 segundos
                self.facturas_section.actualizar_interfaz()
           # Crear y mostrar la ventana de confirmación
        ventana_confirmacion = ConfirmacionEliminar(self, callback, "¿Estás seguro de querer recuperar esta factura?")
        ventana_confirmacion.mainloop()  

    def crear_error_layout(self):
        ctk.CTkLabel(self, text="Error al obtener la información de la factura", fg_color="red").pack(pady=20)
