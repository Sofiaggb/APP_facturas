from tkinter import *
from controllers.facturas_controller  import create, get_fact
from views.facts_table import facts_table

class form_fact:
    def __init__(self, marco):
        
        # labels inputs
        self.ID= StringVar()
        # clientes proveedores
        self.rif_cli_pvd= StringVar()
        self.nom_cli_pvd= StringVar()
        self.telf_cli_pvd= StringVar()
        self.dir_cli_pvd= StringVar()

        # productos
        self.descripcion_pdt= StringVar()
        self.precio_pdt= StringVar()

        # facturas
        self.fecha_emision_fact= StringVar()
        self.nro_fact= StringVar()
        self.tipo_fact= StringVar()
        self.descripcion_fact= StringVar()
        self.imagen_fact= StringVar()

        # cantidad articulos
        self.cant_pdt= StringVar()

        self.lab_rif=Label(marco, text="Rif").grid(row=0, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.rif_cli_pvd)
        self.inp_rif.grid(column=1, row=0)

        self.lab_rif=Label(marco, text="Direccion").grid(row=1, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.dir_cli_pvd)
        self.inp_rif.grid(column=1, row=1)

        self.lab_rif=Label(marco, text="Nombre").grid(row=2, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.nom_cli_pvd)
        self.inp_rif.grid(column=1, row=2)

        self.lab_rif=Label(marco, text="Telefono").grid(row=3, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.telf_cli_pvd)
        self.inp_rif.grid(column=1, row=3)

        self.lab_rif=Label(marco, text="Nombre del Producto").grid(row=4, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.descripcion_pdt)
        self.inp_rif.grid(column=1, row=4) 

        self.lab_rif=Label(marco, text="Precio").grid(row=5, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.precio_pdt)
        self.inp_rif.grid(column=1, row=5)

        self.lab_rif=Label(marco, text="cantidad del producto").grid(row=6, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.cant_pdt)
        self.inp_rif.grid(column=1, row=6)

        self.lab_rif=Label(marco, text="fecha de emision de la factura").grid(row=7, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.fecha_emision_fact)
        self.inp_rif.grid(column=1, row=7)

        self.lab_rif=Label(marco, text="numero de la factura").grid(row=8, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.nro_fact)
        self.inp_rif.grid(column=1, row=8)

        self.lab_rif=Label(marco, text="tipo de factura").grid(row=9, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.tipo_fact)
        self.inp_rif.grid(column=1, row=9)

        self.lab_rif=Label(marco, text="descripcion de la factura").grid(row=10, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.descripcion_fact)
        self.inp_rif.grid(column=1, row=10)

        self.lab_rif=Label(marco, text="imagen").grid(row=11, column=0, padx=5, pady=5)
        self.inp_rif= Entry(marco, textvariable=self.imagen_fact)
        self.inp_rif.grid(column=1, row=11)