import customtkinter as ctk
from tkinter import StringVar
from controllers.users_controller import crear_user, login
# from main import AplicacionPantallaCompleta
# pyinstaller --noconsole --onefile --icon=logo_app.ico --name="Gestion Facturas" session.py

class session:
    def __init__(self):
        self.app = ctk.CTk()
          # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.app.winfo_screenwidth()
        alto_pantalla = self.app.winfo_screenheight()
        # Calcular la posición x e y para centrar la ventana
        posicion_x = (ancho_pantalla - 400) // 2
        posicion_y = (alto_pantalla - 350) // 2
        # Establecer la posición de la ventana en el centro
        self.app.geometry(f"400x350+{posicion_x}+{posicion_y}")
        self.app.title("Inicio de Sesión")

        # variables
        self.user=StringVar()
        self.nivel = StringVar()
        self.contraseña=StringVar()
        self.reenter_contraseña=StringVar()
        self.pregunta1=StringVar()
        self.pregunta2=StringVar()

         # Frame para los widgets de inicio de sesión
        self.frame_inicio_sesion = ctk.CTkFrame(self.app, width=400, height=350, fg_color="transparent",  bg_color="transparent" )
        self.frame_inicio_sesion.pack()

        # Crear y configurar los widgets
        self.label_usuario_registro = ctk.CTkLabel(self.frame_inicio_sesion, text="Inicio de Sesión", font=("Arial", 20, "bold"))
        self.label_usuario_registro.pack( padx=80, pady=(20,0))

        self.label_usuario = ctk.CTkLabel(self.frame_inicio_sesion, text="Usuario:", font=("Arial", 16))
        self.label_usuario.pack(anchor="w", padx=80, pady=(10,0))

        self.entry_usuario = ctk.CTkEntry(self.frame_inicio_sesion,textvariable=self.user, width=200, font=("Arial", 16))
        self.entry_usuario.pack(padx=20, pady=(0,20))

        self.label_contraseña = ctk.CTkLabel(self.frame_inicio_sesion, text="Contraseña:", font=("Arial", 16))
        self.label_contraseña.pack(anchor="w", padx=80, pady=0)

        # Marco para el campo de contraseña y el botón de mostrar/ocultar
        self.frame_contraseña = ctk.CTkFrame(self.frame_inicio_sesion, fg_color="transparent",  bg_color="transparent")
        self.frame_contraseña.pack(padx=(50,0), pady=(0,5))

        self.entry_contraseña = ctk.CTkEntry(self.frame_contraseña,textvariable=self.contraseña,
                                              show="*", width=200, font=("Arial", 16))
        self.entry_contraseña.pack(side="left")

        self.boton_mostrar = ctk.CTkButton(self.frame_contraseña, text="👁️", 
                                           command=self.mostrar_contraseña, bg_color="transparent",
                                           fg_color="transparent", hover_color="#252524",
                                           font=("Arial", 20), width=20, height=20)
        self.boton_mostrar.pack(side="left", fill="y")

        # Crear y configurar el botón de registro
        self.boton_registro = ctk.CTkButton(self.frame_inicio_sesion, text="¿Olvidaste tu contraseña?", font=("Arial", 12),
                                            fg_color="transparent", hover_color="#252524",
                                            text_color="#9BA9EA",
                                            command=self.contraseña_olvidada)
        self.boton_registro.pack(anchor="w", padx=60, pady=(0,10))

        self.boton_iniciar_sesion = ctk.CTkButton(self.frame_inicio_sesion, text="Iniciar Sesión", width=130,
                                             height=40, font=("Arial", 16), fg_color="#4824B7",
                                              command=self.iniciar_sesion)
        self.boton_iniciar_sesion.pack(padx=20, pady=(10,0))

         # Crear y configurar el label de registro
        self.label_registro = ctk.CTkLabel(self.frame_inicio_sesion, text="¿No tienes una cuenta?", font=("Arial", 12))
        self.label_registro.pack(side="left",anchor="s", padx=(60,0),pady=10)

        # Crear y configurar el botón de registro
        self.boton_registro = ctk.CTkButton(self.frame_inicio_sesion, text="Regístrate aquí", font=("Arial", 12),
                                            fg_color="transparent", hover_color="#252524",
                                            text_color="#9BA9EA",
                                            command=self.mostrar_registro)
        self.boton_registro.pack(side="left",anchor="s",padx=(0,20), pady=10)

      # Variable para el estado del texto
        self.mostrar = False
        # Ejecutar la aplicación
        self.app.mainloop()

    def mostrar_contraseña(self):
        if self.mostrar:
            self.entry_contraseña.configure(show="*")
            self.boton_mostrar.configure(text="👁️") 
            self.mostrar = False
        else:
            self.entry_contraseña.configure(show="")
            self.boton_mostrar.configure(text="❌")
            self.mostrar = True
    # Función para registrar un nuevo usuario
    def registrar_usuario(self):
         # Intentar crear el usuario
        usuario_creado = crear_user(self.app, self.user, self.contraseña, 
                                    self.reenter_contraseña, self.pregunta1, self.pregunta2,
                                    self.nivel)
        
        if usuario_creado:
            # Si el usuario se creó correctamente, mostrar la ventana de inicio de sesión
            self.mostrar_inicio_sesion()

    def iniciar_sesion(self):
        # from main import AplicacionPantallaCompleta

        try:
            user_data = login(self.app, self.user, self.contraseña)
            if user_data:
                # self.app.destroy()  # Cerrar la ventana de inicio de sesión
                self.abrir_aplicacion_principal(user_data)  # Retrasar la apertura de la nueva ventana

        except Exception as e:
            print(e)


    def abrir_aplicacion_principal(self, user_data):
        from main import AplicacionPantallaCompleta
        # Ocultar la ventana de inicio de sesión
        self.app.withdraw()
         # Crear una nueva instancia de CTkToplevel (ventana principal)
        app_principal = AplicacionPantallaCompleta(self.app, user_data)

    def contraseña_olvidada(self):
        from views.recover_password import password
        password(self.app)

        
    def mostrar_inicio_sesion(self):
        # Ocultar widgets de registro
        self.frame_registro.pack_forget()
        self.user.set("")
        self.contraseña.set("")
        self.reenter_contraseña.set("")
        self.pregunta1.set("")
        self.pregunta2.set("")

        # Mostrar el frame de inicio de sesión
        self.frame_inicio_sesion.pack()

    def mostrar_registro(self):
        # Ocultar widgets de inicio de sesión
        self.frame_inicio_sesion.pack_forget()
        self.user.set("")
        self.contraseña.set("")

        niveles = ["Admin", "Usuario"]

        # Frame para los widgets de registro
        self.frame_registro = ctk.CTkScrollableFrame(self.app, width=400, height=350, fg_color="transparent",  bg_color="transparent" )
        self.frame_registro.pack( pady=(0,10))

        # Widgets para el registro
        self.label_usuario_registro = ctk.CTkLabel(self.frame_registro, text="Registro", font=("Arial", 20, "bold"))
        self.label_usuario_registro.pack( padx=80, pady=(10,0))

        self.label_usuario_registro = ctk.CTkLabel(self.frame_registro, text="Usuario:", font=("Arial", 14))
        self.label_usuario_registro.pack(anchor="w", padx=80, pady=(10,0))

        self.entry_usuario_registro = ctk.CTkEntry(self.frame_registro, textvariable=self.user,width=200, font=("Arial", 14))
        self.entry_usuario_registro.pack(padx=20, pady=(0,10))
        
        self.label_usuario_registro = ctk.CTkLabel(self.frame_registro, text="Nivel de Usuario:", font=("Arial", 14))
        self.label_usuario_registro.pack(anchor="w", padx=80, pady=(10,0))

        self.entry_usuario_registro = ctk.CTkOptionMenu(self.frame_registro, values= niveles, variable=self.nivel)
        self.entry_usuario_registro.pack(padx=20, pady=(0,10))

        self.label_contraseña_registro = ctk.CTkLabel(self.frame_registro, text="Contraseña:", font=("Arial", 14))
        self.label_contraseña_registro.pack(anchor="w", padx=80, pady=0)

        self.entry_contraseña_registro = ctk.CTkEntry(self.frame_registro,textvariable=self.contraseña,
                                                       show="", width=200, font=("Arial", 14))
        self.entry_contraseña_registro.pack(padx=20, pady=(0,10))

        self.label_contraseña_registro = ctk.CTkLabel(self.frame_registro, text="Vuelva a ingresar la contraseña:", font=("Arial", 14))
        self.label_contraseña_registro.pack(anchor="w", padx=80, pady=0)

        self.entry_contraseña_registro = ctk.CTkEntry(self.frame_registro, textvariable=self.reenter_contraseña,
                                                       show="", width=200, font=("Arial", 14))
        self.entry_contraseña_registro.pack(padx=20, pady=(0,10))

        # preguntas de recuperacion de contraseña
        self.label_contraseña_registro = ctk.CTkLabel(self.frame_registro, text="¿Animal favorito?", font=("Arial", 14))
        self.label_contraseña_registro.pack(anchor="w", padx=80, pady=0)

        self.entry_contraseña_registro = ctk.CTkEntry(self.frame_registro, textvariable=self.pregunta1,
                                                       show="", width=200, font=("Arial", 14))
        self.entry_contraseña_registro.pack(padx=20, pady=(0,10))

        self.label_contraseña_registro = ctk.CTkLabel(self.frame_registro, text="¿Cuál es tu heroe?", font=("Arial", 14))
        self.label_contraseña_registro.pack(anchor="w", padx=80, pady=0)

        self.entry_contraseña_registro = ctk.CTkEntry(self.frame_registro, textvariable=self.pregunta2,
                                                       show="", width=200, font=("Arial", 14))
        self.entry_contraseña_registro.pack(padx=20, pady=(0,10))


        self.boton_registrarse = ctk.CTkButton(self.frame_registro, text="Registrarse", width=130,
                                               height=40, font=("Arial", 16), fg_color="#4824B7",
                                               command=self.registrar_usuario)
        self.boton_registrarse.pack(padx=20, pady=(10,0))

        self.label_ya_tienes_cuenta = ctk.CTkLabel(self.frame_registro, text="¿Ya tienes una cuenta?", font=("Arial", 12))
        self.label_ya_tienes_cuenta.pack(side="left", anchor="s", padx=(60,0), pady=10)

        self.boton_volver_inicio = ctk.CTkButton(self.frame_registro, text="Inicia sesión aquí", font=("Arial", 12),
                                                 fg_color="transparent", hover_color="#252524",
                                                 text_color="#9BA9EA",
                                                 command=self.mostrar_inicio_sesion)
        self.boton_volver_inicio.pack(side="left", anchor="s", padx=(0,20), pady=10)


if __name__ == "__main__":
    try:
        session()


    except Exception as err:
        print("error en sesison", err)
