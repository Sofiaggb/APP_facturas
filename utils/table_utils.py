from tkinter import *
from controllers.facturas_controller import get_factures, delete, get_fact, create, update
from views.facts_table import facts_table
from views.form_fact1 import form_fact

def utils_table(marco):

    tabla=facts_table(marco).tabla_facturas()
    formulario= form_fact(marco)
    # traer la data a la tabla
    get_factures(tabla)

    #  botones
    btnCreate = Button(marco, text="Crear", command=lambda: create(marco, formulario.descripcion_pdt, formulario.precio_pdt, tabla))
    btnCreate.grid(column=1, row=12) 

    btnDelete = Button(marco, text="Eliminar", command=lambda: delete(marco, tabla))
    btnDelete.grid(column=1, row=15)
            
    btnUpdate = Button(marco, text="Editar", command=lambda: get_fact(tabla, marco, formulario.descripcion_pdt, formulario.precio_pdt) )
    btnUpdate.grid(column=2, row=12)

    btnUpdate = Button(marco, text="Actualizar", command=lambda: update(tabla, marco, formulario.descripcion_pdt, formulario.precio_pdt) )
    btnUpdate.grid(column=2, row=13)