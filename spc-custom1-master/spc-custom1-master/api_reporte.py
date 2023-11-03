from flask import Flask, render_template, make_response, redirect, url_for, jsonify, request
import mysql.connector
from datetime import datetime
from fpdf import FPDF  # Importa la biblioteca fpdf2
import requests
from flask import Flask, render_template, make_response, redirect, url_for, session
import mysql.connector
from reportlab.lib.pagesizes import letter, A4, landscape, portrait, A6, A8, A2, A3
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app import get_user_data as app_get_user_data
from io import BytesIO
from reportlab.lib.pagesizes import landscape
app = Flask(__name__)
SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session
app.secret_key = "TrimebutarSioRet12"  #



##getuserdata
@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    # Realiza la consulta a la base de datos para obtener los datos del usuario
    email = session["user"].get("preferred_username")

    print("YO SOY:",session["user"])
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
                user_data_dict["id_formulario"] = user_data[0]  # Reemplaza con la columna real que contiene el ID del formulario

                session['id_formulario'] = user_data_dict['idFormularioin']
                print('idpyme en reporte', user_data_dict['idFormularioin'])
                print('estadoactual reporte', user_data_dict['estadoActual'])
                session['estado_actual']=user_data_dict['estadoActual']


                conn.commit()
                cursor.close()
                conn.close()



                return user_data_dict
                ##return render_template("storage.html", user_data_dict=user_data_dict)
                ##return redirect("http://ec2-54-242-76-154.compute-1.amazonaws.com:5001/get_user_data")
            else:
                # Si no se encontraron datos, puedes devolver un mensaje o un valor por defecto
                return jsonify({"message": "No se encontraron datos para el usuario."})
        except Exception as ex:
            print(f"Error al obtener los datos del usuario: {ex}")
            ##return redirect("http://ec2-54-242-76-154.compute-1.amazonaws.com:5001/get_user_data")
    else:
        return jsonify({"error": "Error de conexión a la base de datos."})



##obtener estadoactual
def obtener_estado_actual(email):
    try:
        # Realiza la consulta a la base de datos para obtener los datos del usuario
        email = session["user"].get("preferred_username")
        # Conecta a la base de datos MySQL (asegúrate de tener los datos de conexión configurados)
        conn = mysql.connector.connect(
            host='database-spc.mysql.database.azure.com',
            user='adminspc',
            password='Changuaslupe5w',
            database='spc-bd'
        )

        cursor = conn.cursor()
        nomUsuario = email  # Usamos el valor de email como nomUsuario
        # Realiza la consulta SQL para obtener el ID del formulario en función del correo electrónico
        select_query = "SELECT * FROM formularioin WHERE nomUsuario = %s"
        cursor.execute(select_query, (nomUsuario,))

        # Obtiene el resultado de la consulta
        estado_actual = cursor.fetchone()

        # Cierra la conexión a la base de datos
        cursor.close()
        conn.close()

        # Si se encontró un resultado, devuelve el ID del formulario, de lo contrario, devuelve None
        return estado_actual[4] if estado_actual else None
    except Exception as ex:
        # Maneja cualquier error que pueda ocurrir al conectar a la base de datos o ejecutar la consulta
        print(f"Error al obtener el ID del formulario: {ex}")
        return None
##obtener estado actual
def obtener_id_formulario(email):
    try:
        # Realiza la consulta a la base de datos para obtener los datos del usuario
        email = session["user"].get("preferred_username")
        # Conecta a la base de datos MySQL (asegúrate de tener los datos de conexión configurados)
        conn = mysql.connector.connect(
            host='database-spc.mysql.database.azure.com',
            user='adminspc',
            password='Changuaslupe5w',
            database='spc-bd'
        )

        cursor = conn.cursor()
        nomUsuario = email  # Usamos el valor de email como nomUsuario
        # Realiza la consulta SQL para obtener el ID del formulario en función del correo electrónico
        select_query = "SELECT * FROM formularioin WHERE nomUsuario = %s"
        cursor.execute(select_query, (nomUsuario,))

        # Obtiene el resultado de la consulta
        id_formulario = cursor.fetchone()

        # Cierra la conexión a la base de datos
        cursor.close()
        conn.close()

        # Si se encontró un resultado, devuelve el ID del formulario, de lo contrario, devuelve None
        return id_formulario[0] if id_formulario else None
    except Exception as ex:
        # Maneja cualquier error que pueda ocurrir al conectar a la base de datos o ejecutar la consulta
        print(f"Error al obtener el ID del formulario: {ex}")
        return None
##traer get data
##getuserdata

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

