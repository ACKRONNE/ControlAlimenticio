from utils.db import db
from sqlalchemy import CheckConstraint

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