from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.db import db

from models.alimento import Alimento
from models.ar import AR
from models.det_comida import DetComida
from models.hist_receta import HistReceta
from models.persona import Persona
from models.receta import Receta

from routes.login import log
from routes.registro import registro
from routes.perfil import perfil
from routes.eliminar_cuenta import delUsr
from routes.inicio import inicio
from routes.update_cuenta import updtUsr

app = Flask(__name__)

# settings
app.secret_key = "123456"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/control_alimenticio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicializar la aplicacion con la base de datos
db.init_app(app)

app.register_blueprint(log)
app.register_blueprint(registro)
app.register_blueprint(perfil)
app.register_blueprint(delUsr)
app.register_blueprint(inicio)
app.register_blueprint(updtUsr)

