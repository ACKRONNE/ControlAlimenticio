from utils.db import db
from sqlalchemy import CheckConstraint

class Comida(db.Model):
    __tablename__ = 'comida'
    id_comida = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'), primary_key=True)
    tipo = db.Column(db.String(1), nullable=False)
    satisfaccion = db.Column(db.String(11), nullable=True)
    comentario = db.Column(db.Text, nullable=True)

    persona = db.relationship('Persona', backref='comida_persona', foreign_keys=[id_persona])

    __table_args__ = (
        (db.PrimaryKeyConstraint('id_comida', 'id_persona')),
        (CheckConstraint("satisfaccion IN ('super','bien','normal','no muy bien','mal','cansado')", name='comida_satis_check')),
        (CheckConstraint("tipo IN ('d','a','c','m')", name='receta_tipo_check')),
    )

    def __init__(self, id_persona, tipo, satisfaccion=None, comentario=None):
        self.id_persona = id_persona
        self.tipo = tipo
        self.satisfaccion = satisfaccion
        self.comentario = comentario