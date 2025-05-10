from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import aliased
from sqlalchemy import cast, Date
from src.database.db import db
from datetime import datetime, date

# Entidades
from src.models.models import Especialista, Paciente, Comida, AC, Alimento, Asignacion
# 

# FIXME: Hay que agregar los try-catch en todos los metodos

pac = Blueprint('paciente', __name__)

# Registrar <
@pac.route('/registro_paciente', methods=['GET','POST'])
def registro():
  if request.method == "POST":
    pri_nombre = request.form['pac-pri-nombre']
    pri_apellido = request.form['pac-pri-apellido']
    seg_apellido = request.form['pac-seg-apellido']
    sexo = request.form['pac-sexo']
    correo = request.form['pac-correo']
    telefono = request.form['pac-telefono']
    clave = request.form.get('pac-clave')
    clave2 = request.form.get('pac-clave2')
    fecha_nac_str = request.form.get('pac-fecha-nacimiento')
    seg_nombre = request.form['pac-seg-nombre']

    if not clave or not clave2:
        return "Las contraseñas son requeridas", 400

    # Validar coincidencia de contraseñas
    if clave != clave2:
        return "Las contraseñas no coinciden", 400
    
    paciente_existente = Paciente.query.filter_by(correo=correo).first()
    if paciente_existente:
        flash('Este correo ya está registrado', 'danger')
        return redirect(url_for('paciente.registro'))    
    
    # Hacer la contraseña segura
    hashed_clave = generate_password_hash(clave)   
    # //

    if not fecha_nac_str:
        flash('La fecha de nacimiento es requerida', 'danger')
        return redirect(url_for('paciente.registro'))

    try:
        fecha_nacimiento = datetime.strptime(fecha_nac_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Formato de fecha inválido. Use AAAA-MM-DD', 'danger')
        return redirect(url_for('paciente.registro'))  

    # Se inserta el paciente en la tabla
    new_pac = Paciente (
        pri_nombre,
        pri_apellido,
        seg_apellido,
        sexo,
        correo,
        telefono,
        hashed_clave,
        fecha_nacimiento,
        seg_nombre
    )

    db.session.add(new_pac)
    db.session.commit()
    db.session.close()

    flash("Paciente agregado correctamente", "success")
    # //

    return redirect(url_for('index.index'))
  
  else:
      return render_template('registro.html')
# // > 

# Inicio <
@pac.route('/inicio/<id>', methods=['GET', 'POST'])
def inicio(id):

    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()

    if get_pac is None:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('index.index')) 

    date = datetime.now()
    formatted_date = date.strftime("%d, %B %Y")

    if request.method == "POST":
        fecha_str = request.form['pac-fecha']
        try:
    
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            start_date = fecha.replace(hour=0, minute=0, second=0)
            end_date = fecha.replace(hour=23, minute=59, second=59)
        except ValueError:
            flash("Formato de fecha inválido. Use YYYY-MM-DD", "danger")
            return redirect(url_for('paciente.inicio', id=id))


        formatted_date = fecha.strftime("%d, %B %Y")

        tipo = db.session.query(Comida.tipo, Comida.fecha_ini)\
            .filter(Comida.fecha_ini.between(start_date, end_date))\
            .filter(Comida.id_paciente == id)\
            .order_by(Comida.fecha_ini).all()

        return render_template('p_inicio.html', 
                            get_pac=get_pac,
                            formatted_date=formatted_date,
                            tipo=tipo,
                            fecha=fecha.date())

    tipo = (
        db.session.query(Comida.tipo, Comida.fecha_ini)
        .filter(Comida.id_paciente == id)
        .filter(Comida.comentario != None)
        .order_by(Comida.fecha_ini)
    ).all()

    return render_template("p_inicio.html", get_pac=get_pac, formatted_date=formatted_date, date=formatted_date, tipo=tipo)
# // >

# Perfil <
@pac.route('/perfil/<id>', methods=["GET"])
def perfil(id):
    paciente = Paciente.query.get(id)

    if paciente is None:
        flash("Paciente no encontrado", "danger")
        return redirect(url_for('index.index'))
    
    return render_template("p_perfil.html", id=id, paciente=paciente)
# // >

