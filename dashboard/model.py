from extensions import db
class Transacao(db.Model):
        __tablename__ = 'transacao'
        id = db.Column(db.Integer, primary_key=True)
        valor = db.Column(db.Numeric(precision=16, scale=2))
        data = db.Column(db.DateTime)
        categoria = db.Column(db.String(40))
        descricao = db.Column(db.String(80))
        origem = db.Column(db.String(80))
        tipo = db.Column(db.String(20))