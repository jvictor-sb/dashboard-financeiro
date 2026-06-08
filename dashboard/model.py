from extensions import db
class Transacao(db.Model):
        __tablename__ = 'transacao'
        id = db.Column(db.Integer, primary_key=True)
        valor = db.Column(db.Float, default=0.00, nullable=False)
        data = db.Column(db.DateTime, nullable=False)
        categoria = db.Column(db.String(80), nullable=False)
        descricao = db.Column(db.String(80), nullable=False)
        origem = db.Column(db.String(80), nullable=False)
