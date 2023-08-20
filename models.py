from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

app = Flask(__name__)

app.secret_key = "123456"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/control_alimenticio'
app.config['SQLALCHEMY TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

# ---

class Receta(db.Model):
    __tablename__ = 'receta'
    id_receta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(1), nullable=False)
    
    __table_args__ = (
        (CheckConstraint("tipo IN ('d','a','c','m')", name='receta_tipo_check')),
    )

    def __init__(self, id_receta, tipo):
        self.id_receta = id_receta
        self.tipo = tipo

# ---

class Alimento(db.Model):
    __tablename__ = 'alimento'
    id_alimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(13), nullable=False)
    nombre = db.Column(db.Text, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        (CheckConstraint("tipo IN ('p','c','v','g','f','b','o')", name='alimento_tipo_check')),
    )

    def __init__(self, id_alimento, tipo, nombre, cantidad):
        self.id_alimento = id_alimento
        self.tipo = tipo
        self.nombre = nombre
        self.cantidad = cantidad

# ---

class Persona(db.Model):
    __tablename__ = 'persona'
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(15), nullable=False)
    apellido = db.Column(db.String(15), nullable=False)
    tipo = db.Column(db.String(1), nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    correo = db.Column(db.Text, nullable=False, unique=True)
    direccion = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.Numeric(12), nullable=False)
    contraseña = db.Column(db.Text, nullable=False)
    fecha_nac = db.Column(db.Numeric(2), nullable=False)
    especialidad = db.Column(db.String(30))
    id_espe = db.Column(db.Integer, db.ForeignKey('persona.id_persona'))

    especialidad_persona = db.relationship('Persona', backref='persona_especialidad', remote_side=[id_persona])

    __table_args__ = (
        (CheckConstraint("tipo IN ('p', 'e')", name='persona_tipo_check')),
        (CheckConstraint("sexo IN ('m', 'f')", name='persona_sexo_check')),
    )

    def __init__(self, id_persona, nombre, apellido, tipo, sexo, correo, direccion, telefono, contraseña, fecha_nac, especialidad, id_espe):
        self.id_persona = id_persona
        self.nombre = nombre
        self.apellido = apellido
        self.tipo = tipo
        self.sexo = sexo
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
        self.contraseña = contraseña
        self.fecha_nac = fecha_nac
        self.especialidad = especialidad
        self.id_espe = id_espe
        
# ---

class HistReceta(db.Model):
    __tablename__ = 'hist_receta'
    id_receta = db.Column(db.Integer, db.ForeignKey("receta.id_receta"), primary_key=True)
    fecha_ini = db.Column(db.Date, primary_key=True)
    fecha_fin = db.Column(db.Date)

    receta_hist = db.relationship('Receta', backref='receta_hist', foreign_keys=[id_receta])

    __table_args__ = (
        db.PrimaryKeyConstraint('id_receta', 'fecha_ini'),
    )

    def __init__(self, id_receta, fecha_ini, fecha_fin=None):
        self.id_receta = id_receta
        self.fecha_ini = fecha_ini
        self.fecha_fin = fecha_fin

# ---
        
class DetComida(db.Model):
    __tablename__ = 'det_comida'
    id_receta = db.Column(db.Integer, db.ForeignKey('receta.id_receta'), primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), primary_key=True)
    satisfaccion = db.Column(db.String(11), nullable=False)
    comentario = db.Column(db.Text)

    receta = db.relationship('Receta', backref='detallec_receta', foreign_keys=[id_receta])
    cliente = db.relationship('Persona', backref='detallec_cliente', foreign_keys=[id_cliente])

    __table_args__ = (
        (db.PrimaryKeyConstraint('id_receta', 'id_cliente')),
        (CheckConstraint("satisfaccion IN ('super','bien','normal','no muy bien','mal','cansado')", name='detcomida_satis_check')),
    )

    def __init__(self, id_receta, id_cliente, satisfaccion=None, comentario=None):
        self.id_receta = id_receta
        self.id_cliente = id_cliente
        self.satisfaccion = satisfaccion
        self.comentario = comentario

# ---

class AR(db.Model):
    __tablename__ = 'a_r'
    id_receta = db.Column(db.Integer, db.ForeignKey('receta.id_receta'), primary_key=True)
    id_alimento = db.Column(db.Integer, db.ForeignKey('alimento.id_alimento'), primary_key=True)

    receta = db.relationship('Receta', backref='alimentos_receta', foreign_keys=[id_receta])
    alimento = db.relationship('Alimento', backref='recetas_alimento', foreign_keys=[id_alimento])

    __table_args__ = (
        (db.PrimaryKeyConstraint('id_receta', 'id_alimento')),
    )

    def __init__(self, id_receta, id_alimento):
        self.id_receta = id_receta
        self.id_alimento = id_alimento

with app.app_context():
    db.create_all()