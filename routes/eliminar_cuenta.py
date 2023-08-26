from flask import Blueprint, render_template, request, redirect, url_for, session
from models.persona import Persona
from utils.db import db

delUsr = Blueprint('delUsr', __name__)

@delUsr.route('/del_paciente/<id>', methods=["GET"])
def delPac(id):
    get_usr = Persona.query.get(id)
    db.session.delete(get_usr)
    db.session.commit()
    return render_template('del_paciente.html', get_usr=get_usr)

@delUsr.route('/del_especialista/<id>', methods=["GET"])
def delEsp(id):
    get_usr = Persona.query.get(id)
    db.session.delete(get_usr)
    db.session.commit()
    return render_template('del_especialista.html', get_usr=get_usr)
