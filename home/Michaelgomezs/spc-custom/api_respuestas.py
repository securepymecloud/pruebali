from urllib import request
from flask import Flask, session
from flask import Flask, jsonify, render_template
import mysql.connector
from flask_cors import CORS
import os  # Importa el módulo os
app = Flask(__name__)
CORS(app)
app.secret_key = "TrimebutarSioRet12"  #
# Configura los datos de conexión a la base de datos
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

# Ruta de la API para obtener respuestas
@app.route('/api/respuestas', methods=['GET'])
def obtener_respuestas():
    # Conecta a la base de datos
    conn = conectar_bd()
    if conn is None:
        return jsonify({"error": "Error de conexión a la base de datos en respuestas"}), 500

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
    app.run(debug=True, host='0.0.0.0')  # Ajusta el puerto según sea necesario