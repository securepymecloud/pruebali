import sys
import os  # Importa el módulo os

# Establece las variables de entorno aquí
os.environ['DB_HOST'] = 'Michaelgomezs.mysql.pythonanywhere-services.com'
os.environ['DB_USER'] = 'Michaelgomezs'
os.environ['DB_PASSWORD'] = 'Changuaslupe5w'
os.environ['DB_NAME'] = 'Michaelgomezs$spc'
os.environ['MSAL_CLIENT_CREDENTIAL'] = 'Es-8Q~mAi7WomZ1Q0gp6kgprYsuSmfWGGrQRldft'

# add your project directory to the sys.path
project_home = u'/home/Michaelgomezs/spc-custom'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from app import app as application  # noqa