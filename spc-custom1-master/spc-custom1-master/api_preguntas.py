from datetime import datetime
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import mysql.connector
from flask_cors import CORS
from msal import PublicClientApplication
from sqlalchemy.orm import Session

import app
from flask import Flask, session


app = Flask(__name__)
CORS(app)
app.secret_key = "TrimebutarSioRet12"  #
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
# Configurar la cookie de sesión con SameSite=None
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
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



##traer get data
@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    # Realiza la consulta a la base de datos para obtener los datos del usuario
    email = session["user"].get("preferred_username")
    global user_data_dict
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
            print("user_data:", user_data)  # Agrega esta línea para depurar


            # Verifica si se encontraron datos en la consulta
            if user_data is not None:
                # Convierte los datos en un diccionario para facilitar la serialización
                user_data_dict = {
                    "idFormularioin": user_data[0],  # Reemplaza con los nombres reales de las columnas
                    "nomPyme": user_data[1],
                    "telefono": user_data[2],
                    "estadoActual": user_data[4],
                    "cargo": user_data[9],
                    "tipoInfra":user_data[10],
                    # Agrega más campos según sea necesario
                }
                session['id_formulario'] = user_data_dict['idFormularioin']
                print('idpyme', user_data_dict['idFormularioin'])
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
            return jsonify({"error": "Error al obtener los datos del usuario."})
    else:
        return jsonify({"error": "Error de conexión a la base de datos."})
##traer get data


