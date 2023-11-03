import email
import os

import pytz
from sqlalchemy.sql.functions import user

import app
import mysql
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import msal
import mysql.connector
from datetime import datetime
from api_preguntas import get_user_data
from msal import PublicClientApplication

app = Flask(__name__)
app.secret_key = "TrimebutarSioRet12"  # Define una clave secreta para la sesión de Flask

# Configuración de Azure AD
CLIENT_ID = "b38835fb-2bbe-4f3b-89cf-dda4a0241316"  # Application (client) ID of app registration

CLIENT_SECRET = "Es-8Q~mAi7WomZ1Q0gp6kgprYsuSmfWGGrQRldft"  # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = "https://login.microsoftonline.com/7d9e7290-e637-4c97-bfe0-af56571907fd"  # For multi-tenant app
# AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

REDIRECT_PATH = "/info"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session


##codigo michael
# Función para conectar a la base de datos MySQL y retornar la conexión
def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host='database-spc.mysql.database.azure.com',
            user='adminspc',
            password='Changuaslupe5w',
            database='spc-bd'
        )
        return conn
    except Exception as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None


# Ruta para la página "indexform.html"

##codigo michael
# Crea una instancia del cliente de msal
app.config["MSAL_CLIENT"] = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY,
    client_credential="Es-8Q~mAi7WomZ1Q0gp6kgprYsuSmfWGGrQRldft",
    # Solo si la aplicación de Azure AD requiere un secreto
    token_cache=None  # No es necesario si solo estamos usando tokens de acceso
)

@app.route("/indexform")
def indexform():
##prueba persistencia
        # Si el usuario no ha iniciado sesión, redirige a la página de inicio de sesión
        if "user" not in session:
            return redirect(url_for("index"))

        # Obtiene el correo electrónico del usuario
        email = session["user"].get("preferred_username")

        # Verifica si el correo electrónico existe en la tabla formularioin
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()
                consulta = "SELECT * FROM formularioin WHERE nomUsuario = %s"
                cursor.execute(consulta, (email,))
                resultado = cursor.fetchone()

                #user session
                fecha_actual = datetime.now()

                # Asigna la fecha actual a la variable de sesión
                session['fechasesion'] = fecha_actual
                #user session fecha


                if resultado:
                    # El usuario ya ha llenado el formulario, redirige a vista nueva
                    return redirect(url_for("exist"))

            except Exception as ex:
                print(f"Error al consultar la base de datos: {ex}")

            finally:
                cursor.close()
                conn.close()

        # Renderiza la plantilla HTML "indexform.html" y pasa la información del usuario a través del contexto
        user = session["user"]
        return render_template("indexform.html", user=user)
##persistencia




# Ruta para la página de inicio de sesión personalizada
@app.route("/")
def index():
    # Si el usuario ya ha iniciado sesión, redirige a la página de bienvenida
    if "user" in session:
        return redirect(url_for("indexform"))

    # Renderiza la plantilla HTML de inicio de sesión y pasa la URL de inicio de sesión a través del contexto
    auth_url = app.config["MSAL_CLIENT"].get_authorization_request_url(
        SCOPE, redirect_uri=url_for("get_token", _external=True)
    )
    return render_template("index1.html", auth_url=auth_url)


# Ruta para iniciar el flujo de autenticación de Azure AD
@app.route("/login", methods=["GET"])
def login():
    # Redirige al inicio de sesión de Azure AD
    auth_url = app.config["MSAL_CLIENT"].get_authorization_request_url(
        SCOPE, redirect_uri=url_for("get_token", _external=True), prompt="login"
    )
    return redirect(auth_url)


