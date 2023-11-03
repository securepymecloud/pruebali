from urllib import request
from flask import Flask, session
from flask import Flask, jsonify, render_template
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "TrimebutarSioRet12"  #
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

# Ruta de la API para obtener respuestas
@app.route('/api/respuestas', methods=['GET'])
def obtener_respuestas():
    # Conecta a la base de datos
    conn = conectar_bd()
    if conn is None:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)

    # Consulta las respuestas de la base de datos
    try:
        cursor.execute("SELECT respuestaRiesgo,idRespuestaRiesgo FROM respuestariesgo")
        respuestas = cursor.fetchall()



        return render_template('respuestas.html', respuestas=respuestas)
    except Exception as e:
        print(f"Error al obtener respuestas: {e}")
        return jsonify({"error": "Error al obtener respuestas"}), 500
    finally:
        cursor.close()
        conn.close()

# Ruta para guardar respuestas (método POST)




if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(debug=True, host='0.0.0.0', port=5004)  # Ajusta el puerto según sea necesario