# Modificar Perfil <
@pac.route('/editar_perfil/<id>', methods=['GET', 'POST'])
def updateProfile(id):

    paciente = Paciente.query.get(id)

    if paciente is None:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('index.index')) 

    if request.method == 'POST':

        paciente.pri_nombre = request.form['pac-pri-nombre']
        paciente.pri_apellido = request.form['pac-pri-apellido']
        paciente.seg_apellido = request.form['pac-seg-apellido']
        paciente.sexo = request.form['pac-sexo']
        paciente.correo = request.form['pac-correo']
        paciente.telefono = request.form['pac-telefono']
        clave = request.form['pac-clave']
        paciente.clave = generate_password_hash(clave)   
        paciente.fecha_nacimiento = (datetime.strptime(request.form['pac-fecha-nacimiento'], '%Y-%m-%d').date())

        paciente.seg_nombre = request.form['pac-seg-nombre']

        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({ 'success': True, 'message': 'Perfil actualizado correctamente' })
        
        flash("Perfil actualizado correctamente", "success")
        return render_template('p_editar_perfil.html', paciente=paciente)
    
    return render_template('p_editar_perfil.html', paciente=paciente)
# // >

# Eliminar Cuenta <
@pac.route('/eliminar_cuenta/<id>', methods=['POST'])
def deleteAccount(id):
    paciente = Paciente.query.get(id)

    if paciente:
        for asignacion in paciente.asignaciones:
            db.session.delete(asignacion)

        db.session.delete(paciente)
        db.session.commit()
        db.session.close()
        flash("Cuenta eliminada correctamente", "success")
        return redirect(url_for('index.index'))
    else:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))
# // >

# Detalle de comida <
@pac.route('/detalle_comida/<id>', methods=["GET"])
def foodDetail(id):
    
    try:
        get_pac = db.session.query(Paciente.id_paciente).filter(Paciente.id_paciente == id).first()

        date_param = request.args.get('date') 

        if isinstance(date_param, str):
            date_obj = datetime.strptime(date_param, '%Y-%m-%d %H:%M:%S')
        elif isinstance(date_param, date):
            date_obj = datetime.combine(date_param, datetime.min.time())
        else:
            return redirect(url_for('paciente.inicio', id=id, error="Fecha inválida"))

        datos = db.session.query(
            Alimento.nombre,
            Alimento.cantidad,
            Alimento.tipo.label('tipo_alimento'),
            Comida.fecha_ini,
            Comida.tipo,
            Comida.satisfaccion,
            Comida.comentario,
            Especialista.pri_nombre,
            Especialista.pri_apellido
        ).select_from(Comida).\
        join(AC, Comida.id_paciente == AC.id_paciente).\
        join(Alimento, Alimento.id_alimento == AC.id_alimento).\
        join(Especialista, Comida.id_espe == Especialista.id_espe).\
        filter(
            Comida.fecha_ini == date_obj, 
            Comida.id_paciente == id,
            AC.fecha_ini == Comida.fecha_ini
        ).distinct().all()

        db.session.close()

        date_formatted = date_obj.strftime("%B, %d %Y a las %H:%M")

        return render_template("p_detalle_comida.html", 
                             get_pac=get_pac, 
                             datos=datos, 
                             date=date_param, 
                             date_formatted=date_formatted)
    
    except Exception as e:
        db.session.rollback()
        flash(f"Error en el Detalle de Comida: {e}")
        return render_template(url_for('paciente.inicio', id=id))
# // >

