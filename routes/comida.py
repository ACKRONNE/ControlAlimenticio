from flask import Blueprint, render_template, request, redirect, url_for
from models.persona import Persona
from models.comida import Comida
from models.ar import AR
from models.hist_comida import HistComida
from models.alimento import Alimento
from utils.db import db

comida = Blueprint('comida', __name__)

@comida.route('/add_comida_pac/<id>', methods=["GET", "POST"])
def comidaPac(id):

    get_usr = Persona.query.get(id)
    # get_comida = Comida.query.get(id) # Hay que cambiar esta consulta

    # if request.method == "POST":


    #     # Tabla alimnto
    #     _tipoA = request.form['food-tipo-pac']

    #     # Tabla comida
    #     _tipo = request.form['food-tipo-pac']
    #     _satisfaccion = request.form['feel-pac']
    #     _tipo = request.form['comment']

        

    #     new_ali = Alimento(
            
    #     )

    #     new_com = Comida(

    #     )

    #     new_hist = HistComida(
    #         date=datetime.now()
    #     )

    #     ar = AR(
    #         persona_id=persona.id, 
    #         comida_id=comida.id, 
    #         hist_comida_id=hist_comida.id
    #     )


    #     new_esp = Persona(
    #         _nombre,
    #         _apellido,
    #         _tipo,
    #         _sexo,
    #         _correo,  
    #         _telefono,  
    #         _contraseña,  
    #         _fechaNac,
    #         _especialidad, 
    #         _id_espe
    #     )

    #     # FIXME: Falta cerrar la sesion de la DB
    #     db.session.add(new_esp)
    #     db.session.commit()

    return redirect(url_for('inicio.inicioPac'), get_usr=get_usr)
    # else:
    #     return render_template("add_food_pac.html", get_usr=get_usr)

@comida.route('/add_comida_esp/<id>', methods=["GET", "POST"])
def comidaEsp(id):

    get_usr = Persona.query.get(id)
    # get_comida = Comida.query.get(id) # Hay que cambiar esta consulta

    # if request.method == "POST":

    return redirect(url_for('inicio.inicioEsp'), get_usr=get_usr)
    # else:
    #     return render_template("add_food_esp.html", get_usr=get_usr)