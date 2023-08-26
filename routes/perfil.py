from flask import Blueprint, render_template, request, redirect, url_for
from models.persona import Persona
from utils.db import db

perfil = Blueprint('perfil', __name__)

@perfil.route('/perfil_paciente/<id>', methods=["GET"])
def perfilPac(id):
    perfil = Persona.query.get(id)
    return render_template("perfil_paciente.html", perfil=perfil)

@perfil.route('/perfil_especialista/<id>', methods=["GET"])
def perfilEsp(id):
    perfil = Persona.query.get(id)
    return render_template("perfil_especialista.html", perfil=perfil)