# Modificar Comida <
@pac.route('/editar_comida/<id>/<date>', methods=['GET', 'POST'])
def updateFood(id, date):
    try:
        # Convertir parámetro de fecha a datetime
        date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')  # Conversión inicial
        
        get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()
        get_ali = db.session.query(Alimento).all()
        
        # Verificar existencia del paciente
        if get_pac is None:
            flash('Paciente no encontrado.', 'danger')
            return redirect(url_for('index.index')) 
            
        # Consulta de especialistas
        get_esp = db.session.query(
            Especialista.id_espe,
            Especialista.pri_nombre,
            Especialista.pri_apellido
        ).select_from(Comida)\
        .join(Paciente, Comida.id_paciente == Paciente.id_paciente)\
        .join(Especialista, Comida.id_espe == Especialista.id_espe)\
        .filter(Paciente.id_paciente == id).distinct().all()

        # Formatear fecha para mostrar
        date_formatted = date_obj.strftime("%B, %d %Y a las %H:%M")

        # Consulta principal usando el objeto datetime
        datos = db.session.query(
            Alimento.nombre,
            Alimento.cantidad,
            Alimento.id_alimento,
            Alimento.tipo.label('tipo_alimento'),
            Comida.fecha_ini,
            Comida.tipo,
            Comida.satisfaccion,
            Comida.comentario,
            Especialista.pri_nombre,
            Especialista.pri_apellido
        ).select_from(Comida)\
        .join(AC, Comida.id_paciente == AC.id_paciente)\
        .join(Alimento, Alimento.id_alimento == AC.id_alimento)\
        .join(Especialista, Comida.id_espe == Especialista.id_espe)\
        .filter(
            Comida.fecha_ini == date_obj,  # Usar objeto datetime aquí
            Comida.id_paciente == id,
            AC.fecha_ini == date_obj  # Y aquí
        ).distinct().all()

        # Manejo de GET para mostrar formulario
        if request.method == 'GET' and request.args.get('modal') == '1':
            return render_template(
                'p_editar_comida.html',
                id=id,
                get_pac=get_pac,
                get_ali=get_ali,
                get_esp=get_esp,
                datos=datos,
                date=date,  # Mantener el string original para referencias
                date_formatted=date_formatted
            )

        # Manejo de POST para actualizar datos
        if request.method == 'POST':
            tipo_comida = request.form['tipo-comida']
            satisfaccion = request.form['satisfaccion']
            comentario = request.form['comentario']
            id_espe = request.form['id-espe']

            # Buscar comida usando datetime
            comida = db.session.query(Comida).filter(
                Comida.id_paciente == id,
                Comida.fecha_ini == date_obj  # Usar objeto datetime
            ).first()

            if not comida:
                flash("Comida no encontrada", "danger")
                return redirect(url_for('paciente.inicio', id=id))

            # Actualizar campos básicos
            comida.tipo = tipo_comida
            comida.satisfaccion = satisfaccion
            comida.comentario = comentario
            comida.id_espe = id_espe

            # Manejo de alimentos asociados
            submitted_ids = {int(x) for x in request.form.getlist('alimentos[]') if x}
            
            # Consultar registros existentes usando datetime
            existing_ac_records = db.session.query(AC).filter(
                AC.id_paciente == get_pac.id_paciente,
                AC.id_espe == id_espe,
                AC.fecha_ini == date_obj  # Usar objeto datetime
            ).all()
            
            # Eliminar relaciones removidas
            existing_ids = {ac.id_alimento for ac in existing_ac_records}
            for ac in existing_ac_records:
                if ac.id_alimento not in submitted_ids:
                    db.session.delete(ac)

            # Agregar nuevas relaciones
            for ali_id in submitted_ids - existing_ids:
                new_ac = AC(
                    id_paciente=get_pac.id_paciente,
                    id_espe=id_espe,
                    fecha_ini=date_obj,  # Usar objeto datetime
                    id_alimento=ali_id
                )
                db.session.add(new_ac)

            db.session.commit()
            flash("Comida actualizada exitosamente", "success")
            return redirect(url_for('paciente.inicio', id=id))

    except ValueError as e:
        flash(f"Formato de fecha inválido: {date}", "danger")
        return redirect(url_for('paciente.inicio', id=id))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error al modificar la comida: {str(e)}", "danger")
        return redirect(url_for('paciente.inicio', id=id))
        
    finally:
        db.session.close()

    return render_template('p_editar_comida.html', 
                         id=id, 
                         get_pac=get_pac, 
                         get_ali=get_ali, 
                         date=date, 
                         datos=datos, 
                         date_formatted=date_formatted, 
                         get_esp=get_esp)
# // >

