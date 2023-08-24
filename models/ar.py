from utils.db import db

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