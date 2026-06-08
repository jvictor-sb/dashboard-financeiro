from dashboard.model import Transacao
from extensions import db

def adicionar_transacao(valor, data, categoria, descricao, origem):
    transacao = Transacao(valor=valor, data=data, categoria=categoria, descricao=descricao, origem=origem)
    db.session.add(transacao)
    db.session.commit()
    
def listar_transacoes():
    return Transacao.query.order_by(Transacao.data.desc()).all()