import customtkinter as ctk
from  tkinter import *
from  tkinter import ttk
from tkcalendar import DateEntry
from controllers.facturas_controller import create

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class f2:
    def __init__(self):

        self.app = ctk.CTk()  # create CTk window like you do with the Tk window
        self.app.title("Crear Factura")
        self.app.geometry("1000x600") #tamaño de la ventana
        self.app.resizable(False, False) # bloqueo de redimencion de la ventana, alto y ancho
        
        # secciones
        # desplazamiento de pantalla
        self.scroll = ctk.CTkScrollableFrame(master=self.app,  fg_color="#212121", orientation="vertical", width=1000, height=600)
        self.scroll.pack(expand = True)
        # facturas
        self.invoice= ctk.CTkFrame(master=self.scroll)
        self.invoice.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")
        # cliente proveedor
        self.client= ctk.CTkFrame(master=self.scroll)
        self.client.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsw")
        # productos impuestos
        self.product = ctk.CTkFrame(master=self.scroll)



        # variables
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


        # facturas
        # self.fecha_emision_fact= StringVar()
        self.nro_fact= StringVar()
        self.data_tipo_fact=["Servicios Públicos", "Compras", "Ventas", "Impuestos"]
        self.tipo_fact= StringVar(value="")
        self.monto_fact= StringVar()
        self.imagen_fact= StringVar()


       
    #    crear widgets
        #seccion factura
        self.info_client=ctk.CTkLabel(master= self.invoice, text="Factura", font=("Arial", 18))
        self.info_client.grid(row=0, column=0,padx=20, pady=20, columnspan=2)

        self.lab_nro=ctk.CTkLabel(master= self.invoice, text="Tipo de Factura")
        self.lab_nro.grid(row=1, column=0, padx=30,pady=(10, 0) , sticky="w")
        self.combobox_fact = ctk.CTkComboBox(master= self.invoice, command=self.selection_tipo_fact, values=self.data_tipo_fact, variable=self.tipo_fact, width=150)
        self.combobox_fact.grid(row=2, column=0, padx=30,  pady=(0, 10),sticky="w")

        self.lab_tipo=ctk.CTkLabel(master= self.invoice, text="Nro de la Factura")
        self.lab_tipo.grid(row=1, column=1, padx=30, pady=(10, 0) , sticky="w")
        self.inp_tipo= ctk.CTkEntry(master= self.invoice, textvariable=self.nro_fact, width=200)
        self.inp_tipo.grid(row=2, column=1, padx=30, pady=(0, 10) , sticky="w")
                
        self.lab_date=ctk.CTkLabel(master= self.invoice, text="Fecha")
        self.lab_date.grid(row=3, column=0, padx=30,pady=(10, 0) , sticky="w")

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
        self.date_entry.grid(row=4, column=0, padx=0, pady=(0, 20))

        
        self.lab_monto=ctk.CTkLabel(master= self.invoice, text="Monto")
        self.lab_monto.grid(row=3, column=1, padx=30,pady=(10, 0) , sticky="w")
        self.inp_monto= ctk.CTkEntry(master= self.invoice, textvariable=self.monto_fact, width=200)
        self.inp_monto.grid(row=4, column=1, padx=(30, 0), pady=(0, 20) , sticky="w")

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


        self.frame_products()
       
        self.handlebutton = ctk.CTkButton(master=self.scroll,
                                            height=40,
                                            text="Guardar", 
                                            font=("Arial",16),
                                            # command=lambda: print(self.vars.keys()))
                                            command=lambda: create(self.app, self.nom_cli_pvd,
                                            self.rif_cli_pvd, self.inp_direccion_cli,
                                            self.telf_cli_pvd, self.date_entry, self.nro_fact, 
                                            self.tipo_fact, self.inp_direccion_fact,
                                            self.vars, self.contain_widgets
                                            ))
        self.handlebutton.grid(row=2, column=0, padx=10, pady=10,  columnspan=2)
        self.app.mainloop()
        
        # seccion producto
    def frame_products(self, *args):
        
        value = self.tipo_fact.get()
        if value !=  "":

            self.product.grid(row=1, column=0, padx=10, pady=(10,0), sticky="nsw", columnspan=2)

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
            self.lab_cant_pdt.configure(text="Mes(es)")
            self.add_button.configure(state=ctk.DISABLED, fg_color="#424242")

            # Borrar las filas excepto la primera
            for num in list(self.contain_widgets.keys()):
                if num != "1":  # No borrar la primera fila
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


    def clear_widgets(self):
        print(list(self.contain_widgets.keys()))
        print(list(self.vars.keys()))


f2()