# Ruta para obtener el token de acceso después del inicio de sesión exitoso
@app.route(REDIRECT_PATH)
def get_token():
    try:
        result = app.config["MSAL_CLIENT"].acquire_token_by_authorization_code(
            request.args["code"],
            scopes=SCOPE,
            redirect_uri=url_for("get_token", _external=True)
        )

        access_token = result.get("access_token")

        user = result.get("id_token_claims")

        session["user"] = user
        email = user["preferred_username"]
        print("este es el user", user)
        # Inserción de la fecha en la base de datos
        conn = conectar_bd()
        ##new michael. traigo datos de la funcion getdatauser
        ##new michael. traigo datos de la funcion getdatauser
        # Conecta a la base de datos
        user = session.get('user')
        get_user_data()
        # Accede a los datos del usuario almacenados en la variable global
        id_formulario =  session['id_formulario']
        ##new michael

        print("la pyme",id_formulario)
        ##new michael

        if conn:
            try:
                cursor = conn.cursor()

                now = datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

                ip_usuario = request.remote_addr
                print(f'IP del usuario: {ip_usuario}')
                print(f'IDPYME en APP.py: {id_formulario}')

                # Consulta SQL para insertar la fecha de inicio de sesión en la tabla logsis
                insert_query = "INSERT INTO logsis (fechaLogin, ipUsuario,idPyme) VALUES (NOW(), %s, %s)"
                cursor.execute(insert_query, (ip_usuario,id_formulario))

                # Consulta SQL para insertar el email del usuario en la tabla usuario
                insert_user_query = "INSERT INTO usuario (emailUsuario) VALUES (%s)"
                cursor.execute(insert_user_query, (
                user["preferred_username"],))  # Reemplaza 'user["preferred_username"]' con el valor correcto

                print("Fecha de inicio de sesión registrada en la tabla logsis--->", now)

                ##nuevafuncion
                # michael

                id_formulario = session['id_formulario']
                select_query_fecha = "SELECT MAX(fechaLogout) FROM logsis WHERE idPyme = %s"
                cursor.execute(select_query_fecha, (id_formulario,))
                user_fecha_tuple = cursor.fetchone()  # Obtiene una fila de datos como tupla

                if user_fecha_tuple and user_fecha_tuple[0] is not None:
                    fecha_resultante = user_fecha_tuple[0]  # Obtiene el valor de la tupla
                    utc_tz = pytz.timezone('UTC')
                    fecha_utc = fecha_resultante.astimezone(utc_tz)
                    fecha_sin_offset = fecha_resultante.replace(tzinfo=None)
                    fecha_formateada = fecha_sin_offset.strftime('%Y-%m-%d %H:%M:%S')
                    session['fechasesion'] = fecha_formateada
                    session['fechasesion1'] = fecha_formateada
                    print("fecha del último acceso:", fecha_formateada)  # Agrega esta línea para depurar
                else:
                    print("No se encontraron datos de fecha del último acceso.")





                    # michael

                ##nuevafuncion


                conn.commit()

                cursor.close()
                conn.close()
            except Exception as ex:
                print(f"Error al insertar en la base de datos: {ex}")
        else:
            print("Error de conexión a la base de datos")

        return redirect(url_for("indexform"))
    except Exception as ex:
        ##return f"Error al obtener el token de acceso1: {ex}"
        return redirect(url_for("indexform"))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    if 'user' in session and isinstance(session['user'], dict):
        # Obtiene el ID del usuario de la sesión actual

        user_id = session['user']


        get_user_data()
        # Accede a los datos del usuario almacenados en la variable global
        id_formulario = session['id_formulario']
        ip_usuario = request.remote_addr
        ##new michael


        # Conecta a la base de datos
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()

                # Consulta SQL para insertar la fecha de cierre de sesión en la tabla logsis
                insert_logout_query = "INSERT INTO logsis (ipUsuario,fechaLogout,idPyme) VALUES (%s,NOW(),%s)"
                cursor.execute(insert_logout_query,(ip_usuario, id_formulario))

                conn.commit()
                cursor.close()
                conn.close()

                print("Fecha de cierre de sesión registrada en la tabla logsis")

            except mysql.connector.Error as err:
                conn.rollback()
                conn.close()
                print("Error al registrar la fecha de cierre de sesión:", str(err))

        # Elimina todos los datos de la sesión
        session.clear()

        # Redirige al usuario a la página de inicio o a donde necesites después de cerrar sesión.
        return redirect('http://ec2-54-242-76-154.compute-1.amazonaws.com:5000')  # Cambia la URL de redirección según tu aplicación

    # Si el usuario no ha iniciado sesión, simplemente redirige a la página de inicio.
    return redirect('http://ec2-54-242-76-154.compute-1.amazonaws.com:5000')  # Cambia la URL de redirección según tu aplicación


