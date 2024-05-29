import customtkinter as ctk
from  tkinter import *
from  tkinter import ttk
from tkcalendar import DateEntry
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.meses import meses
from controllers.facturas_controller import create, update


class form(ctk.CTkToplevel):
    def __init__(self, parent, factura_info=None):
        super().__init__(parent)
        self.app = self
        # self.app.attributes('-topmost' , True)
        self.app.title("Crear Factura")
        self.app.geometry("1030x700+150+0") #tamaño de la ventana
        self.app.resizable(False, False) # bloqueo de redimencion de la ventana, alto y ancho
       
        # secciones
        # desplazamiento de pantalla
        self.scroll = ctk.CTkScrollableFrame(master=self.app,  fg_color="#212121",
                                             orientation="vertical", width=1030, height=700)
        self.scroll.pack(expand = True)
        # facturas
        self.invoice= ctk.CTkFrame(master=self.scroll)
        self.invoice.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        # cliente proveedor
        self.client= ctk.CTkFrame(master=self.scroll)
        self.client.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsw")
        # contenedor productos impuestos y montos
        self.contenedor_products = ctk.CTkFrame(master=self.scroll)
        # productos impuestos
        self.product= ctk.CTkFrame(master=self.contenedor_products, fg_color="transparent")
         # montos 
        self.montos= ctk.CTkFrame(master=self.contenedor_products, fg_color="transparent")
        


        # variables
        # Factura existente
        self.factura_info = factura_info
        
        # clientes proveedores
        self.rif_cli_pvd= StringVar()
        self.nom_cli_pvd= StringVar()
        self.telf_cli_pvd= StringVar()

        # productos
        self.descripcion_pdt= StringVar()
        self.precio_pdt= StringVar()
        # cantidad articulos
        self.cant_pdt= StringVar()
        self.contain_widgets = {}  # diccionario para almacenar los widgets creados dinámicamente
        self.vars={   # diccionario para almacenar las variables creados dinámicamente
                1: {
                    "descripcion":self.descripcion_pdt, 
                    "precio":self.precio_pdt,
                    "cantidad":self.cant_pdt
                }
            }   
        self.ids_pdts=[] 
        
        # montos
        
        self.iva_fact= StringVar()
        self.monto_total= DoubleVar()
        self.monto_neto= DoubleVar()

        # facturas
        self.nro_fact= StringVar()
        self.data_tipo_fact=["Servicios Públicos", "Compras", "Ventas", "Impuestos"]
        self.tipo_fact= StringVar(value="")
        self.imagen_fact= StringVar()


       
    #    crear widgets
        #seccion factura
        self.info_client=ctk.CTkLabel(master= self.invoice, text="Factura", font=("Arial", 18))
        self.info_client.grid(row=0, column=0,padx=20, pady=20, columnspan=2)

        self.lab_nro=ctk.CTkLabel(master= self.invoice, text="Tipo de Factura")
        self.lab_nro.grid(row=1, column=0, padx=30,pady=(10, 0) , sticky="w")
        self.combobox_fact = ctk.CTkOptionMenu(master= self.invoice, command=self.selection_tipo_fact, values=self.data_tipo_fact, variable=self.tipo_fact,
                                                width=150)
                                                # fg_color="#424242",button_color="#2D2863",
                                                #   dropdown_hover_color="#2D2863")
        self.combobox_fact.grid(row=2, column=0, padx=(30,0),  pady=(0, 10),sticky="w")

        self.lab_tipo=ctk.CTkLabel(master= self.invoice, text="Nro de la Factura")
        self.lab_tipo.grid(row=1, column=1, padx=(20, 0), pady=(10, 0) , sticky="w")
        self.inp_tipo= ctk.CTkEntry(master= self.invoice, textvariable=self.nro_fact, width=200)
        self.inp_tipo.grid(row=2, column=1, padx=20, pady=(0, 10) , sticky="w")
                
        self.lab_date=ctk.CTkLabel(master= self.invoice, text="Fecha")
        self.lab_date.grid(row=3, column=0, padx=(30,0),pady=(10, 0) , sticky="w")

        # Crear un estilo personalizado para el DateEntry
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('my.DateEntry',
                fieldbackground='#343434',
                background='#343434',
                foreground='white',
                arrowcolor='white',
                bordercolor='#343434',
                hoverbackground='blue')
        self.date_entry = DateEntry(master= self.invoice, width=20,date_pattern='dd/MM/yyyy',style='my.DateEntry', selected_fg='darkblue')
        self.date_entry.grid(row=4, column=0, padx=(20, 10), pady=(0, 20))

        self.lab_direccion=ctk.CTkLabel(master= self.invoice, text="Descripcion o Motivo")
        self.lab_direccion.grid(row=5, column=0, padx=30, sticky="w")
        self.inp_direccion_fact= ctk.CTkTextbox(master= self.invoice, height=80, width=430)
        self.inp_direccion_fact.grid(row=6, column=0, padx=30, pady=(0, 20), sticky="w", columnspan=2)
        



        # seccion cliente
        self.info_client=ctk.CTkLabel(master= self.client, text="Datos", font=("Arial", 18))
        self.info_client.grid(row=0, column=0,padx=20, pady=(20, 0), columnspan=2)

        self.lab_rif=ctk.CTkLabel(master= self.client, text="R.I.F. / C.I.")
        self.lab_rif.grid(row=1, column=0, padx=30,pady=(10, 0) , sticky="w")
        self.inp_rif= ctk.CTkEntry(master= self.client, textvariable=self.rif_cli_pvd, width=200)
        self.inp_rif.grid(row=2, column=0, padx=30, pady=(0, 10) , sticky="w")
        
        self.lab_nom=ctk.CTkLabel(master= self.client, text="Nombre del Cliente, Proveedor o Servicios")
        self.lab_nom.grid(row=3, column=0, padx=30, pady=(10, 0) , sticky="w")
        self.inp_nom= ctk.CTkEntry(master= self.client, textvariable=self.nom_cli_pvd, width=400)
        self.inp_nom.grid(row=4, column=0, padx=30, pady=(0, 10) , columnspan=2, sticky="w")

        self.lab_telf=ctk.CTkLabel(master= self.client, text="Telefono")
        self.lab_telf.grid(row=5, column=0, padx=30, pady=(10, 0) , sticky="w")
        self.inp_telf= ctk.CTkEntry(master= self.client, textvariable=self.telf_cli_pvd, width=200)
        self.inp_telf.grid(row=6, column=0, padx=30, pady=(0, 10) , sticky="w")

        self.lab_direccion=ctk.CTkLabel(master= self.client, text="Direccion")
        self.lab_direccion.grid(row=7, column=0, padx=30, sticky="w")
        self.inp_direccion_cli= ctk.CTkTextbox(master= self.client, height=60, width=400)
        self.inp_direccion_cli.grid(row=8, column=0, padx=30, pady=(0, 20), sticky="w", columnspan=2)
       
        self.tipo_fact.trace_add("write", self.frame_products)

             # Vincular trace a las variables
        self.precio_pdt.trace_add('write', self.update_montos)
        self.cant_pdt.trace_add('write', self.update_montos)
        self.iva_fact.trace_add('write', self.update_montos)

        self.frame_products()

        if self.factura_info:
            self.load_factura_info()

        self.handlebutton = ctk.CTkButton(master=self.scroll,
                                            height=40,
                                            text="Guardar", 
                                            font=("Arial",16),
                                            fg_color="#2D2863",
                                            command= lambda: self.save_factura(self.app,  self.nom_cli_pvd,
                                            self.rif_cli_pvd, self.inp_direccion_cli,
                                            self.telf_cli_pvd, self.date_entry, self.nro_fact, 
                                            self.tipo_fact,  self.iva_fact, self.inp_direccion_fact,
                                            self.vars, self.contain_widgets, 
                                            self.monto_neto, self.monto_total
                                            ))
        self.handlebutton.grid(row=2, column=0, padx=10, pady=10,  columnspan=2)
        self.grab_set()
       
    def save_factura(self, app, nom_cli_pvd, rif_cli_pvd, inp_direccion_cli, telf_cli_pvd,
                      date_entry, nro_fact, tipo_fact, iva_fact, inp_direccion_fact, 
                      vars, contain_widgets, monto_neto, monto_total):
        # Verificar si es una nueva factura o una edición
        if self.factura_info:
            if self.factura_info["tipo_fact"] in ["Servicios Públicos", "Impuestos"]:
                id_imp_pdt = self.factura_info["ID_serv_impto"] 
            else:
                id_imp_pdt=self.ids_pdts
            # Actualizar factura existente
            # print(id_imp_pdt)
            update( app, self.factura_info["ID"], self.factura_info["id_cp"], id_imp_pdt, nom_cli_pvd, rif_cli_pvd, inp_direccion_cli, telf_cli_pvd, date_entry, nro_fact, tipo_fact, iva_fact, inp_direccion_fact, vars, contain_widgets, monto_neto, monto_total)
        else:
            # Crear nueva factura
            create( app,nom_cli_pvd, rif_cli_pvd, inp_direccion_cli, telf_cli_pvd, date_entry, nro_fact, tipo_fact, iva_fact, inp_direccion_fact, vars, contain_widgets, monto_neto, monto_total)

        # seccion producto
    def frame_products(self, *args):
        
        value = self.tipo_fact.get()

        if value !=  "":

            self.contenedor_products.grid(row=1, column=0, padx=10, pady=(10,0), sticky="nsw", columnspan=2)
            self.product.grid(row=0, column=0, padx=0, pady=0, sticky="nsw")
            self.montos.grid(row=1, column=0, padx=0, pady=0, sticky="e")


            self.info_product=ctk.CTkLabel(master= self.product,text="", font=("Arial", 18), width=400)
            self.info_product.grid(row=0, column=0,padx=20, pady=(20, 0), columnspan=6)

            self.lab_nom_pdt=ctk.CTkLabel(master= self.product, text="", width=150)
            self.lab_nom_pdt.grid(row=1, column=0, padx=30,pady=(10, 0) , sticky="w")
            self.inp_nom_pdt= ctk.CTkEntry(master= self.product, textvariable=self.descripcion_pdt, width=430)
            self.inp_nom_pdt.grid(row=2, column=0, padx=30, pady=(0, 30) , sticky="w", columnspan=2)

            self.lab_precio_pdt=ctk.CTkLabel(master= self.product, text="", width=70)
            self.lab_precio_pdt.grid(row=1, column=3, padx=10,pady=(10, 0) , sticky="w")
            self.inp_precio_pdt= ctk.CTkEntry(master= self.product, textvariable=self.precio_pdt)
            self.inp_precio_pdt.grid(row=2, column=3, padx=10, pady=(0, 30) , sticky="w")


            self.lab_cant_pdt=ctk.CTkLabel(master= self.product, text="", width=70)
            self.lab_cant_pdt.grid(row=1, column=4, padx=30,pady=(10, 0) , sticky="w")

            if value in ["Servicios Públicos", "Impuestos"]:
                self.inp_meses= ctk.CTkOptionMenu(master= self.product, values= meses, variable=self.cant_pdt)
                self.inp_meses.grid(row=2, column=4, padx=30, pady=(0, 30) , sticky="w")
            else:
                self.inp_cant_pdt= ctk.CTkEntry(master= self.product, textvariable=self.cant_pdt)
                self.inp_cant_pdt.grid(row=2, column=4, padx=30, pady=(0, 30) , sticky="w")

            self.widgets={ 
                "1": {
                        "input_name": ctk.CTkEntry(master=self.product, textvariable=self.descripcion_pdt, width=430),
                        "input_precio": ctk.CTkEntry(master=self.product, textvariable=self.precio_pdt, width=100),
                        "input_cantidad": ctk.CTkEntry(master=self.product, textvariable=self.cant_pdt, width=100)
                    }
                        }     
       
            self.num=1
            
            # self.contain_widgets[self.num]=self.widgets

            self.add_button = ctk.CTkButton(master= self.product, text="+", width=40, height=40, font=("Arial",20), command=self.duplicate)
            self.add_button.grid(row=1, column=5, padx=30, pady=(0, 30), rowspan=2, sticky="s")


            # montos de la factura
            self.lab_monto_neto=ctk.CTkLabel(master= self.montos, text="Monto Neto")
            self.lab_monto_neto.grid(row=0, column=0, padx=20,pady=(10, 0) , sticky="w")
            self.inp_monto_neto= ctk.CTkEntry(master= self.montos, textvariable=self.monto_neto, width=130, state=DISABLED)
            self.inp_monto_neto.grid(row=1, column=0, padx=20, pady=(0, 20) , sticky="w")

            self.lab_iva=ctk.CTkLabel(master= self.montos, text="Monto del IVA")
            self.lab_iva.grid(row=0, column=1, padx=20,pady=(10, 0) , sticky="w")
            self.inp_iva= ctk.CTkEntry(master= self.montos, textvariable=self.iva_fact, width=130)
            self.inp_iva.grid(row=1, column=1, padx=20, pady=(0, 20) , sticky="w")

            self.lab_monto_total=ctk.CTkLabel(master= self.montos, text="Monto Total")
            self.lab_monto_total.grid(row=0, column=2, padx=20,pady=(10, 0) , sticky="w")
            self.inp_monto_total= ctk.CTkEntry(master= self.montos, textvariable=self.monto_total, width=130, state=DISABLED)
            self.inp_monto_total.grid(row=1, column=2, padx=20, pady=(0, 20) , sticky="w")
           

    def update_montos(self, *args):
        try:
            tipo_factura = self.tipo_fact.get()
        
            # Compras y Ventas
            if tipo_factura in ["Compras", "Ventas"]:
                try:
                   # Inicializar monto total
                    monto_neto_total = 0
                    for num, vars in self.vars.items():
                        precio = float(vars["precio"].get()) if vars["precio"].get() else 0
                        cantidad = float(vars["cantidad"].get()) if vars["cantidad"].get() else 0
                        # Calcular el monto neto y agregarlo al monto neto total
                        monto_neto = precio * cantidad
                        monto_neto_total += monto_neto

                    iva = float(self.iva_fact.get()) if self.iva_fact.get() else 0

                    self.monto_neto.set(monto_neto_total)

                    monto_total = monto_neto_total + iva
                    self.monto_total.set(monto_total)

                except ValueError:
                    # Manejar el caso en que la entrada no sea un número
                    self.monto_neto.set(0)
                    self.monto_total.set(0)

            # Servicios Públicos e Impuestos
            elif tipo_factura in ["Servicios Públicos", "Impuestos"]:
                if self.precio_pdt.get() and self.iva_fact.get():
                    precio = float(self.precio_pdt.get())
                    iva = float(self.iva_fact.get())

                    self.monto_neto.set(precio)

                    monto_total = precio + iva
                    self.monto_total.set(monto_total)
                else:
                    self.monto_neto.set(0)
                    self.monto_total.set(0)

        except Exception as e:
            print(f"Error al actualizar montos: {e}")


    def duplicate(self):  #crear un nuevo campo para agregar un producto
        # Incrementar los contadores de fila
        self.num_row1=2
        self.num += 1
          # Crear un diccionario para almacenar las variables de esta fila
        row_vars = {
            "descripcion": StringVar(),
            "precio": StringVar(),
            "cantidad": StringVar()
             }

        # Vincular el método update_montos a las nuevas variables
        row_vars["precio"].trace_add('write', self.update_montos)
        row_vars["cantidad"].trace_add('write', self.update_montos)

         # Clonar los widgets existentes y agregarlos al diccionario
        cloned_widgets = {}
        # Clonar y colocar el widget "input_name"
        cloned_widgets["input_name"] = ctk.CTkEntry(master=self.product, textvariable=row_vars["descripcion"], width=430)
        
        # Clonar y colocar el widget "input_precio"
        cloned_widgets["input_precio"] = ctk.CTkEntry(master=self.product, textvariable=row_vars["precio"])

        # Clonar y colocar el widget "input_cantidad"
        cloned_widgets["input_cantidad"] = ctk.CTkEntry(master=self.product, textvariable=row_vars["cantidad"])
       
        cloned_widgets["button_delete"] = ctk.CTkButton(master=self.product, 
                                               text="Eliminar", 
                                               fg_color="#981111", 
                                               hover_color="#D50C0C", 
                                               width=10,)
        # Agregar los widgets clonados al diccionario
        self.contain_widgets[self.num] = cloned_widgets
         # Almacenar el diccionario de variables en una lista para acceder a ellas más tarde
        self.vars[self.num] = row_vars
        
        for key, item in self.contain_widgets.items():
            self.num_row1 += 1

            item["input_name"].grid(row=self.num_row1, column=0, padx=30, pady=(0, 30), sticky="w", columnspan=2)
            item["input_precio"].grid(row=self.num_row1, column=3, padx=10, pady=(0, 30), sticky="w")
            item["input_cantidad"].grid(row=self.num_row1, column=4, padx=30, pady=(0, 30), sticky="w")
            item["button_delete"].configure(command=lambda key=key: self.delete_row(key))
            item["button_delete"].grid(row=self.num_row1, column=5, padx=30, pady=(0, 30), sticky="s")

    #    Actualizar la interfaz de usuario y luego desplazar la vista
        self.scroll.update_idletasks() #actualizamos la interfaz grafica
        self.scroll.after(100, lambda: self.scroll._parent_canvas.yview_moveto(1.0)) # con la funcion after despues de 100 milisegundos scroleamos (bajamos) la pantalla

    
    def delete_row(self, key):
        print(key)

    # Check if the key exists in the dictionary
        if key in self.contain_widgets:
            # Get the item associated with the key
            item = self.contain_widgets[key]
            # Destroy the associated widgets
            item["input_name"].destroy()
            item["input_precio"].destroy()
            item["input_cantidad"].destroy()
            item["button_delete"].destroy()

        # Remove the item from the dictionary
        self.contain_widgets.pop(key)

        # Verificar si la clave existe en el diccionario de variables
        if key in self.vars:
            # Eliminar el diccionario de variables asociado con la clave
            self.vars.pop(key)
        # Actualizacion inmediata de la interfaz de usuario
        self.scroll.update()


    def selection_tipo_fact(self, value):

        # Verificar si la opción seleccionada es "Servicios Públicos" o "Impuestos"
        if value in ["Servicios Públicos", "Impuestos"]:
            # Configurar los textos de los campos
            self.info_product.configure(text=value)
            self.lab_nom_pdt.configure(text="Nombre del Servicio" if value == "Servicios Públicos" else "Nombre del Impuesto")
            self.lab_precio_pdt.configure(text="Monto")
            self.lab_cant_pdt.configure(text="Mes")
            self.add_button.configure(state=ctk.DISABLED, fg_color="#424242")
            # Deshabilitar el campo de entrada
            self.inp_iva.configure(state=ctk.DISABLED)
            # Establecer un valor por defecto, por ejemplo '0.00'
            self.iva_fact.set('0.00')

            # Borrar las filas excepto la primera
            for num in list(self.contain_widgets.keys()):
                if num != 1:  # No borrar la primera fila
                    for widget in self.contain_widgets[num].values():
                        widget.destroy()
                    del self.contain_widgets[num]
                    del self.vars[num]

            # Restablecer el contador a 1
            # self.num = 1

        else:

            self.info_product.configure(text="Productos")
            # Mostrar el botón y campos
            self.lab_nom_pdt.configure(text="Nombre del Producto")
            self.lab_precio_pdt.configure(text="Precio c/u")
            self.lab_cant_pdt.configure(text="Cantidad")
            self.add_button.configure(state=ctk.NORMAL, fg_color="#0277BD")
            # habilitar el campo de entrada
            self.inp_iva.configure(state=ctk.NORMAL)
            self.iva_fact.set('')

    def load_factura_info(self):
        # Cargar la información de la factura en los campos del formulario
        self.nro_fact.set(self.factura_info["nro_fact"])
        self.tipo_fact.set(self.factura_info["tipo_fact"])
        self.selection_tipo_fact(self.tipo_fact.get())
        self.rif_cli_pvd.set(self.factura_info["cliente"]["rif"])
        self.nom_cli_pvd.set(self.factura_info["cliente"]["nombre"])
        self.telf_cli_pvd.set(self.factura_info["cliente"]["teléfono"])
        self.inp_direccion_cli.insert("1.0", self.factura_info["cliente"]["dirección"])
        self.inp_direccion_fact.insert("1.0", self.factura_info["descripción_fact"])
        self.date_entry.set_date(self.factura_info["fecha_emision_fact"])
        self.iva_fact.set(self.factura_info["IVA"])
        self.monto_neto.set(self.factura_info["monto_neto"])
        self.monto_total.set(self.factura_info["monto_total"])

        if self.factura_info["tipo_fact"] in ["Servicios Públicos", "Impuestos"]:
            for index, item in enumerate(self.factura_info["servicios_impuestos"]):
                self.vars[1]["descripcion"].set(item["descripcion_serv_impto"])
                self.vars[1]["precio"].set(item["monto_serv_impto"])
                self.vars[1]["cantidad"].set(item["meses_serv_impto"])
        
        else: 
            # Productos o servicios
            for i, producto in enumerate(self.factura_info["productos"]):
                if i > 0:
                    self.duplicate()
                self.ids_pdts.append(producto["ID_pdt"])
                self.vars[i+1]["descripcion"].set(producto["descripción_pdt"])
                self.vars[i+1]["precio"].set(producto["precio_pdt"])
                self.vars[i+1]["cantidad"].set(producto["cantidad_pdt"])

