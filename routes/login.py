from flask import Blueprint, render_template, request, redirect, url_for, session
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

            _id = session['id']

            if session['tipo'] == 'p':
                return redirect(url_for('inicio.inicioPac', id=_id))
            elif session['tipo'] == 'e':
                return redirect(url_for('inicio.inicioEsp', id=_id))
        else:
            return render_template('login.html', mensaje = 'El usuario no se encuentra registrado')
    else:
        return render_template('login.html')

@log.route('/logout/<id>', methods=['GET'])
def logout(id):
    
    user = Persona.query.get(id)

    if user is None:
        return "Usuario no encontrado"

    if 'account' not in session or session['account'] != int(id):
        return "No hay una sesión activa para este usuario"

    if user.id_persona == int(id):
        session.clear()
        return redirect(url_for('log.index'))
    else:
        return "Error 404, No se pudo cerrar la sesion"
