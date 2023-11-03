import email
import os
from reportlab.platypus import Image
import pytz
from fpdf import FPDF  # Importa la biblioteca fpdf2
from sqlalchemy.sql.functions import user
from reportlab.lib.pagesizes import letter, A4, landscape, portrait, A6, A8, A2, A3
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from io import BytesIO
from reportlab.lib.pagesizes import landscape
import app
import mysql
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, send_from_directory
import msal
import mysql.connector
from datetime import datetime
from api_preguntas import get_user_data, guardar_respuesta, obtener_preguntas
from api_reporte import get_user_data, ejecutar_consulta_sql, generar_pdf, descargar_pdf, guardar_informe_en_bd
from api_respuestas import obtener_respuestas
from msal import PublicClientApplication
from api_reporte import guardar_informe_en_bd
import api_preguntas
import api_reporte
import api_respuestas
from flask import make_response
import os


app = Flask(__name__)
app.secret_key = "TrimebutarSioRet12"  # Define una clave secreta para la sesión de Flask
app.config['STATIC_URL_PATH'] = 'static'

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
 # Asegúrate de importar el módulo os

def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME')
        )
        return conn
    except Exception as e:
        print(f"Errore de conexión a la base de datos en app.py: {e}")
        return None


# Ruta para la página "indexform.html"

##codigo michael
# Crea una instancia del cliente de msal
app.config["MSAL_CLIENT"] = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY,
    client_credential=os.environ.get('MSAL_CLIENT_CREDENTIAL'),
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
            print("Errore de conexión a la base de datos en app.py")

        return redirect(url_for("indexform"))
    except Exception as ex:
        ##return f"Error al obtener el token de acceso1: {ex}"
        return redirect(url_for("indexform"))




#trucomichael

#trucomichael








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
        return redirect('https://michaelgomezs.pythonanywhere.com')  # Cambia la URL de redirección según tu aplicación

    # Si el usuario no ha iniciado sesión, simplemente redirige a la página de inicio.
    return redirect('https://michaelgomezs.pythonanywhere.com')  # Cambia la URL de redirección según tu aplicación


# Agrega esta ruta para redirigir al usuario a Api_form.py después del inicio de sesión
@app.route("/api_form")
def api_form():
    # Aquí puedes realizar cualquier lógica que necesites antes de redirigir al usuario a Api_form.py
    # Por ejemplo, puedes verificar permisos, autenticación, etc.

    # Redirige al usuario a Api_form.py (asegúrate de que la URL coincida con la dirección donde se ejecuta Api_form.py)
    return redirect("https://michaelgomezs.pythonanywhere.com")  # Cambia la URL según sea necesario


@app.route("/exist")
def exist():
    # Aquí puedes realizar cualquier lógica que necesites antes de redirigir al usuario a Api_form.py
    # Por ejemplo, puedes verificar permisos, autenticación, etc.

    # Redirige al usuario a Api_form.py (asegúrate de que la URL coincida con la dirección donde se ejecuta Api_form.py)
   # return render_template('storage.html')
    return redirect("https://michaelgomezs.pythonanywhere.com/get_user_data")




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
                ##return redirect("https://michaelgomezs.pythonanywhere.com/get_user_data")
            else:
                # Si no se encontraron datos, puedes devolver un mensaje o un valor por defecto
                return jsonify({"message": "No se encontraron datos para el usuario."})
        except Exception as ex:
            print(f"Error al obtener los datos del usuario: {ex}")
            ##return redirect("https://michaelgomezs.pythonanywhere.com/get_user_data")
    else:
        return jsonify({"error": "Errore de conexión a la base de datos en app.py."})


##aca traifo preguntas del otro lado





#########################################################################
@app.route('/api/preguntas', methods=['GET'])
def llamar_api_preguntas():
    # Puedes llamar a la función o lógica correspondiente de api_preguntas.py aquí
    return api_preguntas.obtener_preguntas()




@app.route('/api/reporte', methods=['GET'])
def llamar_api_reporte():
    # Puedes llamar a la función o lógica correspondiente de api_reporte.py aquí
    return api_reporte.obtener_reporte()


@app.route('/api/respuesta', methods=['POST'])
def llamar_api_respuesta():
    # Aquí puedes llamar a la función guardar_respuesta que ya tienes definida
    return guardar_respuesta()



