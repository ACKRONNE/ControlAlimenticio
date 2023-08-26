from flask import Blueprint, render_template, request, redirect, url_for
from models.persona import Persona
from utils.db import db

inicio = Blueprint('inicio', __name__)

@inicio.route('/inicio_paciente/<id>')
def inicioPac(id):
    inicio = Persona.query.get(id)
    return render_template("ini_paciente.html", inicio=inicio)


@inicio.route('/inicio_especialista/<id>')
def inicioEsp(id):
    inicio = Persona.query.get(id)
    return render_template('ini_especialista.html', inicio=inicio)