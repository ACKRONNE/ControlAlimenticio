from flask import Blueprint, render_template, request, redirect, url_for, Response, session, flash
from models.persona import Persona
from utils.db import db

log = Blueprint('log', __name__)

@log.route('/')
def index():
    return render_template('index.html')



@log.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST" and 'txt-correo' in request.form and request.form['txt-contraseña']:
        _correo = request.form['txt-correo']
        _contraseña = request.form['txt-contraseña']

        # Check if the user exists in the database
        account = Persona.query.filter_by(correo=_correo).filter_by(contraseña=_contraseña).first()
            
        if account:
            session['logueado'] = True
            session['id'] = account.id_persona
            session['tipo'] = account.tipo

            if session['tipo'] == 'p':
                return render_template('ini_paciente.html')
            elif session['tipo'] == 'e':
                return render_template('ini_especialista.html')
        else:
            return render_template('index.html', mensaje = 'El usuario no se encuentra registrado')
    else:
        return render_template('login.html')