# Agrega esta ruta para redirigir al usuario a Api_form.py después del inicio de sesión
@app.route("/api_form")
def api_form():
    # Aquí puedes realizar cualquier lógica que necesites antes de redirigir al usuario a Api_form.py
    # Por ejemplo, puedes verificar permisos, autenticación, etc.

    # Redirige al usuario a Api_form.py (asegúrate de que la URL coincida con la dirección donde se ejecuta Api_form.py)
    return redirect("http://ec2-54-242-76-154.compute-1.amazonaws.com:5002")  # Cambia la URL según sea necesario


@app.route("/exist")
def exist():
    # Aquí puedes realizar cualquier lógica que necesites antes de redirigir al usuario a Api_form.py
    # Por ejemplo, puedes verificar permisos, autenticación, etc.

    # Redirige al usuario a Api_form.py (asegúrate de que la URL coincida con la dirección donde se ejecuta Api_form.py)
   # return render_template('storage.html')
    return redirect("http://ec2-54-242-76-154.compute-1.amazonaws.com:5001/get_user_data")
# Ruta para obtener los datos del usuario
@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    # Realiza la consulta a la base de datos para obtener los datos del usuario
    email = session["user"].get("preferred_username")

    print("email:", email)  # Agrega esta línea para depurar
    conn = conectar_bd()  # Asegúrate de tener esta función definida
    if conn:

        try:
            cursor = conn.cursor()
            # Suponiendo que nomUsuario es el identificador del usuario
            nomUsuario = email  # Usamos el valor de email como nomUsuario
            select_query = "SELECT * FROM formularioin WHERE nomUsuario = %s"
            cursor.execute(select_query, (nomUsuario,))
            user_data = cursor.fetchone()  # Obtiene una fila de datos
            print("user_data1:", user_data)  # Agrega esta línea para depurar


            # Verifica si se encontraron datos en la consulta
            if user_data is not None:
                # Convierte los datos en un diccionario para facilitar la serialización
                user_data_dict = {
                    "idFormularioin": user_data[0],  # Reemplaza con los nombres reales de las columnas
                    "nomPyme": user_data[1],
                    "telefono": user_data[2],
                    "sector": user_data[3],
                    "estadoActual": user_data[4],
                    "numEmpleados" : user_data[5],
                    "cargo": user_data[9],
                    "tipoInfra":user_data[10],
                    # Agrega más campos según sea necesario
                }
                session['id_formulario'] = user_data_dict['idFormularioin']
                print('idpyme en appsd', user_data_dict['idFormularioin'])
                ##session['fechasesion']


                conn.commit()
                cursor.close()
                conn.close()



               ## return jsonify(user_data_dict)
                return render_template("storage.html", user_data_dict=user_data_dict)
                ##return redirect("http://ec2-54-242-76-154.compute-1.amazonaws.com:5001/get_user_data")
            else:
                # Si no se encontraron datos, puedes devolver un mensaje o un valor por defecto
                return jsonify({"message": "No se encontraron datos para el usuario."})
        except Exception as ex:
            print(f"Error al obtener los datos del usuario: {ex}")
            ##return redirect("http://ec2-54-242-76-154.compute-1.amazonaws.com:5001/get_user_data")
    else:
        return jsonify({"error": "Error de conexión a la base de datos."})

# Ruta para el cuestionario
@app.route("/cuestionario")
def cuestionario():
    # Verifica si el usuario ha iniciado sesión
    if "user" in session:
        # El usuario está autenticado, redirige a la API de preguntas
        # return redirect(os.GetEnv("SERVER_URL") + "/api/preguntas")
        return redirect("http://ec2-54-242-76-154.compute-1.amazonaws.com:5003/api/preguntas")
    else:
        # Si el usuario no ha iniciado sesión, redirige al inicio de sesión
        return redirect("/")
def verificar_sesion():
    try:
        # Verifica si el usuario ha iniciado sesión
        if "user" in session:
            # El usuario ha iniciado sesión y la sesión está activa
            user_data = session["user"]
            return jsonify({"status": "sesion_activa", "user_data": user_data})
        else:
            # El usuario no ha iniciado sesión o la sesión ha caducado
            return jsonify({"status": "sin_sesion"})
    except Exception as ex:
        return jsonify({"error": f"Error al verificar la sesión: {ex}"})


if __name__ == "__main__":
    # app.run(debug=True)
    # app.run(port=5000)
    app.run(debug=True, host='0.0.0.0', port=5001)
