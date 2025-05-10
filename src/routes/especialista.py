from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import aliased
from sqlalchemy import cast, Date, distinct, select
from src.database.db import db
from datetime import datetime

# Entidades
from src.models.models import Especialista, Paciente, Comida, AC, Alimento, Asignacion
# //

esp = Blueprint('especialista', __name__)

# Registro <
@esp.route('/registro_especialista', methods=['GET','POST'])
def registro():
    if request.method == "POST":
        pri_nombre = request.form['esp-pri-nombre']
        pri_apellido = request.form['esp-pri-apellido']
        seg_apellido = request.form['esp-seg-apellido']
        sexo = request.form['esp-sexo']
        correo = request.form['esp-correo']
        telefono = request.form['esp-telefono']
        clave = request.form['esp-clave']
        especialidad = request.form['esp-especialidad']
        seg_nombre = request.form['esp-seg-nombre']

        # Hacer la contraseña segura
        hashed_clave = generate_password_hash(clave)   
        # //

        # Se inserta el especialista en la tabla
        new_esp = Especialista (
            pri_nombre,
            pri_apellido,
            seg_apellido,
            sexo,
            correo,
            telefono,
            hashed_clave,
            especialidad,
            seg_nombre
        )

        db.session.add(new_esp)
        db.session.commit()
        db.session.close()

        flash("Especialista agregado correctamente", "success")
        # //

        return redirect(url_for('index.index'))
    else:
        return render_template('registro.html')
# // >

# Inicio <
@esp.route('/inicio_especialista/<int:id>')
def inicio(id):

    # Consulta todos los datos del especialista
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()

    if get_esp is None:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))
    # //

    # Consulta todos los pacientes del especialista
    pacientes = select(distinct(Asignacion.id_paciente)).where(Asignacion.id_espe == id)
    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente.in_(pacientes)).all()
    # //

    # Fecha Actual
    date = datetime.now()
    formatted_date = date.strftime("%b. %d")
    # //    

    return render_template('e_inicio.html', get_esp=get_esp, get_pac=get_pac, formatted_date=formatted_date)
# // >

# Perfil <
@esp.route('/perfil_especialista/<int:id>', methods=['GET'])
def perfil(id):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()

    if get_esp is None:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))
    
    return render_template('e_perfil.html', get_esp=get_esp)
# //

# Modificar perfil <
@esp.route('/modificar_especialista/<int:id>', methods=['GET','POST'])
def updateProfile(id):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()

    if get_esp is None:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))

    if request.method == "POST":
        get_esp.pri_nombre = request.form['esp-pri-nombre']
        get_esp.pri_apellido = request.form['esp-pri-apellido']
        get_esp.seg_apellido = request.form['esp-seg-apellido']
        get_esp.sexo = request.form['esp-sexo']
        get_esp.correo = request.form['esp-correo']
        get_esp.telefono = request.form['esp-telefono']
        clave = request.form['esp-clave']
        # Hacer la contraseña segura
        get_esp.clave = generate_password_hash(clave)   
        # //        
        get_esp.especialidad = request.form['esp-especialidad']
        get_esp.seg_nombre = request.form['esp-seg-nombre']

        db.session.commit()
        db.session.close()

        flash("Perfil modificado correctamente", "success")
        return redirect(url_for('especialista.perfil', id=id))
    else:
        return render_template('e_editar_perfil.html', get_esp=get_esp)
    
# Eliminar cuenta <
@esp.route('/eliminar_especialista/<int:id>', methods=['POST'])
def deleteAccount(id):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()

    if get_esp:
        db.session.delete(get_esp)
        db.session.commit()
        db.session.close()
        flash("Cuenta eliminada correctamente", "success")
        return redirect(url_for('index.index'))
    else:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))
# //

# Detalle Paciente <
@esp.route('/detalle_paciente/<int:id_espe>/<int:id_pac>', methods=['GET'])
def detallePaciente(id_espe, id_pac):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id_espe).first()
    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id_pac).first()

    if get_pac is None:
        flash("Paciente no encontrado", "danger")
        return redirect(url_for('especialista.inicio', id=id_espe))
    
    return render_template('e_detalle_paciente.html', get_pac=get_pac, get_esp=get_esp)
# //

