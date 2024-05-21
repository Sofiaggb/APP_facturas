import customtkinter as ctk

class VentanaMensaje(ctk.CTkToplevel):
    def __init__(self, parent, titulo, mensaje):
        super().__init__(parent)
        self.title(titulo)

          # Tamaño de la ventana
        ancho_ventana = 330
        alto_ventana = 130
        self.geometry(f"{ancho_ventana}x{alto_ventana}")

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Calcular la posición x e y para centrar la ventana
        posicion_x = (ancho_pantalla - ancho_ventana) // 2
        posicion_y = (alto_pantalla - alto_ventana) // 2

        # Establecer la posición de la ventana en el centro
        self.geometry(f"+{posicion_x}+{posicion_y}")

        # self.geometry("300x100")  # Tamaño de la ventana
        self.resizable(False, False)# bloqueo de redimencion de la ventana, alto y ancho

        # Configurar el mensaje en la ventana
        self.label_mensaje = ctk.CTkLabel(self, text=mensaje, wraplength=280)
        self.label_mensaje.pack(pady=(20, 20), expand=True)

        self.grab_set()  # Hace que la ventana sea modal