##api de preguntas
# Ruta de la API para obtener preguntas
@app.route('/api/preguntas', methods=['GET'])
def obtener_preguntas():
        # Realiza la consulta a la base de datos para obtener los datos del usuario
        email = session["user"].get("preferred_username")

        ##print("email:", email)  # Agrega esta línea para depurar

        # Conecta a la base de datos
        user = session.get('user')

        conn = conectar_bd()

        if conn is None:
            return jsonify({"error": "Error de conexión a la base de datos"}), 500

        cursor = conn.cursor(dictionary=True)

        ##new michael. traigo datos de la funcion getdatauser
        get_user_data()

        #nuevo michael
        respuestas_sesion = session.get('respuestas', {})

        #nuevo michael


        # Accede a los datos del usuario almacenados en la variable global
        if user_data_dict:
            id_formulario = user_data_dict["idFormularioin"]
            session['id_formulario'] = user_data_dict['idFormularioin']
            ##session['estadoActual'] = user_data_dict['estadoActual']
            ##print('idpyme', user_data_dict['idFormularioin'])
            # Realiza otras operaciones con los datos del usuario

        ##new michael
        estado_actual = user_data_dict["estadoActual"]
        tipo_infra = user_data_dict["tipoInfra"]
        print("entre a este tipo_infra en ", tipo_infra)

        # Consulta las preguntas de la base de datos
        try:

            if 'estadoActual' in user_data_dict and 'tipoInfra' in user_data_dict:
                estado_actual = user_data_dict['estadoActual']
                tipo_infra = user_data_dict['tipoInfra']
                print("Entre a este if con estado en", estado_actual, "y tipo_infra en", tipo_infra)

            # Consulta las preguntas de la base de datos junto con sus respuestas
            if estado_actual == 1 and tipo_infra == '1':
                cursor.execute("""
                    SELECT DISTINCT 
                    preguntariesgo.idPreguntaRiesgo, 
                    preguntariesgo.preguntaRiesgo, 
                    COALESCE(respuestariesgo.respuestaRiesgo, registroriesgo.RespuestaR) AS respuestaRiesgo, -- Aquí seleccionamos la respuesta del usuario si existe
                    respuestariesgo.idRespuestaRiesgo
                FROM preguntariesgo 
                LEFT JOIN respuestariesgo ON preguntariesgo.idPreguntaRiesgo = respuestariesgo.codRespuestaR
                LEFT JOIN registroriesgo ON preguntariesgo.idPreguntaRiesgo = registroriesgo.codPreguntaR AND registroriesgo.idPyme = %s -- Unimos con registroriesgo para obtener respuestas del usuario
                JOIN formularioin ON formularioin.estadoActual = 1 -- Este JOIN parece estar redundante, porque el WHERE cláusula ya tiene esta condición
                WHERE (formularioin.estadoActual = 1 AND formularioin.tipoInfra = 1 AND preguntariesgo.codPreguntaR = 1);
                """, (id_formulario,))

            elif estado_actual == 1 and tipo_infra == '2':
                cursor.execute("""
                    SELECT DISTINCT 
                    preguntariesgo.idPreguntaRiesgo, 
                    preguntariesgo.preguntaRiesgo, 
                    COALESCE(respuestariesgo.respuestaRiesgo, registroriesgo.RespuestaR) AS respuestaRiesgo, -- Aquí seleccionamos la respuesta del usuario si existe
                    respuestariesgo.idRespuestaRiesgo
                FROM preguntariesgo 
                LEFT JOIN respuestariesgo ON preguntariesgo.idPreguntaRiesgo = respuestariesgo.codRespuestaR
                LEFT JOIN registroriesgo ON preguntariesgo.idPreguntaRiesgo = registroriesgo.codPreguntaR AND registroriesgo.idPyme = %s -- Unimos con registroriesgo para obtener respuestas del usuario
                JOIN formularioin ON formularioin.estadoActual = 1 -- Este JOIN parece estar redundante, porque el WHERE cláusula ya tiene esta condición
                WHERE (formularioin.estadoActual = 1 AND formularioin.tipoInfra = 2 AND (preguntariesgo.codPreguntaR = 1 OR preguntariesgo.codPreguntaR = 2));
                                """, (id_formulario,))

            elif estado_actual == 2 and tipo_infra == '1':
                cursor.execute("""
                        SELECT DISTINCT 
                    preguntaseguridad.idPreguntaSeguridad, 
                    preguntaseguridad.preguntaSeguridad, 
                    COALESCE(respuestaseguridad.respuestaSeguridad, registroseguridad.RespuestaS) AS respuestaSeguridad, -- Aquí seleccionamos la respuesta del usuario si existe
                    respuestaseguridad.idRespuestaSeguridad
                FROM preguntaseguridad 
                LEFT JOIN respuestaseguridad ON preguntaseguridad.idPreguntaSeguridad = respuestaseguridad.codRespuestaS
                LEFT JOIN registroseguridad ON preguntaseguridad.idPreguntaSeguridad = registroseguridad.codPreguntasS AND registroseguridad.idPyme = %s -- Unimos con registroriesgo para obtener respuestas del usuario
                JOIN formularioin ON formularioin.estadoActual = 2 -- Este JOIN parece estar redundante, porque el WHERE cláusula ya tiene esta condición
                WHERE (formularioin.estadoActual = 2 AND formularioin.tipoInfra = 1 AND preguntaseguridad.codPreguntaS = 1);
                                    """, (id_formulario,))

            elif estado_actual == 2 and tipo_infra == '2':
                cursor.execute("""
                SELECT DISTINCT 
                preguntaseguridad.idPreguntaSeguridad, 
                preguntaseguridad.preguntaSeguridad, 
                COALESCE(respuestaseguridad.respuestaSeguridad, registroseguridad.RespuestaS) AS respuestaSeguridad, -- Aquí seleccionamos la respuesta del usuario si existe
                respuestaseguridad.idRespuestaSeguridad
            FROM preguntaseguridad 
            LEFT JOIN respuestaseguridad ON preguntaseguridad.idPreguntaSeguridad = respuestaseguridad.codRespuestaS
            LEFT JOIN registroseguridad ON preguntaseguridad.idPreguntaSeguridad = registroseguridad.codPreguntasS AND registroseguridad.idPyme = %s -- Unimos con registroriesgo para obtener respuestas del usuario
            JOIN formularioin ON formularioin.estadoActual = 2 -- Este JOIN parece estar redundante, porque el WHERE cláusula ya tiene esta condición
            WHERE (formularioin.estadoActual = 2 AND formularioin.tipoInfra = 2 AND (preguntaseguridad.codPreguntaS = 1 OR preguntaseguridad.codPreguntaS = 2));
            """, (id_formulario,))

            preguntas_con_respuestas = cursor.fetchall()

            # Resto del código para organizar las preguntas y respuestas en un diccionario
            preguntas_y_respuestas = {}
            id_respuestas = []  # Nueva lista para almacenar los id_respuesta

            for fila in preguntas_con_respuestas:
                if estado_actual == 1 :
                    id_pregunta = fila['idPreguntaRiesgo']
                    pregunta = fila['preguntaRiesgo']
                    respuesta = fila['respuestaRiesgo']
                    id_respuesta = fila['idRespuestaRiesgo']  # Agrega esta línea

                elif estado_actual == 2 :
                    id_pregunta = fila['idPreguntaSeguridad']  # Agregar esta línea
                    pregunta = fila['preguntaSeguridad']
                    respuesta = fila['respuestaSeguridad']
                    id_respuesta = fila['idRespuestaSeguridad']  # Agrega esta línea

                    # Agregar id_respuesta a la lista
                    id_respuestas.append(id_respuesta)

                if id_pregunta not in preguntas_y_respuestas:
                    if estado_actual == 1 and tipo_infra == '1' or tipo_infra == '2':
                        preguntas_y_respuestas[id_pregunta] = {'pregunta': pregunta, 'respuestas': []}
                        print("entreal estado 1")

                    elif estado_actual == 2 and tipo_infra == '1' or tipo_infra == '2':
                        preguntas_y_respuestas[id_pregunta] = {'pregunta': pregunta, 'respuestas': []}  # Modificar esta línea
                        print("entreal estado 2")

                if respuesta:
                    preguntas_y_respuestas[id_pregunta]['respuestas'].append(
                        {'respuesta': respuesta, 'id_respuesta': id_respuesta})

            ##aca traifo preguntas y respuestas de seguridad




            # Mover el return fuera del bucle for
            return render_template('preguntas.html', preguntas_y_respuestas=preguntas_y_respuestas,estado_actual=estado_actual)
            print("este es el idrespuesta:", id_respuesta)

        except Exception as e:
            print(f"Error al obtener preguntas: {e}")
            return jsonify({"error": "Error al obtener preguntas"}), 500

        finally:
            cursor.close()
            conn.close()