# Anadir Comida <
@esp.route('/anadir_receta/<int:id_espe>/<int:id_pac>', methods=['GET', 'POST'])
def addFood(id_espe, id_pac):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id_espe).first()
    get_ali = db.session.query(Alimento).all()

    get_pac = db.session.query(
        Paciente.id_paciente,
        Paciente.pri_nombre,
        Paciente.pri_apellido
    ).select_from(Comida)\
    .join(Paciente, Comida.id_paciente == Paciente.id_paciente)\
    .join(Especialista, Comida.id_espe == Especialista.id_espe)\
    .filter(
        Especialista.id_espe == id_espe
    ).distinct().all()

    if get_esp is None:
        flash("Paciente no encontrado", "danger")
        return redirect(url_for('especialista.inicio', id=id_espe))

    if request.method == "POST":
        try:
            tipo_comida = request.form['tipo-comida']
            id_paciente = request.form['id-paciente']
            fecha_ini = request.form['fecha-ini']
            fecha_fin = request.form['fecha-fin']
    
            new_comida = Comida(
                id_paciente,
                get_esp.id_espe,
                fecha_ini,
                tipo_comida,
                None,
                None,
                fecha_fin,
            )
            db.session.add(new_comida)
            db.session.commit()
            print("Comida agregada con exito")
            flash("Comida agregada correctamente", "success")

            _alimmento = request.form.getlist('alimentos[]')

            for alimento in _alimmento:
                if alimento:
                    new_ac = AC(
                        id_paciente,
                        get_esp.id_espe,
                        new_comida.fecha_ini,
                        alimento
                    )
                    db.session.add(new_ac)

                    print("Registro de alimento agregado con exito")
                    flash("Registro de alimento agregado con exito")
    
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Ocurrio un error al agregar la comida", "danger")
            print(f"Error: {e}")      
        finally:
            db.session.close()

        return redirect(url_for('especialista.inicio', id=id_espe))

    else:
        return render_template('e_add_receta.html', id_espe=id_espe, id_pac=id_pac, get_pac=get_pac, get_esp=get_esp, get_ali=get_ali)
# //


# Detalle Comida de un paciente especifico
@esp.route('/detalles_comidas/<id_espe>/<id_pac>', methods=['GET', 'POST'])
def foodDetail(id_espe, id_pac):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id_espe).first()
    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id_pac).first()

    # Obtener parámetros de filtrado
    fecha_ini = request.args.get('fecha_ini')
    tipo_comida = request.args.get('tipo_comida')

    query = db.session.query(
        Alimento.nombre,
        Alimento.cantidad,
        Alimento.tipo.label('tipo_alimento'),
        Comida.fecha_ini,
        Comida.tipo,
        Comida.satisfaccion,
        Comida.comentario
    ).select_from(Comida).\
    join(AC, Comida.id_paciente == AC.id_paciente).\
    join(Alimento, Alimento.id_alimento == AC.id_alimento).\
    join(Especialista, Comida.id_espe == Especialista.id_espe).\
    join(Paciente, Comida.id_paciente == Paciente.id_paciente).\
    filter(
        Comida.id_espe == id_espe, 
        Comida.id_paciente == id_pac,
    )

    # Aplicar filtros si están presentes
    if fecha_ini:
        query = query.filter(db.func.date(Comida.fecha_ini) == fecha_ini)
    if tipo_comida:
        query = query.filter(Comida.tipo == tipo_comida)

    datos = query.distinct().all()

    return render_template('e_detalle_comida.html', get_esp=get_esp, get_pac=get_pac, datos=datos)


# Lista de recetas <
@esp.route('/recetas/<id>', methods=['GET'])
def receipeList(id):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()

    if get_esp is None:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))
    
    get_com = db.session.query(
            Alimento.nombre,
            Alimento.cantidad,
            Alimento.tipo.label('tipo_alimento'),
            Comida.fecha_ini,
            Comida.tipo,
            Comida.satisfaccion,
            Comida.comentario
        ).select_from(Comida).\
        join(AC, Comida.id_paciente == AC.id_paciente).\
        join(Alimento, Alimento.id_alimento == AC.id_alimento).\
        join(Especialista, Comida.id_espe == Especialista.id_espe).\
        filter(
            Comida.id_espe == id
        ).distinct().all()
    
    return render_template('e_recetas.html', get_esp=get_esp, get_com=get_com)
# //

