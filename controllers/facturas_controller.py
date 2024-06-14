from datetime import date
from connection import connection_bd # database
from views.messages import  VentanaMensaje # mensages
from controllers.auth_invoice import valilidar_formulario
db = connection_bd()

def clear(nombre_cli_pvd, rif_cli_pvd, direccion_cli_pvd, telefono_cli_pvd, 
           fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars, widgets,
           monto_neto, monto_total):
    # limpiar todos los campos
    nombre_cli_pvd.set("")
    rif_cli_pvd.set("")
    direccion_cli_pvd.delete("0.0", "end")  
    telefono_cli_pvd.set("")
    fecha_emision.set_date(date.today())
    nro_fact.set("")
    tipo_fact.set("")
    descripcion_fact.delete("0.0", "end")  
    # montos
    iva_fact.set("")
    monto_neto.set(0)
    monto_total.set(0)

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

def get_facturas(app):
    try:
        # seleccionar los elemtos y devolverlos
        sql="""SELECT ID_fact,fecha_emision_fact, nro_fact,tipo_fact, descripción_fact 
                FROM facturas
                WHERE is_deleted = FALSE
                ORDER BY ID_fact DESC;"""
        db.cursor.execute(sql)
        filas= db.cursor.fetchall()

        facturas_data = []
        for fila in filas:
            facturas_data.append({
                "id": fila[0],
                "fecha": fila[1],
                "nro": fila[2],
                "tipo": fila[3],
                "descripcion": fila[4]
            })
        
        return facturas_data
    
    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error al devolver las facturas. ¡Inténtalo más tarde!")
        print(err)

