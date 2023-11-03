import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('datos2.db')
cursor = conn.cursor()

## Crear la tabla FormPyme
cursor.execute('''
    CREATE TABLE IF NOT EXISTS FormPyme (
        idPyme INTEGER PRIMARY KEY,
        NamePyme VARCHAR(45) NULL,
        Telefono INTEGER(20) NULL,
        Sector VARCHAR(45) NULL,
        EstadoActual INTEGER NULL,
        NumEmployes INTEGER NULL,
        TermCond INTEGER NOT NULL
    )
''')

# Crear la tabla Preguntas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Preguntas (
        idPreguntas INTEGER PRIMARY KEY,
        Preguntas VARCHAR(250) NULL,
        EstadoActual INTEGER NULL,
        FOREIGN KEY (EstadoActual) REFERENCES FormPyme (idPyme)
    )
''')

# Crear la tabla Respuestas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Respuestas (
        idRespuestas INTEGER PRIMARY KEY,
        Respuestas VARCHAR(250) NULL,
        idPreguntas INTEGER NULL,
        FOREIGN KEY (idPreguntas) REFERENCES Preguntas (idPreguntas)
    )
''')

# Crear la tabla Diagnostico
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Diagnostico (
        idDiagnostico INTEGER PRIMARY KEY,
        idPyme INTEGER NULL,
        idPreguntas INTEGER NULL,
        idRespuestas INTEGER NULL,
        FOREIGN KEY (idPyme) REFERENCES FormPyme (idPyme),
        FOREIGN KEY (idPreguntas) REFERENCES Preguntas (idPreguntas),
        FOREIGN KEY (idRespuestas) REFERENCES Respuestas (idRespuestas)
    )
''')

# Crear la tabla logsSys
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logsSys (
        idlogsSys INTEGER PRIMARY KEY,
        idDiagnostico INTEGER NULL,
        fechaLog DATETIME NULL,
        detalle VARCHAR(300) NULL,
        FOREIGN KEY (idDiagnostico) REFERENCES Diagnostico (idDiagnostico)
    )
''')

# Cerrar la conexión
cursor.close()
conn.close()