# Función para ejecutar la consulta SQL
def ejecutar_consulta_sql(id_formulario):
    ##get_user_data()

    ##getuser añadido



    # Configura los datos de conexión a la base de datos
    # Conecta a la base de datos usando la función conectar_bd
    connection = conectar_bd()

    if connection is None:
        return []

    user = session.get('user')
    get_user_data()

    cursor = connection.cursor()
    print("mi valor de pyme en reportesz", session['id_formulario'],session['estado_actual'])
    valorestado=session['estado_actual']
    valorpyme= session['id_formulario']
    print("idformz",valorpyme)



    # Ejecuta la consulta SQL

    if valorestado == 1:
        cursor.execute("""
        SELECT DISTINCT  dr.funcionR , dr.dominioR, pr.preguntaRiesgo, rr.respuestaRiesgo, rr.codNivelR, dr.diagnosticoRiesgo, dr.codNivel 
        FROM diagnosticoriesgo1 dr
        INNER JOIN preguntariesgo pr ON dr.codDiagnosticoriesgo = pr.idPreguntaRiesgo
        INNER JOIN respuestariesgo rr ON dr.codRiesgo = rr.idRespuestaRiesgo
        INNER JOIN registroriesgo rg ON dr.idDiagnosticoRiesgo = rg.codDiagnosticoriesgo
        WHERE rg.idPyme = %s;  """, (valorpyme,))

    elif valorestado == 2:
          cursor.execute("""
            SELECT DISTINCT dr.funcionS , dr.dominioS, pr.preguntaSeguridad, rr.respuestaSeguridad, rr.codNivelS, dr.diagnosticoSeg , dr.codNivel 
            FROM diagnosticoseguridad dr
            INNER JOIN preguntaseguridad pr ON dr.codDiagnosticoseg = pr.idPreguntaSeguridad
            INNER JOIN respuestaseguridad rr ON dr.codSeg = rr.idRespuestaSeguridad
            INNER JOIN registroseguridad rg ON dr.idDiagnosticoSeg= rg.codDiagnosticoseg
            WHERE rg.idPyme = %s;  """, (valorpyme,))




    resultados = cursor.fetchall()

    # Cierra la conexión a la base de datos
    cursor.close()
    connection.close()

    return resultados

# Ruta para obtener un informe
@app.route('/api/reporte', methods=['GET'])
def obtener_reporte():
    # Realiza una solicitud HTTP a la ruta /get_user_data para obtener los datos del usuario
    user_data_dict = get_user_data()
    # Verifica si los datos del usuario se obtuvieron con éxito
    if user_data_dict:
        # Obtener el id_formulario del diccionario de datos del usuario
        id_formulario = user_data_dict.get("id_formulario")
        valorestado = session['estado_actual']
        print("Valor actual de id_formulario:", id_formulario)
        print("MI REPORTE TIENE ESTADO EN :", session['estado_actual'])
        # Ejecutar la consulta SQL para obtener los datos del informe
        resultados = ejecutar_consulta_sql(id_formulario)

        # Renderizar la plantilla HTML con los resultados
        return render_template('reporte.html', resultados=resultados, valorestado=valorestado)
    else:
        # Maneja el caso en el que no se pudieron obtener los datos del usuario
        return jsonify({"error": "Error al obtener los datos del usuario en reporte"})
# Ruta para mostrar los resultados en una tabla HTML
@app.route('/api/reporte/mostrar', methods=['GET'])
def mostrar_reporte():
    resultados = ejecutar_consulta_sql()

    # Renderiza la plantilla HTML con los resultados
    return render_template('reporte.html', resultados=resultados)

# Ruta para descargar el informe en PDF



@app.route('/api/reporte/descargar_pdf', methods=['GET'])
def descargar_pdf():
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



def guardar_informe_en_bd(id_formulario, informe_data):
    try:
        # Conecta a la base de datos
        conn = conectar_bd()
        if conn:
            cursor = conn.cursor()

            # Define la consulta SQL para insertar el informe en la tabla "reporte"
            insert_query = "INSERT INTO reporte (reporteGenerado, codReporte, descargaPdf) VALUES (%s, %s, NOW())"
            cursor.execute(insert_query, (informe_data, id_formulario))

            conn.commit()
            cursor.close()
            conn.close()

            print("Informe guardado en la tabla 'reporte'")
        else:
            print("Error de conexión a la base de datos.")
    except Exception as ex:
        print(f"Error al guardar el informe en la base de datos: {ex}")


def cambiar_orientacion(canvas, doc, col_widths=None):
    if doc.page >= 3:
        doc.pagesize = landscape(A4)
        canvas.setPageSize(landscape(A4))
        if col_widths is not None:
            table_width = sum(col_widths)
            page_width = landscape(A4)[0]
            extra_space = page_width - table_width
            left_padding = extra_space / 2
            # Aquí podrías añadir código para centrar la tabla usando left_padding
    else:
        doc.pagesize = portrait(A4)
        canvas.setPageSize(portrait(A4))

