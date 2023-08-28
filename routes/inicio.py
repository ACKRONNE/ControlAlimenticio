from flask import Blueprint, render_template, request, redirect, url_for, session
from models.persona import Persona
from models.comida import Comida
from models.ar import AR
from models.hist_comida import HistComida
from models.alimento import Alimento
from sqlalchemy import and_, distinct
from sqlalchemy.orm import aliased
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

        db.session.close()

        return render_template('ini_paciente.html', inicio=inicio, formatted_date=formatted_date, resultados=resultados, formatted_fecha=formatted_fecha)
    else:    
        return render_template("ini_paciente.html", inicio=inicio, formatted_date=formatted_date)

# FIXME: Tengo que coloca los datos de la fecha y la comida que se actualicen automaticamente
@inicio.route('/detalle_comida/<id>')
def detalleCom(id):    

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
            Comida.tipo == 'd'
        )
    ).all()

    db.session.close()

    return render_template('dc_paciente.html', results=result, inicio=inicio)


@inicio.route('/inicio_especialista/<id>', methods=['GET', 'POST'])
def inicioEsp(id):
     
    PersonaP = aliased(Persona) # represents 'Paciente'
    PersonaE = aliased(Persona) # represents 'Especialista'

    inicio = Persona.query.get(id)

    date = datetime.now()
    formatted_date = date.strftime("%b. %d")

    # Realizar la consulta
    resultados = db.session.query(PersonaP.nombre, PersonaP.apellido, PersonaP.fecha_nac)\
    .join(PersonaE, PersonaP.id_espe == PersonaE.id_persona)\
    .filter(and_(PersonaP.id_espe == PersonaE.id_persona, PersonaE.id_persona == inicio.id_persona))\
    .all()

    db.session.close()

    hoy = datetime.today()

    return render_template('ini_especialista.html', inicio=inicio, formatted_date=formatted_date, resultados=resultados, today=hoy)


# FIXME: Falta desarrollar esto
@inicio.route('/detalle_comida/<id>')
def detallePac(id):    

    inicio = Persona.query.get(id)

    db.session.close()

    return render_template('dc_paciente.html', results=result, inicio=inicio)