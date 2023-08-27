from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.db import db

from models.alimento import Alimento
from models.ar import AR
from models.comida import Comida
from models.hist_comida import HistComida
from models.persona import Persona

from routes.login import log
from routes.registro import registro
from routes.perfil import perfil
from routes.eliminar_cuenta import delUsr
from routes.inicio import inicio
from routes.update_cuenta import updtUsr
from routes.password_recovery import password

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# settings
key = os.environ['SECRETKEY']
config = os.environ['MYSQLCONFIG']

app.secret_key = key
app.config['SQLALCHEMY_DATABASE_URI'] = config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicializar la aplicacion con la base de datos
db.init_app(app)

app.register_blueprint(log)
app.register_blueprint(registro)
app.register_blueprint(perfil)
app.register_blueprint(delUsr)
app.register_blueprint(inicio)
app.register_blueprint(updtUsr)
app.register_blueprint(password)