def get_factura(id, tipo):
        
        if tipo =="Ventas" or tipo == "Compras":

            sql = """SELECT f.fecha_emision_fact, f.nro_fact,f.tipo_fact, f.descripción_fact, cp.nombre_cli_pvd, cp.rif_cli_pvd, cp.dirección_cli_pvd, cp.telefono_cli_pvd, 
                        p.descripción_pdt, p.precio_pdt, p.cantidad_pdt, f.monto_neto, f.IVA, f.monto_total, f.ID_fact, f.ID_cli_pvd, apf.ID_pdt
                    FROM facturas f
                    JOIN clientes_proveedores cp ON f.ID_cli_pvd = cp.ID_cli_pvd
                    JOIN articulos_por_factura apf ON f.ID_fact = apf.ID_fact
                    JOIN productos p ON apf.ID_pdt = p.ID_pdt
                    WHERE f.ID_fact =%s"""
            db.cursor.execute(sql, (id,))
            results = db.cursor.fetchall()
               # Crear un diccionario para la información de la factura
            factura_info = {
                "ID":None,
                "id_cp":None,
                "fecha_emision_fact": None,
                "nro_fact": None,
                "tipo_fact": None,
                "descripción_fact": None,
                "cliente": {
                    "nombre": None,
                    "rif": None,
                    "dirección": None,
                    "telefono": None
                },
                "productos": [],
                "monto_neto": None,
                "IVA": None,
                "monto_total": None
            }

            if results:
                # Rellenar la información de la factura
                first_row = results[0]
                factura_info["fecha_emision_fact"] = first_row[0]
                factura_info["nro_fact"] = first_row[1]
                factura_info["tipo_fact"] = first_row[2]
                factura_info["descripción_fact"] = first_row[3]
                factura_info["cliente"]["nombre"] = first_row[4]
                factura_info["cliente"]["rif"] = first_row[5]
                factura_info["cliente"]["dirección"] = first_row[6]
                factura_info["cliente"]["telefono"] = first_row[7]
                factura_info["monto_neto"] = first_row[11]
                factura_info["IVA"] = first_row[12]
                factura_info["monto_total"] = first_row[13]
                factura_info["ID"] = first_row[14]
                factura_info["id_cp"] = first_row[15]

                # Rellenar la información de los productos
                for fila in results:
                    producto = {
                        "ID_pdt":fila[16],
                        "descripción_pdt": fila[8],
                        "precio_pdt": fila[9],
                        "cantidad_pdt": fila[10]
                    }
                    factura_info["productos"].append(producto)

            return factura_info
        
        elif tipo == "Servicios Públicos" or tipo == "Impuestos":
            sql = """SELECT f.fecha_emision_fact, f.nro_fact, f.tipo_fact, f.descripción_fact, cp.nombre_cli_pvd, cp.rif_cli_pvd, cp.dirección_cli_pvd, cp.telefono_cli_pvd, 
                            si.descripcion_serv_impto, si.monto_serv_impto, si.meses_serv_impto, f.monto_neto, f.IVA, f.monto_total, f.ID_fact, f.ID_cli_pvd, si.ID_serv_impto
                    FROM facturas f
                    JOIN clientes_proveedores cp ON f.ID_cli_pvd = cp.ID_cli_pvd
                    JOIN detalles_factura df ON f.ID_fact = df.ID_fact
                    JOIN servicios_e_impuestos si ON df.ID_serv_impto = si.ID_serv_impto
                    WHERE f.ID_fact = %s"""
            db.cursor.execute(sql, (id,))
            results = db.cursor.fetchall()
            
            # Crear un diccionario para la información de la factura
            factura_info = {
                "ID":None,
                "id_cp":None,
                "ID_serv_impto": None,
                "fecha_emision_fact": None,
                "nro_fact": None,
                "tipo_fact": None,
                "descripción_fact": None,
                "cliente": {
                    "nombre": None,
                    "rif": None,
                    "dirección": None,
                    "telefono": None
                },
                "servicios_impuestos": [],
                "monto_neto": None,
                "IVA": None,
                "monto_total": None
            }

            if results:
                # Rellenar la información de la factura
                first_row = results[0]
                factura_info["fecha_emision_fact"] = first_row[0]
                factura_info["nro_fact"] = first_row[1]
                factura_info["tipo_fact"] = first_row[2]
                factura_info["descripción_fact"] = first_row[3]
                factura_info["cliente"]["nombre"] = first_row[4]
                factura_info["cliente"]["rif"] = first_row[5]
                factura_info["cliente"]["dirección"] = first_row[6]
                factura_info["cliente"]["telefono"] = first_row[7]
                factura_info["monto_neto"] = first_row[11]
                factura_info["IVA"] = first_row[12]
                factura_info["monto_total"] = first_row[13]
                factura_info["ID"] = first_row[14]
                factura_info["id_cp"] = first_row[15]
                factura_info["ID_serv_impto"] = first_row[16]


                # Rellenar la información de los servicios o impuestos
                for fila in results:
                    servicio_impuesto = {
                        "descripcion_serv_impto": fila[8],
                        "monto_serv_impto": fila[9],
                        "meses_serv_impto": fila[10],
                    }
                    factura_info["servicios_impuestos"].append(servicio_impuesto)

            return factura_info
        else:
            print("Tipo de factura no reconocido.")
            return None


def create(app, nombre_cli_pvd, rif_cli_pvd, direccion_cli_pvd, telefono_cli_pvd, 
           fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars, widgets,
           monto_neto, monto_total, facturas_section):
    
    try:
        # validaciones 
        validar=valilidar_formulario(app, nombre_cli_pvd, rif_cli_pvd, direccion_cli_pvd, telefono_cli_pvd, 
        fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars, VentanaMensaje)
        
        if not validar:

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

            val_fact= fecha_emision.get_date(), nro_fact.get(), ID_cli_pvd, tipo_fact.get(), descripcion_fact.get("0.0", "end").strip(), monto_neto.get(), iva_fact.get(), monto_total.get()
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
            fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars, widgets,
            monto_neto, monto_total)

            # Se ejecuta este código cuando se cierra la ventana
            if facturas_section:
                facturas_section.hide()

            # Recargar la pantalla principal 
            facturas_section.actualizar_interfaz()

        

    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error. ¡Inténtalo más tarde!")
        print(err)