def guardar_respuesta_en_sesion(id_pregunta, respuesta):
    # Obtener las respuestas actuales de la sesión o un diccionario vacío si no existen
    respuestas_sesion = session.get('respuestas', {})
    respuestas_sesion[id_pregunta] = respuesta
    session['respuestas'] = respuestas_sesion




##api de preguntas

@app.route('/api/respuesta', methods=['POST'])
def guardar_respuesta():
    try:

        ##new michael. traigo datos de la funcion getdatauser
        get_user_data()

        # Accede a los datos del usuario almacenados en la variable global
        if user_data_dict:
            id_formulario = user_data_dict["idFormularioin"]
            session['id_formulario'] = user_data_dict['idFormularioin']
            ##print('idpyme', user_data_dict['idFormularioin'])
            # Realiza otras operaciones con los datos del usuario

        ##new michael
        estado_actual = user_data_dict["estadoActual"]
        tipo_infra = user_data_dict["tipoInfra"]
        ##print("entre a este tipo_infra en ", tipo_infra)






        # Obtener los datos enviados en la solicitud POST
        id_pregunta = request.form.get('id_pregunta')
        respuesta = request.form.get('respuesta')
        id_respuesta = request.form.get('id_respuesta')
        id_formulario = session.get('id_formulario')
        id_respuesta2= id_respuesta

        guardar_respuesta_en_sesion(id_pregunta, respuesta)

        # Agregar impresiones para ver los datos
        print(f'ID Pregunta: {id_pregunta}')
        print(f'Respuesta: {respuesta}')
        print(f'ID Respuesta: {id_respuesta}')
        print(f'ID pyme: {id_formulario}')
        print(f'ID del estado:{estado_actual}')

        # Conecta a la base de datos
        conn = conectar_bd()
        if conn is None:
            return jsonify({"error": "Error de conexión a la base de datos"}), 500

        cursor = conn.cursor()
        if estado_actual == 1:
            # Verificar si ya existe una respuesta para esta pregunta y formulario
            cursor.execute("SELECT codRespuestaR FROM registroriesgo WHERE codPreguntaR = %s AND idPyme = %s", (id_pregunta, id_formulario))
            existing_response = cursor.fetchone()

            if existing_response:
                # Si existe, actualiza la respuesta
                cursor.execute("UPDATE registroriesgo SET RespuestaR = %s, codRespuestaR = %s, codDiagnosticoriesgo=%s WHERE codRespuestaR = %s", (respuesta, id_respuesta,id_respuesta2,existing_response[0]))
                ##print(f"Valores a enviar en el UPDATE: Respuesta = {respuesta}, id_respuesta = {id_respuesta}")
            else:
                # Si no existe, inserta una nueva respuesta
                cursor.execute("INSERT INTO registroriesgo (codPreguntaR, RespuestaR, codRespuestaR, codDiagnosticoriesgo,  idPyme) VALUES (%s, %s, %s, %s, %s)", (id_pregunta, respuesta, id_respuesta, id_respuesta2,  id_formulario))
