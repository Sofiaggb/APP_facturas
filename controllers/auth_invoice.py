import re
from datetime import datetime

def validar_rif(rif):
    # El formato general del RIF es una letra (V, E, J, G), seguida de 9 dígitos
    patron = r'^[VEJG]-[0-9]{8,9}$'
    return re.match(patron, rif) is not None

def validar_telefono(numero):
    # El formato de un número de teléfono es 0 seguido de 3 dígitos para el código de área y 7 dígitos del número
    patron = r'^0[0-9]{3}[0-9]{7}$'
    return re.match(patron, numero) is not None

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


