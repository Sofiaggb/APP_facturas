from tkinter import END
from datetime import date
from connection import connection_bd # database
from views.messages import  VentanaMensaje # mensages
from controllers.auth_invoice import validar_rif, validar_telefono, validar_fecha, num_positivo

db = connection_bd()

def clear(nombre_cli_pvd, rif_cli_pvd, direccion_cli_pvd, telefono_cli_pvd, 
           fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars, widgets):
    # limpiar todos los campos
    nombre_cli_pvd.set("")
    rif_cli_pvd.set("")
    direccion_cli_pvd.delete("0.0", "end")  
    telefono_cli_pvd.set("")
    fecha_emision.set_date(date.today())
    nro_fact.set("")
    tipo_fact.set("")
    iva_fact.set("")
    descripcion_fact.delete("0.0", "end")  

     # Borrar todos los widgets y variables excepto los de la primera fila
    for num in list(vars.keys()):
        if num != 1:  # Asegurarse de no borrar la primera fila
            for widget in widgets[num].values():
                widget.destroy()  # Destruir el widget
            del widgets[num]  # Eliminar la entrada del diccionario de widgets
            del vars[num]  # Eliminar la entrada del diccionario de variables
        else:  # Si es la primera fila, dejar los valores en blanco
            for var in vars[num].values():
                var.set("")  # Dejar los valores en blanco


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