##michael

        if estado_actual == 2:
            # Verificar si ya existe una respuesta para esta pregunta y formulario en seguridad
            cursor.execute("SELECT codRespuestasS FROM registroseguridad WHERE codPreguntasS = %s AND idPyme = %s",
                           (id_pregunta, id_formulario))
            existing_response = cursor.fetchone()

            if existing_response:
                # Si existe, actualiza la respuesta
                cursor.execute("UPDATE registroseguridad SET RespuestaS = %s,codRespuestasS=%s,codDiagnosticoSeguridad=%s WHERE codRespuestasS = %s",
                               (respuesta,id_respuesta,id_respuesta2 ,existing_response[0]))
            else:
                # Si no existe, inserta una nueva respuesta
                cursor.execute(
                    "INSERT INTO registroseguridad (codPreguntasS, RespuestaS, codRespuestasS,codDiagnosticoseg, idPyme) VALUES (%s, %s, %s, %s, %s)",
                    (id_pregunta, respuesta, id_respuesta,id_respuesta2, id_formulario))
##michael

        #cosas nuevas
            # Después de guardar la respuesta en la base de datos:
                # Actualizar el progreso del cuestionario (por ejemplo, si cada pregunta es 10% del total)
                progreso_actual = session.get('progresoCuestionario', 0)
                progreso_actualizado = progreso_actual + 10
                session['progresoCuestionario'] = progreso_actualizado


        #cosas nuevas

        # Guardar los cambios en la base de datos
        conn.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()

        # Devolver una respuesta de éxito
        return jsonify({"message": "Respuesta guardada con éxito"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    if 'user' in session and isinstance(session['user'], dict):
        # Obtiene el ID del usuario de la sesión actual
        user_id = session['user']

        # Conecta a la base de datos
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()

                # Consulta SQL para insertar la fecha de cierre de sesión en la tabla logsis
                insert_logout_query = "INSERT INTO logsis (fechaLogout) VALUES (NOW())"
                cursor.execute(insert_logout_query)

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





if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(debug=True, host='0.0.0.0', port=5003) ##parametros de conexion
