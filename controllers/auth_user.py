import re #expresiones regulares

def validar_contraseña(app, contraseña, reentre_contraseña, VentanaMensaje):
        if not contraseña.get().strip() or not reentre_contraseña.get().strip():
            return VentanaMensaje(app, "Error", "La contraseña es obligatoria en ambos campos.")

        if contraseña.get() != reentre_contraseña.get():
            return VentanaMensaje(app, "Error", "Las contraseñas no coinciden, por favor verifica.")

        # Validaciones de complejidad de contraseña
        if len(contraseña.get()) < 8:
            return VentanaMensaje(app, "Error", "La contraseña debe tener al menos 8 caracteres.")
        
        if not re.search("[a-z]", contraseña.get()):
            return VentanaMensaje(app, "Error", "La contraseña debe contener al menos una letra minúscula.")
        
        if not re.search("[A-Z]", contraseña.get()):
            return VentanaMensaje(app, "Error", "La contraseña debe contener al menos una letra mayúscula.")
        
        if not re.search("[0-9]", contraseña.get()):
            return VentanaMensaje(app, "Error", "La contraseña debe contener al menos un número.")
        
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", contraseña.get()):
            return VentanaMensaje(app, "Error", "La contraseña debe contener al menos un símbolo especial.")
       