from dashboard.model import Transacao
from extensions import db
from sqlalchemy import func

def adicionar_transacao(valor, data, categoria, descricao, origem, tipo):
    transacao = Transacao(valor=valor, data=data, categoria=categoria, descricao=descricao, origem=origem, tipo=tipo)
    db.session.add(transacao)
    db.session.commit()
    
def listar_transacoes():
    return Transacao.query.order_by(Transacao.data.desc()).all()

def listar_transacoes_por_tipo(tipo):
    return Transacao.query.filter_by(tipo=tipo).order_by(Transacao.data.desc()).all()
    
def total_despesas():
    resultado = db.session.query(func.sum(Transacao.valor)).filter(Transacao.tipo == 'despesa').scalar()
    return resultado or 0.0

def total_receitas():
    resultado = db.session.query(func.sum(Transacao.valor)).filter(Transacao.tipo == 'receita').scalar()
    return resultado or 0.0

def total_transacao():
    resultado = Transacao.query.count()
    return resultado

def deletar_transacao(id):
    transacao = Transacao.query.get_or_404(id)
    db.session.delete(transacao)
    db.session.commit()
    