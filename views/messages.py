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


class ConfirmacionEliminar(ctk.CTkToplevel):
    def __init__(self, parent, callback, mensaje):
        super().__init__(parent)
        self.callback = callback
        self.title("Confirmación")
        self.geometry("330x150+200+200")
        # Centrar la ventana de confirmación respecto a la ventana padre
        self.center_window(parent)
        self.protocol("WM_DELETE_WINDOW", self.on_no)

        # Mensaje de confirmación
        self.label = ctk.CTkLabel(self, text=mensaje,  wraplength=280)
        self.label.pack(pady=20)

        # Botones Sí y No
        self.btn_yes = ctk.CTkButton(self, text="Sí", command=self.on_yes,
                                      fg_color="#9B0202", hover_color="#DC0F0F",
                                      width=100)
        self.btn_yes.pack(side="left", padx=20, pady=20)
        self.btn_no = ctk.CTkButton(self, text="No", command=self.on_no, width=100)
        self.btn_no.pack(side="right", padx=20, pady=20)

        self.grab_set()  # Hace que la ventana sea modal

    def on_yes(self):
        self.callback(True)
        self.after(50, self.destroy)

    def on_no(self):
        self.callback(False)
        self.destroy()

    def center_window(self, parent):
        # Esperar que la ventana se actualice para obtener sus dimensiones
        self.update_idletasks()
        # Calcular la posición central
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class LoadingPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Generando PDF")
        self.geometry("300x100")
        
        self.label = ctk.CTkLabel(self, text="Se está generando el PDF. Por favor, espere...")
        self.label.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0.0)