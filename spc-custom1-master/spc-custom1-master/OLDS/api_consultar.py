from flask import Flask, render_template, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
##CORS(app)

CORS(app, resources={r"/*": {"origins": "http://ec2-54-242-76-154.compute-1.amazonaws.com"}})


@app.route('/')
def inicio():
    return render_template('index1.html')



@app.route('/consultar', methods=['GET'])
def consultar_info():
    try:
        # Conexión a la base de datos SQLite
        conn = sqlite3.connect('datos.db')
        cursor = conn.cursor()

        # Consultar los datos en la tabla
        cursor.execute('''SELECT nombre, apellido FROM usuarios''')
        rows = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        # Crear una lista de diccionarios con los datos
        info = [{'nombre': row[0], 'apellido': row[1]} for row in rows]

        return render_template('info.html', info=info)
    except sqlite3.Error as e:
        return jsonify({'message': f'Error al consultar la información: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5001)