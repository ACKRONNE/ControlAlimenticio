from flask import Blueprint, render_template, request, redirect, url_for
from models.persona import Persona
from models.comida import Comida
from models.ar import AR
from models.hist_comida import HistComida
from models.alimento import Alimento
from sqlalchemy import and_, distinct
from datetime import datetime
from utils.db import db

inicio = Blueprint('inicio', __name__)

# Home Page
@inicio.route('/inicio_paciente/<id>', methods=['GET', 'POST'])
def inicioPac(id):
    inicio = Persona.query.get(id)

    date = datetime.now()
    formatted_date = date.strftime("%b. %d")

    if request.method == 'POST':
        # Extraigo la fecha
        fecha_str = request.form['srch-fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        formatted_fecha = fecha.strftime('%B, %d %Y')

        # Realizar la consulta
        resultados = db.session.query(Comida.tipo, HistComida.fecha_ini)\
        .join(HistComida, and_(Comida.id_comida == HistComida.id_comida, Comida.id_persona == HistComida.id_persona))\
        .filter(and_(Comida.id_persona == inicio.id_persona, HistComida.fecha_ini == fecha))

        return render_template('ini_paciente.html', inicio=inicio, formatted_date=formatted_date, resultados=resultados, formatted_fecha=formatted_fecha)
    else:    
        return render_template("ini_paciente.html", inicio=inicio, formatted_date=formatted_date)


@inicio.route('/inicio_especialista/<id>', methods=['GET', 'POST'])
def inicioEsp(id):
    inicio = Persona.query.get(id)    

    date = datetime.now()
    formatted_date = date.strftime("%b. %d")

    return render_template('ini_especialista.html', inicio=inicio, formatted_date=formatted_date)

@inicio.route('/detalle_comida/<id>')
def detallePac(id):    

    inicio = Persona.query.get(id)

    result = db.session.query(
        distinct(Alimento.tipo),
        Comida.tipo,
        Alimento.nombre,
        Alimento.cantidad,
        Comida.satisfaccion,
        Comida.comentario
    ).filter(
        and_(
            Comida.id_comida == AR.id_comida,
            Comida.id_persona == AR.id_persona,
            Alimento.id_alimento == AR.id_alimento,
            Comida.id_persona == 6,
            HistComida.fecha_ini == '2023-03-15',
            Comida.tipo == 'a'
        )
    ).all()

    return render_template('dc_paciente.html', results=result, inicio=inicio)