from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Ruta para la URL raíz ("/")
@app.route('/', methods=['GET'])
def index():
    return render_template('index1.html')

# Ruta para redirigir las solicitudes a app.py
@app.route('/app', methods=['GET', 'POST'])
def app_route():
    # URL del servicio app.py
    global response
    app_url = 'http://ec2-54-242-76-154.compute-1.amazonaws.com:5001'  # Ajusta el puerto según sea necesario

    # Reenviar la solicitud al servicio app.py
    if request.method == 'GET':
        response = requests.get(f'{app_url}/api/resource')
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f'{app_url}/api/resource', json=data)

    return (response.text, response.status_code, response.headers.items())

# Ruta para redirigir las solicitudes a Api_form.py
@app.route('/api_form', methods=['GET', 'POST'])
def api_form_route():
    # URL del servicio Api_form.py
    api_form_url = 'http://ec2-54-242-76-154.compute-1.amazonaws.com:5002'  # Ajusta el puerto según sea necesario

    # Reenviar la solicitud al servicio Api_form.py
    if request.method == 'GET':
        response = requests.get(f'{api_form_url}/api/form')
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f'{api_form_url}/api/form', json=data)

    return (response.text, response.status_code, response.headers.items())

# Ruta para redirigir las solicitudes a api_preguntas.py
@app.route('/api_preguntas', methods=['GET', 'POST'])
def api_preguntas_route():
    # URL del servicio api_preguntas.py
    api_preguntas_url = 'http://ec2-54-242-76-154.compute-1.amazonaws.com:5003'  # Ajusta el puerto según sea necesario

    # Reenviar la solicitud a api_preguntas.py
    if request.method == 'GET':
        response = requests.get(f'{api_preguntas_url}/api/preguntas')
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f'{api_preguntas_url}/api/preguntas', json=data)

    return (response.text, response.status_code, response.headers.items())

@app.route('/api_respuestas', methods=['GET', 'POST'])
def api_respuestas_route():
    # URL del servicio api_respuestas.py
    api_respuestas_url = 'http://ec2-54-242-76-154.compute-1.amazonaws.com:5004'  # Ajusta el puerto según sea necesario

    # Reenviar la solicitud a api_respuestas.py
    if request.method == 'GET':
        response = requests.get(f'{api_respuestas_url}/api/respuestas')
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f'{api_respuestas_url}/api/respuestas', json=data)

    return (response.text, response.status_code, response.headers.items())

##mi nueva api de reporte
# Ruta para redirigir las solicitudes a la nueva API en el puerto 5005
@app.route('/reporte', methods=['GET', 'POST'])
def reporte_route():
    # URL de la nueva API en el puerto 5005
    reporte_url = 'http://ec2-54-242-76-154.compute-1.amazonaws.com:5005'  # Ajusta el puerto según sea necesario

    # Reenviar la solicitud a la nueva API
    if request.method == 'GET':
        response = requests.get(f'{reporte_url}/api/reporte')
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f'{reporte_url}/api/reporte', json=data)

    return (response.text, response.status_code, response.headers.items())

##mi nueva api de reporte
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)