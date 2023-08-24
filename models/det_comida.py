from utils.db import db
from sqlalchemy import CheckConstraint

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