from flask import Flask, request, jsonify, render_template, redirect  # <-- Añadir 'redirect'
import requests

app = Flask(__name__)

# Ruta para la URL raíz ("/")
@app.route('/', methods=['GET'])
def index():
    return render_template('index1.html')

@app.route('/app', methods=['GET', 'POST'])
def app_route():
    # URL del servicio app.py
    app_url = 'https://michaelgomezs.pythonanywhere.com'  # Ajusta el puerto según sea necesario

    # Reenviar la solicitud al servicio app.py
    if request.method == 'GET':
        return redirect(f'{app_url}/api/resource')
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f'{app_url}/api/resource', json=data)
        return (response.text, response.status_code, response.headers.items())

##mi nueva api de reporte
# Ruta para redirigir las solicitudes a la nueva API en el puerto 5005
@app.route('/reporte', methods=['GET', 'POST'])
def reporte_route():
    # URL de la nueva API en el puerto 5005
    reporte_url = 'https://michaelgomezs.pythonanywhere.com/reporte'  # Ajusta el puerto según sea necesario

    # Reenviar la solicitud a la nueva API
    if request.method == 'GET':
        response = requests.get(f'{reporte_url}/api/reporte')
    elif request.method == 'POST':
        data = request.json
        response = requests.post(f'{reporte_url}/api/reporte', json=data)

    return (response.text, response.status_code, response.headers.items())

##mi nueva api de reporte

if __name__ == '__main__':
    app.run(debug=True)