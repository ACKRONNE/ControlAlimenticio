from flask import Blueprint, render_template, request, redirect, url_for, session
from models.persona import Persona
from utils.db import db

password = Blueprint('password', __name__)

@password.route('/recovery', methods=['GET','POST'])
def recovery():
    if request.method == "POST":

        _correo = request.form['txt-correo-rec']

        # Check if the user is in the database
        cuenta = Persona.query.filter_by(correo=_correo).first()

        if cuenta:
            session['logueado'] = True
            return "Correo de recuperacion enviado satisfactoriamente"
        else:
            return render_template('recovery_email.html', mensaje="El usuario no se encuentra registrado")
    else:
        return render_template('recovery_email.html')

@password.route('/recovery_password/<id>', methods=['GET','POST'])
def recoveryPas(id):
    if request.method == "POST":

        cuenta = Persona.query.get(id)

        _contra1 = request.form['txt-contraseña-1']
        _contra2 = request.form['txt-contraseña-2']

        if _contra1 == _contra2:
            cuenta.nombre = _contra1
            return "Contraseña Reestablecida con exito"
        else:
            return "Las contraseñas no coinciden"

    else:
        return render_template('recovery_password.html', id=1)