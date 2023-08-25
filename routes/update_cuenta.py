from flask import Blueprint, render_template, request, redirect, url_for, session
from models.persona import Persona
from utils.db import db

updtUsr = Blueprint('updtUsr', __name__)

@updtUsr.route('/update_paciente/<id>', methods=["GET","POST"])
def updatePac(id):
    if request.method == 'POST':

        get_usr = Persona.query.get(id)

        get_usr.nombre = request.form['updt-nombre-pac']
        get_usr.apellido = request.form['updt-apellido-pac']
        get_usr.tipo = 'p'
        get_usr.sexo = request.form['updt-genero-pac']
        get_usr.correo = request.form['updt-correo-pac']
        get_usr.direccion = request.form['updt-direccion-pac']
        get_usr.telefono = request.form['updt-telefono-pac']
        get_usr.contraseña = request.form['updt-contraseña-pac']
        get_usr.fecha_nac = request.form['updt-fechaNac-pac']
        get_usr.especialidad = None
        get_usr.id_espe = None 

        db.session.commit()

        return redirect(url_for('inicio.inicioPac', id=id))
    else:
        get_usr = Persona.query.get(id)
        return render_template("update_paciente.html", get_usr=get_usr)