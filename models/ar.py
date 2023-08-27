from utils.db import db

class AR(db.Model):
    __tablename__ = 'a_r'
    id_comida = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, primary_key=True)
    id_alimento = db.Column(db.Integer, db.ForeignKey('alimento.id_alimento'), primary_key=True)

    comida = db.relationship('Comida', backref='a_r_comida', foreign_keys=[id_comida, id_persona])
    alimento = db.relationship('Alimento', backref='comidas_alimento', foreign_keys=[id_alimento])

    __table_args__ = (
        (db.PrimaryKeyConstraint('id_comida', 'id_persona', 'id_alimento')),
        db.ForeignKeyConstraint(['id_comida', 'id_persona'], ['comida.id_comida', 'comida.id_persona']),
    )

    def __init__(self, id_comida, id_persona, id_alimento):
        self.id_comida = id_comida
        self.id_persona = id_persona
        self.id_alimento = id_alimento
