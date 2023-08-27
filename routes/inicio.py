from flask import Blueprint, render_template, request, redirect, url_for
from models.persona import Persona
from datetime import datetime
from utils.db import db

inicio = Blueprint('inicio', __name__)

# Home Page
@inicio.route('/inicio_paciente/<id>')
def inicioPac(id):
    inicio = Persona.query.get(id)

    date = datetime.now()
    formatted_date = date.strftime("%b. %d")

    if request.method == 'POST':
        _fecha = request.form.get('srch-fecha')

        resultados = Evento.query.filter(HistReceta.fecha_ini.like(_fecha)).all()

        return render_template('resultados.html', resultados=resultados)
    else:    
        return render_template("ini_paciente.html", inicio=inicio, formatted_date=formatted_date)


@inicio.route('/inicio_especialista/<id>', methods=['GET', 'POST'])
def inicioEsp(id):
    inicio = Persona.query.get(id)    

    date = datetime.now()
    formatted_date = date.strftime("%b. %d")

    return render_template('ini_especialista.html', inicio=inicio, formatted_date=formatted_date)
