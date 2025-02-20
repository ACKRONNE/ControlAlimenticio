from flask import Flask
from src.database.db import db
from sqlalchemy import create_engine
from flask_mail import Mail

# Objetos de las rutas
from src.routes.index import ind
from src.routes.paciente import pac
from src.routes.especialista import esp

# Librerias para el funcionamiento
from dotenv import load_dotenv
import os
# //

load_dotenv()

app = Flask(__name__)

# Settings de la DB
key = os.environ['SECRETKEY']
config = os.environ['POSTGRESCONFIG']

app.secret_key = key
app.config['SQLALCHEMY_DATABASE_URI'] = config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# //

engine = create_engine(config)
db.metadata.create_all(engine)

# inicializar la aplicacion con la base de datos
db.init_app(app)
# //

app.register_blueprint(ind)
app.register_blueprint(pac)
app.register_blueprint(esp)


mail = os.environ['MAIL_USERNAME']
password = os.environ['MAIL_PASSWORD']
default_sender = os.environ['MAIL_DEFAULT_SENDER']

# Configuraci�n del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = mail
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_DEFAULT_SENDER'] = default_sender

mail = Mail(app)

if __name__ == '__main__':
    app.run(debug=True)