def update(app, ID_fact, ID_cp, ID_imp_pdt, nombre_cli_pvd, rif_cli_pvd, direccion_cli_pvd, telefono_cli_pvd, 
           fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars, widgets,
           monto_neto, monto_total, facturas_section, ventana_fact, ventana_form, parent):
    
    try:
        validar=valilidar_formulario(app, nombre_cli_pvd, rif_cli_pvd, direccion_cli_pvd, telefono_cli_pvd, 
        fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars, VentanaMensaje)
        
        if not validar:
             # Insertar cliente/proveedor
            #  cliente
            print(telefono_cli_pvd.get())
            val_cli= nombre_cli_pvd.get(), rif_cli_pvd.get(), direccion_cli_pvd.get("0.0", "end"), telefono_cli_pvd.get(), ID_cp
            sql_cli="""
                 UPDATE clientes_proveedores
                    SET nombre_cli_pvd = %s, rif_cli_pvd = %s, dirección_cli_pvd = %s, 
                    telefono_cli_pvd = %s
                    WHERE ID_cli_pvd = %s
                            """
            db.cursor.execute(sql_cli, val_cli)

            # factura
            val_fact = fecha_emision.get_date(), nro_fact.get(), tipo_fact.get(), descripcion_fact.get("0.0", "end").strip(), monto_neto.get(), iva_fact.get(), monto_total.get(), ID_fact
            sql_fact = """
                UPDATE facturas
                SET fecha_emision_fact = %s, nro_fact = %s, tipo_fact = %s, descripción_fact = %s, monto_neto = %s, IVA = %s, monto_total = %s
                WHERE ID_fact = %s
            """
            db.cursor.execute(sql_fact, val_fact)

            # impuestos y servicios
            if tipo_fact.get() in ["Servicios Públicos", "Impuestos"]:
                val_impto_serv = vars[1]["descripcion"].get(), vars[1]["precio"].get(), vars[1]["cantidad"].get(), ID_imp_pdt
                sql_impto_serv = """
                    UPDATE servicios_e_impuestos
                    SET descripcion_serv_impto = %s, monto_serv_impto = %s, meses_serv_impto = %s
                    WHERE ID_serv_impto = %s
                """
                db.cursor.execute(sql_impto_serv, val_impto_serv)

                # Confirmar las inserciones
                db.connection.commit()
                ventana_fact.destroy()
                ventana_form.destroy()
                # Se ejecuta este código cuando se cierra la ventana
                if facturas_section:
                    facturas_section.hide()

                # Recargar la pantalla principal 
                facturas_section.actualizar_interfaz()

                parent.after(1000, lambda:VentanaMensaje(parent, "Confirmación de Edición", "¡Éxito! Tu factura ha sido editada correctamente."))


            else:
                productos_existentes = len(vars)

                if productos_existentes < len(ID_imp_pdt):
                    VentanaMensaje(app, "Error de Edición", "Se ha detectado que falta un ID de producto, lo que indica que se ha borrado un producto. Esto no está permitido.")
                else:
                    # productos
                    index=0
                    error_flag=False
                    for key, producto in vars.items():
                        if index < len(ID_imp_pdt):
                            # print(len(ID_imp_pdt))
                            # print(index)
                            ID_pdt = ID_imp_pdt[index]
                            index+=1
                            val_pdt = (producto["descripcion"].get(), producto["precio"].get(), producto["cantidad"].get(), ID_pdt)
                            sql_pdt = """
                                UPDATE productos
                                SET descripción_pdt = %s, precio_pdt = %s, cantidad_pdt = %s
                                WHERE ID_pdt = %s
                            """
                            db.cursor.execute(sql_pdt, val_pdt)

                        # else:
                            # # Insertar producto
                            # val_pdt= producto["descripcion"].get(), producto["precio"].get(), producto["cantidad"].get()
                            
                            # sql_pdt="""
                            #     INSERT INTO productos (descripción_pdt, precio_pdt, cantidad_pdt)
                            #     VALUES (%s, %s, %s)
                            # """
                            # db.cursor.execute(sql_pdt, val_pdt)
                            
                            # # Obtener el ID del servicio o impuesto recién insertado
                            # ID_pdt = db.cursor.lastrowid
                            
                            # # Insertar detalles de la factura
                            # db.cursor.execute("""
                            #     INSERT INTO articulos_por_factura (ID_fact, ID_pdt)
                            #     VALUES (%s, %s)
                            # """, (ID_fact, ID_pdt))
                        else:
                            error_flag = True  # Se encontró un error
                            break  # Salir del bucle for

                    if error_flag:
                        # Si se encontró un error, mostrar la ventana de mensaje
                        VentanaMensaje(app, "Error de Edición", "No puedes agregar más productos a una factura ya emitida, por favor borra los campos extra que agregaste")
                    else:
                        # Confirmar las inserciones
                        db.connection.commit()
                        ventana_fact.destroy()
                        ventana_form.destroy()
                        # Se ejecuta este código cuando se cierra la ventana
                        if facturas_section:
                            facturas_section.hide()

                        # Recargar la pantalla principal 
                        facturas_section.actualizar_interfaz()

                        parent.after(1000, lambda:VentanaMensaje(parent, "Confirmación de Edición", "¡Éxito! Tu factura ha sido editada correctamente."))


    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error. ¡Inténtalo más tarde!")
        print(err)