def generar_pdf(resultados):
    user_data = get_user_data()
    id_formulario = obtener_id_formulario(session["user"].get("preferred_username"))
    email = session["user"].get("preferred_username")

    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y %H:%M:%S")

    doc = SimpleDocTemplate("informe.pdf", pagesize=A4, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    elements = []


    styles = getSampleStyleSheet()
    style_normal = styles['Normal']

    # Define un estilo personalizado para el título con color azul oscuro
    style_titulo = ParagraphStyle(
        name='TituloStyle',
        parent=style_normal,
        fontSize=11,
        textColor=colors.HexColor('#000080'),  # Cambiar a azul oscuro (#000080)
        leading=24,  # Espaciado entre líneas
        alignment=1  #
    )
    # Define un estilo personalizado para los títulos de las celdas con texto más oscuro
    style_titulo_celda = ParagraphStyle(
        name='TituloCeldaStyle',
        parent=style_normal,
        textColor=colors.HexColor('#000000'),  # Cambiar a un tono más oscuro (#333333)
        alignment=1,
        bold=True
    )
    data = [[Paragraph("Función", style_titulo_celda),
    Paragraph("Dominio", style_titulo_celda),
    Paragraph("Pregunta que<br/>se realizó", style_titulo_celda),
    Paragraph("Respuesta<br/>Seleccionada", style_titulo_celda),
    Paragraph("Estado actual", style_titulo_celda),
    Paragraph("Recomendación para<br/>incrementar el nivel de madurez", style_titulo_celda),
    Paragraph("Estado al que<br/>pasarás con la recomendación", style_titulo_celda),
    ]]
    for row in resultados:
        data.append([Paragraph(str(row[0]), style_titulo_celda),
                     Paragraph(str(row[1]), style_titulo_celda),
                     Paragraph(str(row[2]), style_titulo_celda),
                     Paragraph(str(row[3]), style_titulo_celda),
                     Paragraph(str(row[4]), style_titulo_celda),
                     Paragraph(str(row[5]), style_titulo_celda),
                     Paragraph(str(row[6]), style_titulo_celda)])

        # Agrega un espacio en blanco antes de colocar el logo
    elements.append(
    Spacer(1, 1))  # Ajusta el tamaño del espacio en blanco según sea necesario (36 es aproximadamente 1 cm)

    # Agrega el logo en el documento
    logo_path = 'static/logo.png'  # Reemplaza 'logo.png' con el nombre de tu imagen de logo
    logo = Image(logo_path, width=10 * cm, height=7 * cm)  # Ajusta el tamaño del logo según tus necesidades
    elements.append(logo)

    style_info_formulario = ParagraphStyle(
        name='InfoFormularioStyle',
        parent=styles['Normal'],
        fontSize=16,  # Aumenta el tamaño de la fuente a 14 o el valor que desees
        textColor=colors.HexColor('#000080'),  # Establece el color del texto a azul
        leading=24,  # Espaciado entre líneas
        alignment=1,  # Centrado
        bold=True  # Negrilla
    )
    style_titulo1 = ParagraphStyle(
        name='TituloStyle',
        parent=style_normal,
        fontSize=10,
        textColor=colors.gray,  # Cambiar a azul oscuro (#000080)
        leading=24,  # Espaciado entre líneas
        alignment=4  #
    )

    info_titulo1 = Paragraph(f" Politica tratamiento de datos: Para efectos de dar cumplimiento a lo dispuesto en el artículo 9º de la Ley 1581 de 2012, los responsables del tratamiento de datos personales establecen mecanismos para obtener la Autorización de los titulares o de quien se encuentre legitimado en los términos de la Ley. Por lo anterior SECURE PYME CLOUD, pone a disposición los mecanismos que podrán ser predeterminados a través de medios técnicos que faciliten al titular su manifestación automatizada. La Autorización podrá otorgarse conforme a alguna de las siguientes opciones: (i) Por escrito, (ii) De forma verbal o (iii) Mediante conductas inequívocas del titular que permitan concluir de manera razonable que otorgó la autorización. En ningún caso el silencio podrá asimilarse a una conducta inequívoca. Así mismo, de conformidad a lo dispuesto en el artículo 10º del Decreto 1377 de 2013, SECURE PYME CLOUD, cumple con los establecido donde se indica que si en el término de treinta (30) días hábiles a partir de la implementación del anterior mecanismo, los titulares no contactaron al RESPONSABLE o ENCARGADO para solicitar la supresión de sus datos personales, el RESPONSABLE y ENCARGADO podrán continuar realizando el Tratamiento de los datos personales contenidos en sus bases de datos para la finalidad o finalidades previstas e indicadas en la política de tratamiento de protección de datos personales.<br/><br/><br/><br/><br/><br/>", style_titulo1)
    small_logo = Image(logo_path, width=5 * cm, height=3.5 * cm)

    info_titulo = Paragraph(f" DATOS REGISTRADOS DE LA PYME ", style_info_formulario)
    info_raya = Paragraph(f" -------------------------------------------------------- ", style_info_formulario)
    info_name = Paragraph(f"Nombre de la Pyme: {user_data['nomPyme']}", style_titulo)
    info_formulario = Paragraph(f"ID de la Pyme: {id_formulario}", style_titulo)
    info_telefono = Paragraph(f"Telefono registrado: {user_data['telefono']}", style_titulo)
    info_cargo = Paragraph(f"Cargo de la persona que consulta a nombre de la pyme: {user_data['cargo']}", style_titulo)
    info_sector = Paragraph(f"Sector de la pyme: {user_data['sector']}", style_titulo)
    info_emple = Paragraph(f"Cantidad de empleados: {user_data['numEmpleados']}", style_titulo)
    info_mail = Paragraph(f"E-mail registrado: {email}", style_titulo)
    if user_data['estadoActual'] == 1:
        info_estado = Paragraph(f"Estado Actual de la pyme: Nube", style_titulo)
    else:
        info_estado = Paragraph(f"Estado Actual de la pyme: On-Premise", style_titulo)

    if user_data['tipoInfra'] == '1':
        info_infra = Paragraph(f"La seleccion de preguntas fue realizada a Alto Nivel", style_titulo)
    else:
        info_infra = Paragraph(f"La seleccion de preguntas fue realizada a Bajo Nivel", style_titulo)

    info_fecha = Paragraph(f"Fecha y hora de generación del reporte: {formatted_date}", style_titulo)
    info_raya2 = Paragraph(f" _____________________________________________________<br/><br/><br/><br/> <br/>  ", style_info_formulario)

    elements.append(info_titulo1)
    elements.append(small_logo)
    elements.append(info_titulo)
    elements.append(info_raya)
    elements.append(info_name)
    elements.append(info_formulario)
    elements.append(info_telefono)
    elements.append(info_cargo)
    elements.append(info_sector)
    elements.append(info_emple)
    elements.append(info_mail)
    elements.append(info_estado)
    elements.append(info_infra)
    elements.append(info_fecha)
    elements.append(info_raya2)
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 12))
    elements.append(Spacer(1, 48))
    elements.append(Spacer(1, 48))
    elements.append(Spacer(1, 48))
    elements.append(Spacer(1, 48))
    elements.append(Spacer(1, 48))
    elements.append(Spacer(1, 48))
    elements.append(Spacer(1, 10))

    # Crea el título y agrega la tabla debajo
    titulo = Paragraph("<br/><br/><br/><br/>Informe con Recomendaciones", style_info_formulario)
    elements.append(Spacer(1, 12))
    elements.append(titulo)
    col_widths = [2.5 * cm, 3.5 * cm, 4.8 * cm, 4.5 * cm, 2.0 * cm, 4.8 * cm, 5.0 * cm]
    table = Table(data, colWidths=col_widths, repeatRows=1, style=[
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#000080')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),  # Cambiar el tamaño de fuente a 14 puntos
        ('BOTTOMPADDING', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (-1, -1), (0.96, 0.96, 0.96)),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
    ])
    # Si la página es mayor o igual a 3 (orientación horizontal)
    if len(elements) >= 2:
        table_width = sum(col_widths)  # Ancho total de la tabla
        page_width = landscape(A4)[0]  # Ancho total de la página en orientación horizontal
        extra_space = page_width - table_width  # Espacio sobrante
        left_padding = extra_space / 2  # Calcula el padding izquierdo para centrar la tabla
        elements.append(Spacer(left_padding, 0))  # Añade un espacio para centrar la tabla
    table.hAlign = 'LEFT'
    elements.append(table)
    elements.append(info_fecha)
    doc.build(elements,
              onFirstPage=lambda canvas, doc: cambiar_orientacion(canvas, doc, col_widths=col_widths),
              onLaterPages=lambda canvas, doc: cambiar_orientacion(canvas, doc, col_widths=col_widths))

    with open("informe.pdf", "rb") as f:
        pdf_data = f.read()
    return pdf_data


# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    if 'user' in session and isinstance(session['user'], dict):
        # Obtiene el ID del usuario de la sesión actual
        user_id = session['user']
        id_formulario = session['id_formulario']
        ip_usuario = request.remote_addr
        # Conecta a la base de datos
        conn = conectar_bd()
        if conn:
            try:
                cursor = conn.cursor()



                insert_logout_query = "INSERT INTO logsis (ipUsuario,fechaLogout,idPyme) VALUES (%s,NOW(),%s)"
                cursor.execute(insert_logout_query, (ip_usuario, id_formulario))

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
    app.run(debug=True, host='0.0.0.0', port=5005)
