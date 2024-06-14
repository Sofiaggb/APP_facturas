import customtkinter as ctk

class Info(ctk.CTkToplevel):
    def __init__(self, parent ):
        super().__init__(parent)
        self.app = self
        # self.data_user= data_user
        self.parent = parent # Guarda una referencia a la ventana principal
        self.app.title("Información General")
        self.app.geometry("500x200+150+150") #tamaño de la ventana
        self.app.resizable(False, False) # bloqueo de redimencion de la ventana, alto y ancho
        self.app.attributes('-topmost' , True)

        texto = ("La Aplicación de Escritorio para la Gestión de Facturas de la "
                 "Distribuidora Caromack C.A. surge como una solución crucial para "
                 "abordar los desafíos actuales en la gestión documental. Esta "
                 "aplicación automatiza el almacenamiento, organización y recuperación "
                 "de las facturas, mejorando la eficiencia y precisión en la administración "
                 "documental. Además, reduce el riesgo de pérdida o extravío de facturas y "
                 "facilita la toma de decisiones de manera ágil y eficiente.")
        
        ctk.CTkLabel(self.app, text=texto, font=("Arial", 16), wraplength=420,
                     justify="center" ).pack( padx=20, pady=20)
# Crear la ventana principal y la ventana de usuario
# root = ctk.CTk()
# app = Info(root)
# root.mainloop()