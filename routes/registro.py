from flask import Blueprint, render_template, request, redirect, url_for
from models.persona import Persona
from utils.db import db

registro = Blueprint('registro', __name__)

# >
@registro.route('/registro_usuario')
def registroUsuario():
    return render_template('registro_usuario.html')
# ---

# >
@registro.route('/registro_paciente', methods=['GET','POST'])
def registroPac():
    if request.method == "POST":
        _nombre = request.form['txt-nombre-pac']
        _apellido = request.form['txt-apellido-pac']
        _tipo = 'p'
        _sexo = request.form['txt-genero-pac']
        _correo = request.form['txt-correo-pac']
        _direccion = request.form['txt-direccion-pac']
        _telefono = request.form['txt-telefono-pac']
        _contraseña = request.form['txt-contraseña-pac']
        _fechaNac = request.form['txt-fechaNac-pac']
        _especialidad = None
        _id_espe = None

        new_pac = Persona(
            _nombre,
            _apellido,
            _tipo,
            _sexo,
            _correo,  
            _direccion,  
            _telefono,  
            _contraseña,  
            _fechaNac,
            _especialidad, 
            _id_espe
        )

        db.session.add(new_pac)
        db.session.commit()
        return render_template('ini_paciente.html')

    else:
        return render_template('registro_paciente.html')
# ---

# >
@registro.route('/registro_especialista', methods=['GET','POST'])
def registroEsp():
    if request.method == "POST":
        _nombre = request.form['txt-nombre-esp']
        _apellido = request.form['txt-apellido-esp']
        _tipo = 'e'
        _sexo = request.form['txt-genero-esp']
        _correo = request.form['txt-correo-esp']
        _direccion = request.form['txt-direccion-esp']
        _telefono = request.form['txt-telefono-esp']
        _contraseña = request.form['txt-contraseña-esp']
        _fechaNac = None
        _especialidad = request.form['txt-especialidad-esp']
        _id_espe = None

        new_esp = Persona(
            _nombre,
            _apellido,
            _tipo,
            _sexo,
            _correo,  
            _direccion,  
            _telefono,  
            _contraseña,  
            _fechaNac,
            _especialidad, 
            _id_espe
        )

        db.session.add(new_esp)
        db.session.commit()
        return render_template('ini_especialista.html')

    else:
        return render_template('registro_especialista.html')
# ---