def papelera(app, ID_fact):
    try:
        sql_eliminacion_logica = """UPDATE facturas
                                    SET is_deleted = TRUE
                                    WHERE ID_fact = %s;"""
        val_eliminacion_logica = (ID_fact,)
        db.cursor.execute(sql_eliminacion_logica, val_eliminacion_logica)

        db.connection.commit()

        app.after(2000, lambda: VentanaMensaje(app, "Eliminación", "Tu factura ha sido movida a papelera correctamente."))
    except Exception as err:
        VentanaMensaje(app, "Error", "Error al buscar la factura. Por favor, verifica que la factura exista, recarga la sección de facturas para verificar")
        print(err)

def get_papelera_facts(app):
    try:
        # seleccionar los elemtos y devolverlos
        sql="""SELECT ID_fact,fecha_emision_fact, nro_fact,tipo_fact, descripción_fact 
                FROM facturas
                WHERE is_deleted = TRUE
                ORDER BY ID_fact DESC;"""
        db.cursor.execute(sql)
        filas= db.cursor.fetchall()

        facturas_data = []
        for fila in filas:
            facturas_data.append({
                "id": fila[0],
                "fecha": fila[1],
                "nro": fila[2],
                "tipo": fila[3],
                "descripcion": fila[4]
            })
        
        return facturas_data
    
    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error al devolver las facturas. ¡Inténtalo más tarde!")
        print(err)

def delete(app, ID_fact, tipo):
    try:
        if tipo in  ["Servicios Públicos", "Impuestos"]:
            # Eliminar los servicios o impuestos relacionados con la factura en la tabla detalles_factura
            sql_eliminar_servicios_impuestos = "DELETE FROM detalles_factura WHERE ID_fact = %s"
            val_eliminar_servicios_impuestos = (ID_fact,)
            db.cursor.execute(sql_eliminar_servicios_impuestos, val_eliminar_servicios_impuestos)

            # Eliminar todos los servicios o impuestos que no están asociados con ninguna factura
            sql_eliminar_servicios_impuestos_no_asociados = """
            DELETE FROM servicios_e_impuestos
            WHERE ID_serv_impto NOT IN (SELECT ID_serv_impto FROM detalles_factura);
            """
            db.cursor.execute(sql_eliminar_servicios_impuestos_no_asociados)

        else:
            # Eliminar los artículos relacionados con la factura en la tabla articulos_por_factura
            sql_eliminar_articulos = "DELETE FROM articulos_por_factura WHERE ID_fact = %s"
            val_eliminar_articulos = (ID_fact,)
            db.cursor.execute(sql_eliminar_articulos, val_eliminar_articulos)

            # -- Eliminar todos los productos que no están asociados con ninguna factura
            sql_eliminar_productos = """DELETE FROM productos
                                WHERE ID_pdt NOT IN (SELECT ID_pdt FROM articulos_por_factura);"""

            db.cursor.execute(sql_eliminar_productos)

        # Primero, obtén el ID del cliente asociado a la factura
        sql_obtener_id_cliente = "SELECT ID_cli_pvd FROM facturas WHERE ID_fact = %s"
        val_factura = (ID_fact,)
        db.cursor.execute(sql_obtener_id_cliente, val_factura)
        ID_cli_pvd_a_eliminar = db.cursor.fetchone()[0]

            # Eliminar la factura de la tabla facturas
        sql_eliminar_factura = "DELETE FROM facturas WHERE ID_fact = %s"
        val_eliminar_factura = (ID_fact,)
        db.cursor.execute(sql_eliminar_factura, val_eliminar_factura)


        # Y finalmente, elimina el cliente usando el ID obtenido previamente
        sql_eliminar_cliente = "DELETE FROM clientes_proveedores WHERE ID_cli_pvd = %s"
        val_cliente = (ID_cli_pvd_a_eliminar,)
        db.cursor.execute(sql_eliminar_cliente, val_cliente)

        db.connection.commit()

        app.after(500, lambda: VentanaMensaje(app, "Eliminación", "Tu factura ha sido eliminada correctamente."))

    except Exception as err:
        VentanaMensaje(app, "Error", "Error al buscar la factura. Por favor, verifica que la factura exista, recarga la sección de facturas para verificar")
        print(err)


    # No olvides hacer commit para aplicar los cambios en la base de datos
    db.connection.commit()

