from connection import connection_bd # database
from views.messages import  VentanaMensaje # mensages
from datetime import datetime
from .auth_user import validar_contraseña

db = connection_bd()

def crear_user(app, user, contraseña, reentre_contraseña, pregunta1, pregunta2, nivel):
    try:
        if not user.get().strip():
           return VentanaMensaje(app, "Error", "El nombre de usuario es obligatorio.")
        
        validar_con = validar_contraseña(app, contraseña, reentre_contraseña, VentanaMensaje)
        
        if not validar_con:
            if not pregunta1.get().strip() or not pregunta2.get().strip():
                VentanaMensaje(app, "Error", "Debes responser las preguntas.")
                return False
            
            # Verificar si el nombre de usuario ya existe
            #  COUNT(*) en SQL se utiliza para contar el número de filas que coinciden con un criterio específico
            sql_verificacion = "SELECT COUNT(*) FROM Usuarios WHERE nombre_usuario =%s"
            db.cursor.execute(sql_verificacion, (user.get(),))
            resultado = db.cursor.fetchone()

            if resultado[0] > 0:
                VentanaMensaje(app, "Error", "El nombre de usuario ya está en uso. Por favor, elige otro.")
                return False
            
            # Verifica si ya existe un usuario con el nivel "Admin"
            nivel_usuario = nivel.get()  # Obtener el nivel de usuario

            sql_verificacion = "SELECT COUNT(*) FROM Usuarios WHERE nivel_usuario = %s"
            db.cursor.execute(sql_verificacion, (nivel_usuario,))
            resultado = db.cursor.fetchone()

            if nivel_usuario == "Admin" and resultado[0] > 0:
                VentanaMensaje(app, "Error", "El nivel de usuario 'Admin' ya está en uso. Por favor, elige otro.")
                return False
            
            # Insertar usuario y contraseña
            val= user.get(), contraseña.get(), pregunta1.get(), pregunta2.get(), nivel.get()
            sql="""
                    INSERT INTO Usuarios (nombre_usuario, contraseña_usuario,
                                         pregunta1, pregunta2, nivel_usuario)
                    VALUES (%s, %s, %s, %s, %s)
                """
            db.cursor.execute(sql, val)
            db.connection.commit()

            # Aquí puedes mostrar un mensaje de éxito si lo deseas
            VentanaMensaje(app, "Éxito", "Usuario creado correctamente.")
            return True  # Devolver True si el usuario se creó correctamente
    
    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error. ¡Inténtalo más tarde!")
        print(err)
        return False
    
def login(app, user, contraseña):
    try:
        if not user.get().strip():
                VentanaMensaje(app, "Error", "El usuario es obligatorio.")
                return None
        
        if not contraseña.get().strip():
                VentanaMensaje(app, "Error", "La contraseña es obligatoria.")
                return None
        
        # Verificar si el nombre de usuario y la contraseña coinciden
        sql_verificacion = """SELECT id_usuario, nombre_usuario, nivel_usuario
                         FROM Usuarios 
                        WHERE nombre_usuario = %s AND contraseña_usuario = %s"""
        db.cursor.execute(sql_verificacion, (user.get(), contraseña.get()))
        resultado = db.cursor.fetchone()

        data_user= {
            "ID":None,
            "user":None,
            "nivel":None
        }

        if resultado:
            data_user["ID"]= resultado[0]
            data_user["user"]= resultado[1]
            data_user["nivel"]= resultado[2]


             # Registrar la nueva sesión
            sql_registro_sesion = """INSERT INTO Sesiones (ID_usuario, fecha_acceso, fecha_salida)
                                     VALUES (%s, %s, 'None')"""  # NULL o una fecha futura para 'fecha_salida'
            db.cursor.execute(sql_registro_sesion, (resultado[0], datetime.now()))
            # Confirmar las inserciones
            db.connection.commit()
            user.set("")
            contraseña.set("")
            return data_user
        else:
            # Si no se encontró un usuario, el inicio de sesión falló
            VentanaMensaje(app, "Error", "Nombre de usuario o contraseña incorrectos.")
            return None
        
    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error. ¡Inténtalo más tarde!")
        print(err)
        return None
    
