from utils.db import db

class HistComida(db.Model):
    __tablename__ = 'hist_comida'
    id_comida = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, primary_key=True)
    fecha_ini = db.Column(db.Date, primary_key=True)
    fecha_fin = db.Column(db.Date)

    comida = db.relationship('Comida', backref='hist_comida', foreign_keys=[id_comida, id_persona])

    __table_args__ = (
        db.PrimaryKeyConstraint('id_comida', 'id_persona' , 'fecha_ini'),
        db.ForeignKeyConstraint(['id_comida', 'id_persona'], ['comida.id_comida', 'comida.id_persona']),

    )

    def __init__(self, id_comida, id_persona, fecha_ini, fecha_fin=None):
        self.id_comida = id_comida
        self.id_persona = id_persona
        self.fecha_ini = fecha_ini
        self.fecha_fin = fecha_fin