# Modificar Receta
@esp.route('/modificar_comida/<id_espe>/<id_pac>/<fecha_ini>', methods=['GET','POST'])
def updateFood(id_espe, id_pac, fecha_ini):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id_espe).first()
    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id_pac).first()
    get_comida = db.session.query(Comida).filter(Comida.id_paciente == id_pac, Comida.id_espe == id_espe, Comida.fecha_ini == fecha_ini).first()
    get_ac = db.session.query(AC).filter(AC.id_paciente == id_pac, AC.id_espe == id_espe, AC.fecha_ini == fecha_ini).all()
    get_ali = db.session.query(Alimento).all()

    if get_comida is None:
        flash("Comida no encontrada", "danger")
        return redirect(url_for('especialista.inicio', id=id_espe))

    if request.method == "POST":
        try:
            tipo_comida = request.form['tipo-comida']
            fecha_ini = request.form['fecha-ini']
            fecha_fin = request.form['fecha-fin']
            # Verificar que todos los datos necesarios están presentes
            get_comida.tipo_comida = tipo_comida
            get_comida.fecha_ini = fecha_ini
            get_comida.fecha_fin = fecha_fin

            db.session.commit()
            flash("Comida modificada correctamente", "success")

            _alimmento = request.form.getlist('alimentos[]')

            for alimento in _alimmento:
                if alimento:
                    new_ac = AC(
                        id_pac,
                        id_espe,
                        fecha_ini,
                        alimento
                    )
                    db.session.add(new_ac)
                    print("Registro de alimento agregado con exito")
                    flash("Registro de alimento agregado con exito")
    
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Ocurrio un error al modificar la comida", "danger")
            print(f"Error: {e}")      
        finally:
            db.session.close()

        return redirect(url_for('especialista.inicio', id=id_espe))

    else:
        return render_template('e_editar_receta.html', get_esp=get_esp, get_pac=get_pac, get_comida=get_comida)

# Asignar paciente <
@esp.route('/asignar_paciente', methods=['POST'])
def asignar_paciente():
    try:
        id_espe_str = request.form.get('id_espe')
        id_paciente_str = request.form.get('id_paciente')

        if not id_espe_str or not id_paciente_str:
            return jsonify({"error": "IDs faltantes"}), 400

        id_espe = int(id_espe_str)
        id_paciente = int(id_paciente_str)

        especialista = Especialista.query.get(id_espe)
        paciente = Paciente.query.get(id_paciente)
        
        if not especialista:
            return jsonify({"error": "Especialista no encontrado"}), 404
        if not paciente:
            return jsonify({"error": "Paciente no encontrado"}), 404

        if Asignacion.query.filter_by(id_espe=id_espe, id_paciente=id_paciente).first():
            return jsonify({"error": "La asignación ya existe"}), 409

        nueva_asignacion = Asignacion(
            id_espe=id_espe,
            id_paciente=id_paciente
        )
        
        db.session.add(nueva_asignacion)
        db.session.commit()
        return jsonify({"mensaje": "Paciente asignado correctamente"}), 201

    except ValueError:
        return jsonify({"error": "Los IDs deben ser números enteros"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
# //    

@esp.route('/asignar_paciente/<int:id>', methods=['GET'])
def mostrar_asignacion(id):
    get_esp = Especialista.query.get(id)
    pacientes_no_asignados = Paciente.query.filter(~Paciente.asignaciones.any(id_espe=id)).all()
    return render_template('e_asignar_paciente.html', 
                         get_esp=get_esp,
                         pacientes_disponibles=pacientes_no_asignados)

# Añadir Alimento <
@esp.route('/anadir_alimento/<int:id>', methods=['GET', 'POST'])
def anadir_alimento(id):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()
    
    if request.method == "POST":
        try:
            tipo = request.form['tipo']
            nombre = request.form['nombre']
            cantidad = request.form['cantidad']
            
            nuevo_alimento = Alimento(
                tipo=tipo,
                nombre=nombre,
                cantidad=cantidad
            )
            
            db.session.add(nuevo_alimento)
            db.session.commit()
            flash("Alimento agregado exitosamente", "success")
            
        except Exception as e:
            db.session.rollback()
            flash("Error al agregar el alimento", "danger")
            print(f"Error: {e}")
            
        return redirect(url_for('especialista.inicio', id=id))
    
    # Opciones predefinidas para el tipo
    tipos_alimento = ['Proteina', 'Carbohidrato', 'Grasa', 'Vegetal', 
                     'Fruta', 'Bebida', 'Dulce', 'Otros']
    
    return render_template('e_anadir_alimento.html', 
                         get_esp=get_esp,
                         tipos=tipos_alimento)
# //