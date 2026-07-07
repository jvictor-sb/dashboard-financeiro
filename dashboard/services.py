from dashboard.model import Transacao
from extensions import db
from sqlalchemy import func

def adicionar_transacao(user_email, valor, data, categoria, descricao, origem, tipo):
    transacao = Transacao(user_email=user_email, valor=valor, data=data, categoria=categoria, descricao=descricao, origem=origem, tipo=tipo)
    db.session.add(transacao)
    db.session.commit()
    
def listar_transacoes(user_email):
    return Transacao.query.filter_by(user_email=user_email).order_by(Transacao.data.desc()).all()

def listar_transacoes_por_tipo(user_email, tipo):
    return Transacao.query.filter_by(user_email=user_email, tipo=tipo).order_by(Transacao.data.desc()).all()
    
def total_despesas(user_email):
    resultado = db.session.query(func.sum(Transacao.valor)).filter(
        Transacao.user_email == user_email,
        Transacao.tipo == 'despesa'
    ).scalar()
    return resultado or 0.0

def total_receitas(user_email):
    resultado = db.session.query(func.sum(Transacao.valor)).filter(
        Transacao.user_email == user_email,
        Transacao.tipo == 'receita'
    ).scalar()
    return resultado or 0.0

def total_transacao(user_email):
    resultado = Transacao.query.filter_by(user_email=user_email).count()
    return resultado

def deletar_transacao(id, user_email):
    transacao = Transacao.query.filter_by(id=id, user_email=user_email).first_or_404()
    db.session.delete(transacao)
    db.session.commit()