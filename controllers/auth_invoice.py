import re
from datetime import datetime

def validar_rif(rif):
    # El formato general del RIF es una letra (V, E, J, G), seguida de 9 dígitos
    patron = r'^[VEJG]-[0-9]{8,9}$'
    return re.match(patron, rif) is not None

def validar_telefono(numero):
    # El formato de un número de teléfono es 0 seguido de 3 dígitos para el código de área y 7 dígitos del número
    patron = r'^0[0-9]{3}[0-9]{7}$'
    return re.match(patron, numero) is not None or numero == ""

def validar_fecha(fecha):
    fecha_actual = datetime.now().date()
    diferencia = fecha_actual - fecha
    # Verificar que la fecha no sea futura y no tenga más de 15 años de antigüedad
    return diferencia.days >= 0 and diferencia.days <= 365 * 15

def num_positivo(valor):
    try:
        # Convertir a float y comprobar si es positivo
        return float(valor) > 0
    except ValueError:
        # No se pudo convertir a float, no es un número
        return False

def valilidar_formulario(app, nombre_cli_pvd, rif_cli_pvd, direccion_cli_pvd, telefono_cli_pvd, 
           fecha_emision, nro_fact, tipo_fact, iva_fact, descripcion_fact, vars,VentanaMensaje):
        
        # validaciones 
        if not tipo_fact.get().strip():
           return VentanaMensaje(app, "Error", "El tipo de la factura es obligatorio.")
       
        if not nro_fact.get().strip():
           return VentanaMensaje(app, "Error", "El número de la factura es obligatorio.")

        if not validar_fecha(fecha_emision.get_date()):
            return VentanaMensaje(app, "Error", "La fecha es invalida.  Verifica que la fecha no sea futura o no tenga más de 15 años de antigüedad")

       
        if not descripcion_fact.get("0.0", "end").strip():
           return VentanaMensaje(app, "Error", "La descripción de la factura es obligatoria.")
        
        if not rif_cli_pvd.get().strip():
           return VentanaMensaje(app, "Error", "El RIF del cliente/proveedor es obligatorio.")
        
        if not validar_rif(rif_cli_pvd.get()):
             return VentanaMensaje(app, "Error", "El RIF del cliente/proveedor es inválido, El formato es una letra (V, E, J, G), seguida de una linea (-) y 8 o 9 dígitos.")
        
        if not nombre_cli_pvd.get().strip():
           return VentanaMensaje(app, "Error", "El nombre del cliente/proveedor es obligatorio.")
        
        # if not telefono_cli_pvd.get().strip():
        #    return VentanaMensaje(app, "Error", "El teléfono del cliente/proveedor es obligatorio.")

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

        if not iva_fact.get().strip():
           return VentanaMensaje(app, "Error", "El IVA de la factura es obligatorio.")

        if tipo_fact.get()== "Compras" or tipo_fact.get()=="Ventas":
            if not num_positivo(iva_fact.get()):
                return VentanaMensaje(app, "Error", "El monto del IVA debe ser un valor positivo. Por favor, ingresa un valor válido.")