def create(app, nombre_cli_pvd, rif_cli_pvd, direccion_cli_pvd, telefono_cli_pvd, 
           fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars, widgets):
    try:
        # validaciones 
        if not tipo_fact.get().strip():
           return VentanaMensaje(app, "Error", "El tipo de la factura es obligatorio.")
       
        if not nro_fact.get().strip():
           return VentanaMensaje(app, "Error", "El número de la factura es obligatorio.")

        if not validar_fecha(fecha_emision.get_date()):
            return VentanaMensaje(app, "Error", "La fecha es invalida.  Verifica que la fecha no sea futura o no tenga más de 15 años de antigüedad")

        if not iva_fact.get().strip():
           return VentanaMensaje(app, "Error", "El IVA de la factura es obligatorio.")

        if tipo_fact.get()== "Compras" or tipo_fact.get()=="Ventas":
            if not num_positivo(iva_fact.get()):
                return VentanaMensaje(app, "Error", "El monto del IVA debe ser un valor positivo. Por favor, ingresa un valor válido.")

        if not descripcion_fact.get("0.0", "end").strip():
           return VentanaMensaje(app, "Error", "La descripción de la factura es obligatoria.")
        
        if not rif_cli_pvd.get().strip():
           return VentanaMensaje(app, "Error", "El RIF del cliente/proveedor es obligatorio.")
        
        if not validar_rif(rif_cli_pvd.get()):
             return VentanaMensaje(app, "Error", "El RIF del cliente/proveedor es inválido, El formato es una letra (V, E, J, G), seguida de una linea (-) y 8 o 9 dígitos.")
        
        if not nombre_cli_pvd.get().strip():
           return VentanaMensaje(app, "Error", "El nombre del cliente/proveedor es obligatorio.")
        
        if not telefono_cli_pvd.get().strip():
           return VentanaMensaje(app, "Error", "El teléfono del cliente/proveedor es obligatorio.")

        if not validar_telefono(telefono_cli_pvd.get()):
            return VentanaMensaje(app, "Error", "El teléfono del cliente/proveedor es inválido.")

        if not direccion_cli_pvd.get("0.0", "end").strip():
           return VentanaMensaje(app, "Error", "La dirección del cliente/proveedor es obligatorio.")
        
        if tipo_fact.get()== "Servicios Públicos" or tipo_fact.get()=="Impuestos":
            if not vars[1]["descripcion"].get() or not vars[1]["precio"].get() or not vars[1]["cantidad"].get() :
                return VentanaMensaje(app, "Error", f"Por favor llene todos los campos del {tipo_fact.get()} a guardar")
        
            if not num_positivo(vars[1]["precio"].get()):
                return VentanaMensaje(app, "Error", "El monto debe ser un valor positivo. Por favor, ingresa un valor válido.")
        
        else:
            for key, item in vars.items():
                if not item["descripcion"].get() or not item["precio"].get() or not item["cantidad"].get() :
                    return VentanaMensaje(app, "Error", "Por favor llene todos los campos de los producto(s) a guardar o elimina las filas que se encuentren vacias")

                if not num_positivo(item["precio"].get()) or not num_positivo(item["cantidad"].get()):
                     return VentanaMensaje(app, "Error", "El precio y la cantidad debe ser un número positivo. Por favor, ingresa un valor válido.")


        # Insertar cliente/proveedor
        val_cli= nombre_cli_pvd.get(), rif_cli_pvd.get(), direccion_cli_pvd.get("0.0", "end"), telefono_cli_pvd.get()
        sql_cli="""
            INSERT INTO clientes_proveedores (nombre_cli_pvd, rif_cli_pvd, dirección_cli_pvd, telefono_cli_pvd)
            VALUES (%s, %s, %s, %s)
        """
        db.cursor.execute(sql_cli, val_cli)

        # Obtener el ID del cliente/proveedor recién insertado
        ID_cli_pvd = db.cursor.lastrowid

        # Insertar factura
        iva_val = float(iva_fact.get())
        if tipo_fact.get() == "Servicios Públicos" or tipo_fact.get() == "Impuestos":
            monto_neto_val=float(vars[1]["precio"].get())
        else:
            monto_neto_val = sum(float(vars[i]["precio"].get()) * float(vars[i]["cantidad"].get())
                                  for i in list(vars.keys()))


        # Calcular el monto total
        monto_total_val = monto_neto_val + iva_val

        val_fact= fecha_emision.get_date(), nro_fact.get(), ID_cli_pvd, tipo_fact.get(), descripcion_fact.get("0.0", "end").strip(), monto_neto_val, iva_fact.get(), monto_total_val
        sql_fact= """
            INSERT INTO facturas (fecha_emision_fact, nro_fact, ID_cli_pvd, tipo_fact, descripción_fact, monto_neto, IVA, monto_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        db.cursor.execute(sql_fact, val_fact)
        
        # Obtener el ID de la factura recién insertada
        ID_fact = db.cursor.lastrowid

        if tipo_fact.get() == "Servicios Públicos" or tipo_fact.get() == "Impuestos":
            # Insertar servicio o impuesto
            val_impto_serv= vars[1]["descripcion"].get(), vars[1]["precio"].get(), vars[1]["cantidad"].get()
            sql_impto_serv="""
                INSERT INTO servicios_e_impuestos (descripcion_serv_impto, monto_serv_impto, meses_serv_impto)
                VALUES (%s, %s, %s)
            """
            db.cursor.execute(sql_impto_serv, val_impto_serv)
            
            # Obtener el ID del servicio o impuesto recién insertado
            ID_serv_impto = db.cursor.lastrowid
            
            # Insertar detalles de la factura
            db.cursor.execute("""
                INSERT INTO detalles_factura (ID_fact, ID_serv_impto)
                VALUES (%s, %s)
            """, (ID_fact, ID_serv_impto))
            
            # Confirmar las inserciones
            db.connection.commit()
        else:
            for key, producto in vars.items():
                # Insertar producto
                val_pdt= producto["descripcion"].get(), producto["precio"].get(), producto["cantidad"].get()
                
                sql_pdt="""
                    INSERT INTO productos (descripción_pdt, precio_pdt, cantidad_pdt)
                    VALUES (%s, %s, %s)
                """
                db.cursor.execute(sql_pdt, val_pdt)
                
                # Obtener el ID del servicio o impuesto recién insertado
                ID_pdt = db.cursor.lastrowid
                
                # Insertar detalles de la factura
                db.cursor.execute("""
                    INSERT INTO articulos_por_factura (ID_fact, ID_pdt)
                    VALUES (%s, %s)
                """, (ID_fact, ID_pdt))
            
            # Confirmar las inserciones
            db.connection.commit()

        VentanaMensaje(app, "Confirmación de Guardado", "¡Éxito! Tu factura ha sido guardada correctamente.")
        
        clear(nombre_cli_pvd, rif_cli_pvd, direccion_cli_pvd, telefono_cli_pvd, 
           fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars, widgets)

    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error. ¡Inténtalo más tarde!")
        print(err)

        
        # si no se cumple se agrga el registro
    # val= descripcion_pdt.get(), precio_pdt.get()
    # sql="insert INTO productos (pdt_descripcion, pdt_precio) values(%s, %s)"
    # db.cursor.execute(sql, val)
    # db.connection.commit()
    # messaje(marco, "se ha guardado el registro correctamente", "green")
    # get_factures(tabla)
    # clear(descripcion_pdt, precio_pdt)

def update(tabla, marco,  descripcion_pdt, precio_pdt):
        # formulario de modificar factura
    update= False
    if update==False:
        # Obtener los valores de los campos
        descripcion = descripcion_pdt.get()
        precio = precio_pdt.get()

        # Verificar si ambos campos tienen valores
        # if not (descripcion and precio):
        #     messaje(marco, "Por favor, completa todos los campos", "red")
        #     return
        
        # si no se cumple se agrga el registro
        id= tabla.selection()[0]
        val= descripcion_pdt.get(), precio_pdt.get()
        sql="UPDATE productos SET pdt_descripcion =%s, pdt_precio=%s WHERE ID_pdt = "+id
        db.cursor.execute(sql, val)
        db.connection.commit()
        # messaje(marco, "se ha actualizado el registro correctamente", "green")
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
        # messaje(marco, "se ha eliminado el registro correctamente", "green")
    # else:
    #     messaje(marco, "selecciona un registro para eliminar", "red")