# Funcion para eliminar un alimento dentro de la comida
@pac.route('/eliminar_alimento/<int:id_alimento>/<date>/<int:id>', methods=['DELETE'])
def eliminar_alimento(id_alimento, date, id):
    try:
        ac_record = db.session.query(AC).filter(
            AC.id_alimento == id_alimento,
            AC.id_paciente == id,
            AC.fecha_ini == date
        ).first()
        if ac_record:
            db.session.delete(ac_record)
            db.session.commit()
            return jsonify({'message': 'Alimento eliminado con éxito.'}), 200
        else:
            return jsonify({'message': 'Alimento no encontrado.'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar el alimento: {e}'}), 500
    finally:
        db.session.close()
# // >

# Eliminar Comida <
@pac.route('/eliminar_comida/<id>/<date>', methods=['GET', 'POST'])
def deleteFood(id, date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') 
        
        comida = db.session.query(Comida).filter(
            Comida.id_paciente == id,
            Comida.fecha_ini == date_obj 
        ).first()
        
        if comida:
            db.session.delete(comida)
            db.session.commit()
            return redirect(url_for('paciente.inicio', id=id))
        else:
            flash("Comida no encontrada", "danger")
            return redirect(url_for('paciente.inicio', id=id))
            
    except ValueError as ve:
        flash(f"Formato de fecha inválido: {date}", "danger")
        return redirect(url_for('paciente.inicio', id=id))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar la comida: {e}", "danger")
        return redirect(url_for('paciente.inicio', id=id))
        
    finally:
        db.session.close()
# // >

# Ver Especialistas <
@pac.route('/ver_especialistas/<id>', methods=['GET'])
def especialistas(id):
    date = datetime.now()
    date = date.strftime("%b, %d %Y")

    result = db.session.query(
        Especialista.pri_nombre, 
        Especialista.pri_apellido, 
        Especialista.especialidad,
        Especialista.id_espe
    ).join(
        Asignacion, Especialista.id_espe == Asignacion.id_espe
    ).filter(
        Asignacion.id_paciente == id
    ).distinct().all()

    get_pac = Paciente.query.get(id)

    return render_template('p_ver_especialistas.html', 
                         id=id, 
                         result=result, 
                         date=date, 
                         get_pac=get_pac)
# // >

# Detalle especialistas <
@pac.route('/detalle_especialista/<id>/<espe>', methods=['GET'])
def detalleEspecialista(id, espe):
    tipo_comida = request.args.get('tipo_comida', '')

    paciente = Paciente.query.get(id)
    especialista = db.session.query(Especialista).filter(Especialista.id_espe == espe).first()
    
    if tipo_comida:
        comidas = db.session.query(Comida).filter(Comida.id_espe == espe, Comida.id_paciente == id, Comida.tipo == tipo_comida).all()
    else:
        comidas = db.session.query(Comida).filter(Comida.id_espe == espe, Comida.id_paciente == id).all()
    
    for comida in comidas:
        comida.alimentos = db.session.query(Alimento).join(AC, Alimento.id_alimento == AC.id_alimento).filter(AC.id_paciente == comida.id_paciente, AC.id_espe == comida.id_espe, AC.fecha_ini == comida.fecha_ini).all()
    
    db.session.close()

    return render_template('p_detalle_especialista.html', especialista=especialista, paciente=paciente, comidas=comidas, tipo_comida=tipo_comida)

@pac.route('/get_comida/<id>/<date>', methods=['GET'])
def get_comida(id, date):
    try:
        datos = db.session.query(
            Alimento.nombre,
            Alimento.cantidad,
            Alimento.id_alimento,
            Alimento.tipo.label('tipo_alimento'),
            Comida.fecha_ini,
            Comida.tipo,
            Comida.satisfaccion,
            Comida.comentario,
            Especialista.pri_nombre,
            Especialista.pri_apellido
        ).select_from(Comida).\
        join(AC, Comida.id_paciente == AC.id_paciente).\
        join(Alimento, Alimento.id_alimento == AC.id_alimento).\
        join(Especialista, Comida.id_espe == Especialista.id_espe).\
        filter(
            Comida.fecha_ini == date, 
            Comida.id_paciente == id,
            AC.fecha_ini == Comida.fecha_ini
        ).distinct().all()

        date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date_formatted = date_obj.strftime("%B, %d %Y a las %H:%M")

        return jsonify({
            'datos': [dato._asdict() for dato in datos],
            'date_formatted': date_formatted
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al obtener la comida: {e}'}), 500
    finally:
        db.session.close()

@pac.route('/addFood/<id>', methods=['GET', 'POST'])
def addFood(id):
    get_pac = Paciente.query.get(id)
    get_esp = Especialista.query.join(Asignacion, Especialista.id_espe == Asignacion.id_espe)\
                                .filter(Asignacion.id_paciente == id)\
                                .all()
    alimentos = Alimento.query.all() 

    alimentos = db.session.query(Alimento).all()
    print("DEBUG: Base de datos conectada en:", db.engine.url)
    print("DEBUG: Alimentos en sesión:", len(alimentos))

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            id_espe = request.form['id-espe']
            tipo_comida = request.form['tipo-comida']
            satisfaccion = request.form['satisfaccion']
            comentario = request.form['comentario']
            fecha_ini = datetime.strptime(request.form['fecha-ini'], '%Y-%m-%dT%H:%M')
            
            # Crear nueva comida
            nueva_comida = Comida(
                id_paciente=id,
                id_espe=id_espe,
                fecha_ini=fecha_ini,
                tipo=tipo_comida,
                satisfaccion=satisfaccion,
                comentario=comentario
            )
            db.session.add(nueva_comida)
            
            # Agregar alimentos relacionados
            alimentos_ids = request.form.getlist('alimentos[]')
            for alimento_id in alimentos_ids:
                ac = AC(
                    id_paciente=id,
                    id_espe=id_espe,
                    fecha_ini=fecha_ini,
                    id_alimento=alimento_id
                )
                db.session.add(ac)
            
            db.session.commit()
            flash("Comida registrada exitosamente", "success")
            return redirect(url_for('paciente.inicio', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar la comida: {str(e)}", "danger")
    
    return render_template('p_add_comida.html', 
                         get_pac=get_pac,
                         get_esp=get_esp,
                         alimentos=alimentos)