def verificar_respuestas(app, user, res1, res2):
    try:
        if not user.get().strip():
                VentanaMensaje(app, "Error", "El campo de usuario es obligatorio.")
                return False
        
        if not res1.get().strip() or not res2.get().strip():
                VentanaMensaje(app, "Error", "Debes responser las preguntas.")
                return False

        sql="SELECT pregunta1, pregunta2 FROM Usuarios WHERE nombre_usuario = %s"
        db.cursor.execute(sql, (user.get(),))

        resultado = db.cursor.fetchone()

        if resultado:
            res_bd_1, res_bd_2 = resultado

            # Verificar si las respuestas coinciden
            if res1.get() == res_bd_1 and res2.get() == res_bd_2:
                return True
            else:
                VentanaMensaje(app, "Error", "Las respuestas no coinciden. Inténtalo de nuevo.")
                return False

        else:
            VentanaMensaje(app, "Error", "Usuario no encontrado en la base de datos.")
            return False

    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error. ¡Inténtalo más tarde!")
        print(err)
        return False

def cambiar_password(app,user, con1, con2):
    try:
        validar_con = validar_contraseña(app, con1, con2, VentanaMensaje)
        
        if not validar_con:
             # Insertar usuario y contraseña
            val= (con1.get(), user.get())
            sql=""" UPDATE Usuarios
                    SET contraseña_usuario = %s
                    WHERE nombre_usuario = %s """
            db.cursor.execute(sql, val)
            db.connection.commit()
       
            VentanaMensaje(app, "Exito", "Tu contraseña a sido cambiada con exito")

            return True

    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error. ¡Inténtalo más tarde!")
        print(err)
        return False

def cerrar_sesion(app, id_usuario):
    try:
        # Actualizar la fecha de salida de la sesión más reciente del usuario
        sql_actualizacion_sesion = """UPDATE Sesiones
                                      SET fecha_salida = %s
                                      WHERE ID_usuario = %s AND fecha_salida IS NULL
                                      ORDER BY fecha_acceso DESC
                                      LIMIT 1"""
        db.cursor.execute(sql_actualizacion_sesion, (datetime.now(), id_usuario))
        db.connection.commit()
    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error al cerrar sesión. ¡Inténtalo más tarde!")
        print(err)
    # finally:
    #     db.close()

def movimientos(app):
    try:
                  # seleccionar los elemtos y devolverlos
        sql=""" SELECT 
                    u.nombre_usuario,
                    DATE_FORMAT(s.fecha_acceso, '%d/%m/%Y %H:%i:%s') AS fecha_entrada,
                    DATE_FORMAT(s.fecha_salida, '%d/%m/%Y %H:%i:%s') AS fecha_salida
                FROM 
                    Sesiones s
                JOIN 
                    Usuarios u ON s.ID_usuario = u.id_usuario
                ORDER BY 
                    s.fecha_acceso DESC
                LIMIT 10;"""
        db.cursor.execute(sql)
        filas= db.cursor.fetchall()

        # Crear una lista de diccionarios para almacenar los datos
        sesiones_data = []

        # Iterar sobre las filas obtenidas de la consulta
        for fila in filas:
            sesion = {
                "usuario": fila[0],
                "fecha_entrada": fila[1],
                "fecha_salida": fila[2]
            }
            sesiones_data.append(sesion)

        return sesiones_data

    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error al devolver las sesiones. ¡Inténtalo más tarde!")
        print(err)

def get_users(app):
    try:
                  # seleccionar los elemtos y devolverlos
        sql=""" SELECT id_usuario, nombre_usuario
                FROM Usuarios
                WHERE nivel_usuario <> 'Admin';"""
        db.cursor.execute(sql)
        filas= db.cursor.fetchall()

        # Crear una lista de diccionarios para almacenar los datos
        users_data = []

        # Iterar sobre las filas obtenidas de la consulta
        for fila in filas:
            user = {
                "ID": fila[0],
                "usuario": fila[1]
            }
            users_data.append(user)

        return users_data

    except Exception as err:
        VentanaMensaje(app, "Error", "Lo sentimos, Ocurrió un error al devolver los usuarios. ¡Inténtalo más tarde!")
        print(err)

def delete_user(app, id):
    try:
            sql = "DELETE FROM Sesiones WHERE ID_usuario = %s "
            val = (id,)
            db.cursor.execute(sql, val)

            sql = "DELETE FROM Usuarios WHERE id_usuario = %s;"
            val = (id,)
            db.cursor.execute(sql, val)
            db.connection.commit()
            return True
    except Exception as err:
        VentanaMensaje(app, "Error", "Error al buscar el usuario. Por favor, verifica que el usuario exista, recarga la sección de usuarios para verificar")
        print(err)
        return False
