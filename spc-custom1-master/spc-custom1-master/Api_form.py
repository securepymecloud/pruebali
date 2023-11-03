from datetime import datetime
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import mysql.connector
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.secret_key = "TrimebutarSioRet12"  #
# Configuración de la extensión Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # Almacena la sesión en el sistema de archivos
app.config['SESSION_PERMANENT'] = False  # La sesión no es permanente

# Configura los datos de conexión a la base de datos
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


# Función para conectar a la base de datos
print("intentando conectar")  # Agrega este mensaje de depuración




# Ruta para la página "indexform.html"
@app.route("/indexform")
def indexform():
    # Si el usuario no ha iniciado sesión, redirige a la página de inicio de sesión
    if "user" not in session:
        return redirect(url_for("index1"))

    # Realiza la inserción en la base de datos
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()

            # Obtiene la fecha y hora actual
            now = datetime.now()

            # Formatea la fecha y hora como se desee, por ejemplo: 'YYYY-MM-DD HH:MM:SS'
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

            # Define la consulta SQL para insertar en la tabla logsis
            insert_query = "INSERT INTO logsis (fechaTrans) VALUES (%s)"

            # Ejecuta la consulta SQL con la fecha formateada
            cursor.execute(insert_query, (formatted_date,))
            print("Registro insertado en la tabla logsis")  # Mensaje de depuración

            # Realiza un commit para aplicar los cambios en la base de datos
            conn.commit()

            # Cierra el cursor y la conexión
            cursor.close()
            conn.close()
        except Exception as ex:
            # Maneja cualquier error que pueda ocurrir durante la inserción
            print(f"Error al insertar en la base de datos: en indexform {ex}")
    else:
        print("Error de conexión a la base de datos")

    # Renderiza la plantilla HTML "indexform.html" y pasa la información del usuario a través del contexto
    user = session["user"]
    print("este son los datos del user")
    return render_template("indexform.html", user=user, nomUsuario=user.get('preferred_username', ''))


# Ruta para verificar la conexión a la base de datos
@app.route('/verificar_conexion', methods=['GET'])
def verificar_conexion():
    conn = conectar_bd()
    if conn:
        conn.close()
        return jsonify({'mensaje': 'Conexión a la base de datos exitosa'})
    else:
        return jsonify({'mensaje': 'Error de conexión a la base de datos'}), 500


# Ruta para guardar un registro en la tabla "logsis"
@app.route('/guardar_registro', methods=['POST'])
def guardar_registro():
    conn = conectar_bd()
    if not conn:
        return jsonify({'mensaje': 'Error al guardar el registro: no se pudo conectar a la base de datos'}), 500

    try:
        cursor = conn.cursor()
        ip_usuario = request.remote_addr
        print(f'IP del usuario: {ip_usuario}')
        cursor.execute("INSERT INTO logsis (fechaTrans, ipUsuario) VALUES (NOW(), %s)", (ip_usuario,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'mensaje': 'Registro guardado correctamente'})
    except mysql.connector.Error as err:
        conn.rollback()
        conn.close()
        return jsonify({'mensaje': 'Error al guardar el registro', 'error': str(err)}), 500

##agregado nuevo michael
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
        return jsonify({'success': False, 'error': 'Error de conexión a la base de datos'}), 500

##agregado nuevo michael
@app.route('/confirmacion')
def confirmacion():
    return render_template('confirmacion.html')

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(debug=True, host='0.0.0.0', port=5002)
