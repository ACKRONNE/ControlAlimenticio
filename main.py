from flask import render_template, request, redirect, url_for, Response, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import *


@app.route('/')
def index():
    return render_template('index.html')

# → → → INICIO DE SESION ← ← ←
@app.route('/inicio-sesion.html')
def inicioSesion():
   return render_template('inicio-sesion.html')   

# → → INICIO DE SESION ← ←
@app.route('/acceso-login', methods=["GET", "POST"])
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
                return render_template('paciente.html')
            elif session['tipo'] == 'e':
                return render_template('especialista.html')
        else:
            return render_template('inicio-sesion.html', mensaje = flash('El usuario no se encuentra registrado'))

# → → → ELECCION DE REGISTRO ← ← ←
@app.route('/eleccion-registro.html')
def eleccionRegistro():
    return render_template('eleccion-registro.html')

# → → REGISTRO PACIENTE ← ←
@app.route('/registro-paciente.html', methods=["GET", "POST"])
def registroPac():
    _correo = request.form['txt-correo-pac']
    _nombre = request.form['txt-nombre-pac']
    _apellido = request.form['txt-apellido-pac']
    _genero = request.form['txt-genero-pac']
    _contraseña = request.form['txt-contraseña-pac']
    _direccion = request.form['txt-direccion-pac']
    _fechaNac = request.form['txt-fechaNac-pac']
    _telefono = request.form['txt-telefono-pac']

    
    

    return render_template('registro-paciente.html')

@app.route('/registro-especialista.html')
def registroEsp():
    return render_template('registro-especialista.html')

if __name__ == '__main__':
    app.run(debug=True)