# Ruta para procesar el formulario y guardar los datos en la base de datos
@app.route('/guardar_datos', methods=['POST'])
def guardar_datos():


    # Obtén los datos enviados por el formulario
    data = request.form

    # Convierte los datos en variables individuales
    nomPyme = data['nomPyme']
    telefono = data['telefono']
    sector = data['sector']
    estadoActual = data['estadoActual']
    numEmpleados = int(data['numEmpleados'])  # Convierte a entero
    nomUsuario = data['nomUsuario']
    cargo = data['cargo']
    terminosCond = 1 if 'terminosCond' in data else 0
    terminosDatos = 1 if 'terminosDatos' in data else 0
    tipoInfra = data['tipoInfra']

    print("el nom usuario es",nomUsuario)
    # Log del query SQL
    ##print("Query SQL:", nomPyme, telefono, sector, estadoActual, numEmpleados, nomUsuario, cargo, terminosCond,
          ##terminosDatos)

    # Realiza la inserción en la base de datos
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()

            # Define la consulta SQL para insertar en la tabla correspondiente
            insert_query = """
            INSERT INTO formularioin (nomPyme, telefono, sector, estadoActual, numEmpleados, nomUsuario, cargo, terminosCond, terminosDatos,tipoInfra)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            ##print("Query SQL:", insert_query)  # Agrega esta línea
            cursor.execute(insert_query, (nomPyme, telefono, sector, estadoActual, numEmpleados, nomUsuario, cargo, terminosCond, terminosDatos, tipoInfra))

            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('confirmacion'))
            ##return jsonify({'success': True})
        except Exception as ex:
            print(f"Error al insertar en la base de datos: {ex}")
            return jsonify({'success': False, 'error': str(ex)})
    else:
        return jsonify({'success': False, 'error': 'Error de conexión a la base de datos en apiform'}), 500




##agregado nuevo michael
@app.route('/confirmacion')
def confirmacion():
    return render_template('confirmacion.html')












@app.route('/api/reporte/descargar_pdf', methods=['GET'])
def descargar_pdf():

    base_path = os.path.dirname(os.path.abspath(__file__))
    logo_path = "/home/Michaelgomezs/spc-custom/static/logo.png"
    print("mi ruta de la foto",logo_path)
    # Obtén el valor de id_formulario de la sesión
    id_formulario = session.get('id_formulario')

    # Verifica si id_formulario es None o no está definido en la sesión
    if id_formulario is not None:
        # Llama a ejecutar_consulta_sql() con id_formulario como argumento
        resultados = ejecutar_consulta_sql(id_formulario)

        pdf_data = generar_pdf(resultados)
        # Guarda el informe en la base de datos
        guardar_informe_en_bd(id_formulario, pdf_data)

        # Genera el PDF y configura la respuesta
        response = make_response(generar_pdf(resultados))
        response.headers['Content-Disposition'] = 'attachment; filename=informe.pdf'
        return response
    else:
        # Maneja el caso en el que id_formulario no está definido en la sesión
        return jsonify({"error": "id_formulario no encontrado en la sesión"})







@app.route('/home/Michaelgomezs/spc-custom/static/logo.png')
def serve_static_logo():
    return send_from_directory('static', 'logo.png')


############################################################################################


# Ruta para el cuestionario
@app.route("/cuestionario" )
def cuestionario():
    # Verifica si el usuario ha iniciado sesión
    # Verifica si el usuario ha iniciado sesión
      if "user" in session:
        # Hacer una solicitud a la API en api_preguntas.py
        api_url = "https://michaelgomezs.pythonanywhere.com/"  # Reemplaza con la URL de tu API
        response = requests.get(api_url)

        if response.status_code == 200:
            # Si la solicitud es exitosa, obtén los datos de la respuesta JSON
            preguntas_y_respuestas = response.json()
            return render_template("preguntas.html", preguntas_y_respuestas=preguntas_y_respuestas)
        else:
            # Si la solicitud no es exitosa, maneja el error apropiadamente
            return "Error al obtener los datos de la API", 500

      else:
        # Si el usuario no ha iniciado sesión, redirige al inicio de sesión
        return redirect("/")

#######################################################################

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
       app.run(debug=True, host='0.0.0.0')