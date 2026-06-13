from dashboard.model import Transacao
from extensions import db
from sqlalchemy import func

def adicionar_transacao(valor, data, categoria, descricao, origem, tipo):
    transacao = Transacao(valor=valor, data=data, categoria=categoria, descricao=descricao, origem=origem, tipo=tipo)
    db.session.add(transacao)
    db.session.commit()
    
def listar_transacoes():
    return Transacao.query.order_by(Transacao.data.desc()).all()

def total_despesas():
    resultado = db.session.query(func.sum(Transacao.valor)).filter(Transacao.tipo == 'despesa').scalar()
    return resultado or 0.00

def deletar_transacao(id):
    transacao = Transacao.query.get_or_404(id)
    db.session.delete(transacao)
    db.session.commit()