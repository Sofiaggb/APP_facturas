from tkinter import *
from tkinter import ttk

class facts_table:
    def __init__(self, marco):
        self.tb_facturas=ttk.Treeview(marco)
        self.tb_facturas.grid(column=0, row=14, columnspan=4)
        self.tb_facturas["columns"]=["ID","nro_fact", "fecha_emision_fact", "descripcion_fact","tipo_fact", "nom_cli_pvd", "rif_cli_pvd","telf_cli_pvd", "dir_cli_pvd", "descripcion_pdt", "precio_pdt", "cant_pdt"]
        self.tb_facturas.column("#0", width=0)
        self.tb_facturas.column("ID", width=50, anchor="center")
        self.tb_facturas.column("nro_fact", width=100, anchor="center")
        self.tb_facturas.column("fecha_emision_fact", width=100, anchor="center")
        self.tb_facturas.column("descripcion_fact", width=100, anchor="center")
        self.tb_facturas.column("tipo_fact", width=100, anchor="center")
        self.tb_facturas.column("nom_cli_pvd", width=100, anchor="center")
        self.tb_facturas.column("rif_cli_pvd", width=100, anchor="center")
        self.tb_facturas.column("telf_cli_pvd", width=100, anchor="center")
        self.tb_facturas.column("dir_cli_pvd", width=100, anchor="center")
        self.tb_facturas.column("descripcion_pdt", width=100, anchor="center")
        self.tb_facturas.column("precio_pdt", width=100, anchor="center")
        self.tb_facturas.column("cant_pdt", width=100, anchor="center")
        self.tb_facturas.heading("#0", text="")
        self.tb_facturas.heading("ID", text="ID", anchor="center")
        self.tb_facturas.heading("nro_fact", text="nro factura", anchor="center")
        self.tb_facturas.heading("fecha_emision_fact", text="fecha de emicion factura", anchor="center")
        self.tb_facturas.heading("descripcion_fact", text="descripcion factura", anchor="center")
        self.tb_facturas.heading("tipo_fact", text="tipo factura", anchor="center")
        self.tb_facturas.heading("nom_cli_pvd", text="nombre cliente-proveedor", anchor="center")
        self.tb_facturas.heading("rif_cli_pvd", text="rif cliente-proveedor", anchor="center")
        self.tb_facturas.heading("telf_cli_pvd", text="telefono cliente-proveedor", anchor="center")
        self.tb_facturas.heading("dir_cli_pvd", text="direccion cliente-proveedor", anchor="center")
        self.tb_facturas.heading("descripcion_pdt", text="nomre producto", anchor="center")
        self.tb_facturas.heading("precio_pdt", text="precio producto", anchor="center")
        self.tb_facturas.heading("cant_pdt", text="cantidad producto", anchor="center")
    
    def tabla_facturas(self):
        return self.tb_facturas







    

