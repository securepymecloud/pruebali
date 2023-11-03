import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('datos.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT NOT NULL,
                 apellido TEXT NOT NULL)''')

# Cerrar la conexión
cursor.close()
conn.close()