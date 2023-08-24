from utils.db import db
from sqlalchemy import CheckConstraint

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