from utils.db import db

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