def recuperar(app, ID_fact):
    try:
        sql_eliminacion_logica = """UPDATE facturas
                                    SET is_deleted = FALSE
                                    WHERE ID_fact = %s;"""
        val_eliminacion_logica = (ID_fact,)
        db.cursor.execute(sql_eliminacion_logica, val_eliminacion_logica)

        db.connection.commit()

        app.after(2000, lambda: VentanaMensaje(app, "Recuperación", "Tu factura ha sido recuperada correctamente."))
    except Exception as err:
        VentanaMensaje(app, "Error", "Error al recuperar la factura. Por favor, verifica que la factura exista, recarga la sección de facturas para verificar")
        print(err)

def busqueda(app,valor):
    try:
        # Consulta SQL que busca en varias tablas y columnas
        query = """
        SELECT DISTINCT f.ID_fact, f.fecha_emision_fact, f.nro_fact, f.tipo_fact, f.descripción_fact, 
        f.ID_cli_pvd, f.is_deleted, cp.nombre_cli_pvd, p.descripción_pdt, 
        si.descripcion_serv_impto
        FROM facturas f
        LEFT JOIN clientes_proveedores cp ON f.ID_cli_pvd = cp.ID_cli_pvd
        LEFT JOIN articulos_por_factura af ON f.ID_fact = af.ID_fact
        LEFT JOIN productos p ON af.ID_pdt = p.ID_pdt
        LEFT JOIN detalles_factura df ON f.ID_fact = df.ID_fact
        LEFT JOIN servicios_e_impuestos si ON df.ID_serv_impto = si.ID_serv_impto
        WHERE (f.tipo_fact LIKE %s
        OR f.nro_fact LIKE %s
        OR cp.nombre_cli_pvd LIKE %s
        OR p.descripción_pdt LIKE %s
        OR si.descripcion_serv_impto LIKE %s
        OR f.fecha_emision_fact LIKE %s)
        AND f.is_deleted = False
        GROUP BY f.ID_fact
        ORDER BY f.ID_fact DESC
        """
        
        # El valor '%' se utiliza en SQL para indicar un comodín que puede coincidir con cualquier secuencia de caracteres
        valor_busqueda = f"%{valor}%"
        
        # Ejecutar la consulta con el valor de búsqueda para cada columna
        db.cursor.execute(query, [valor_busqueda] * 6)
        
        # Obtener y retornar los resultados
        filas = db.cursor.fetchall()

        
        facturas_data = []
        for fila in filas:
            facturas_data.append({
                "id": fila[0],
                "fecha": fila[1],
                "nro": fila[2],
                "tipo": fila[3],
                "descripcion": fila[4]
            })
            
        return facturas_data
    
    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error al devolver las facturas. ¡Inténtalo más tarde!")
        print(err)