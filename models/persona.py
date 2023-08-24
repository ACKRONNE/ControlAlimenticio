from utils.db import db
from sqlalchemy import CheckConstraint

class Persona(db.Model):
    __tablename__ = 'persona'
    id_persona = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(15), nullable=False)
    apellido = db.Column(db.String(15), nullable=False)
    tipo = db.Column(db.String(1), nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    correo = db.Column(db.Text, nullable=False, unique=True)
    direccion = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.Numeric(12), nullable=False)
    contraseña = db.Column(db.Text, nullable=False)
    fecha_nac = db.Column(db.Date, nullable=True)
    especialidad = db.Column(db.String(30), nullable=True)
    id_espe = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), nullable=True)

    especialidad_persona = db.relationship('Persona', backref='persona_especialidad', remote_side=[id_persona])

    __table_args__ = (
        (CheckConstraint("tipo IN ('p', 'e')", name='persona_tipo_check')),
        (CheckConstraint("sexo IN ('m', 'f')", name='persona_sexo_check')),
    )

    def __init__(self, nombre, apellido, tipo, sexo, correo, direccion, telefono, contraseña, fecha_nac, especialidad, id_espe):
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
        