from tkinter import END
from connection import connection_bd # database
from views.messages import  messaje # mensages

db = connection_bd()

def clear(descripcion_pdt, precio_pdt):
    descripcion_pdt.set("")
    precio_pdt.set("")

def get_fact(tabla, marco, descripcion_pdt, precio_pdt):
    # print(tabla.selection()) 
    if tabla.selection():
        id= tabla.selection()[0]
        sql = "SELECT * FROM productos WHERE ID_pdt = %s"
        db.cursor.execute(sql, (id,))
        registro = db.cursor.fetchone()
        descripcion_pdt.set(registro[1])
        precio_pdt.set(registro[2])

        print(registro)
        # return registro
    else:
        # descripcion_pdt.set("sin valor")
        print("sin valor")

    

def get_factures(tabla):
    # vaciar tabla
    tabla.delete(*tabla.get_children())
    # seleccionar los elemtos y devolverlos
    sql="select * from productos"
    db.cursor.execute(sql)
    filas= db.cursor.fetchall()
    for fila in filas:
        id= fila[0]
        tabla.insert("", END, id, text=id, values=fila)


def create(marco, descripcion_pdt, precio_pdt, tabla):
    # formulario de modificar factura
    update= False
    if update==False:
        # Obtener los valores de los campos
        descripcion = descripcion_pdt.get()
        precio = precio_pdt.get()

        # Verificar si ambos campos tienen valores
        if not (descripcion and precio):
            messaje(marco, "Por favor, completa todos los campos", "red")
            return
        
        # si no se cumple se agrga el registro
        val= descripcion_pdt.get(), precio_pdt.get()
        sql="insert INTO productos (pdt_descripcion, pdt_precio) values(%s, %s)"
        db.cursor.execute(sql, val)
        db.connection.commit()
        messaje(marco, "se ha guardado el registro correctamente", "green")
        get_factures(tabla)
        clear(descripcion_pdt, precio_pdt)

def update(tabla, marco,  descripcion_pdt, precio_pdt):
        # formulario de modificar factura
    update= False
    if update==False:
        # Obtener los valores de los campos
        descripcion = descripcion_pdt.get()
        precio = precio_pdt.get()

        # Verificar si ambos campos tienen valores
        if not (descripcion and precio):
            messaje(marco, "Por favor, completa todos los campos", "red")
            return
        
        # si no se cumple se agrga el registro
        id= tabla.selection()[0]
        val= descripcion_pdt.get(), precio_pdt.get()
        sql="UPDATE productos SET pdt_descripcion =%s, pdt_precio=%s WHERE ID_pdt = "+id
        db.cursor.execute(sql, val)
        db.connection.commit()
        messaje(marco, "se ha actualizado el registro correctamente", "green")
        get_factures(tabla)
        clear(descripcion_pdt, precio_pdt)

def delete(marco, tabla):
    print(tabla.selection())

    if tabla.selection():
        id= tabla.selection()[0]
        sql="DELETE FROM productos WHERE ID_pdt=%s"
        db.cursor.execute(sql, (id,))
        db.connection.commit()
        tabla.delete(id)
        messaje(marco, "se ha eliminado el registro correctamente", "green")
    else:
        messaje(marco, "selecciona un registro para eliminar", "red")