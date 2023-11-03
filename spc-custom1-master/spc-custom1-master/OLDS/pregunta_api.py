from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)


@app.route('/consulta')
def consulta():
    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host='database-spc.mysql.database.azure.com',
        user='adminspc',
        password='Changuaslupe5w',
        database='spc-bd'
    )
    cursor = conn.cursor()

    # Consulta a la base de datos
    query = 'SELECT * FROM logsis'
    cursor.execute(query)
    results = cursor.fetchall()

    # Cerrar conexión
    cursor.close()
    conn.close()

    # Devolver resultados en formato JSON
    return jsonify(results)


if __name__ == '__main__':
    app.run()