from utils.db import db

class HistComida(db.Model):
    __tablename__ = 'hist_comida'
    id_comida = db.Column(db.Integer, db.ForeignKey("comida.id_comida"), primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey("persona.id_persona"), primary_key=True)
    fecha_ini = db.Column(db.Date, primary_key=True)
    fecha_fin = db.Column(db.Date)

    persona_hist = db.relationship('Persona', backref='persona_hist', foreign_keys=[id_persona])
    comida_hist = db.relationship('Comida', backref='comida_hist', foreign_keys=[id_comida])

    __table_args__ = (
        db.PrimaryKeyConstraint('id_comida', 'fecha_ini'),
    )

    def __init__(self, id_comida, id_persona, fecha_ini, fecha_fin=None):
        self.id_comida = id_comida
        self.id_persona = id_persona
        self.fecha_ini = fecha_ini
        self.fecha_fin = fecha_fin