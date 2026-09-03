from dashboard.model import Transacao
from extensions import db
from sqlalchemy import func
from datetime import date

MESES_PT = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

def adicionar_transacao(user_email, valor, data, categoria, descricao, tipo):
    transacao = Transacao(user_email=user_email, valor=valor, data=data, categoria=categoria, descricao=descricao, tipo=tipo)
    db.session.add(transacao)
    db.session.commit()
    
def listar_transacoes(user_email):
    return Transacao.query.filter_by(user_email=user_email).order_by(Transacao.data.desc()).all()

def listar_transacoes_por_tipo(user_email, tipo):
    return Transacao.query.filter_by(user_email=user_email, tipo=tipo).order_by(Transacao.data.desc()).all()

def listar_transacoes_recentes(user_email, limite=6):
    return Transacao.query.filter_by(user_email=user_email).order_by(Transacao.data.desc()).limit(limite).all()
    
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

def _ultimos_6_meses():
    hoje = date.today()

    meses = []
    for i in range(5, -1, -1):
        mes = hoje.month - i
        ano = hoje.year
        while mes <= 0:
            mes += 12
            ano -= 1
        meses.append((ano, mes))

    labels = [f"{MESES_PT[mes]}/{ano}" for ano, mes in meses]
    inicio = date(meses[0][0], meses[0][1], 1)

    return meses, labels, inicio

def receitas_despesas_ultimos_6_meses(user_email):
    meses, labels, inicio = _ultimos_6_meses()

    receitas = [0.0] * 6
    despesas = [0.0] * 6

    resultados = (
        db.session.query(
            func.extract('year', Transacao.data).label('ano'),
            func.extract('month', Transacao.data).label('mes'),
            Transacao.tipo,
            func.sum(Transacao.valor)
        )
        .filter(
            Transacao.user_email == user_email,
            Transacao.data >= inicio
        )
        .group_by('ano', 'mes', Transacao.tipo)
        .all()
    )

    indice_por_mes = {(ano, mes): idx for idx, (ano, mes) in enumerate(meses)}

    for ano, mes, tipo, total in resultados:
        idx = indice_por_mes.get((int(ano), int(mes)))
        if idx is None:
            continue
        if tipo == 'receita':
            receitas[idx] = float(total)
        elif tipo == 'despesa':
            despesas[idx] = float(total)

    return {'labels': labels, 'receitas': receitas, 'despesas': despesas}

def despesas_ultimos_6_meses(user_email):
    meses, labels, inicio = _ultimos_6_meses()

    despesas = [0.0] * 6

    resultados = (
        db.session.query(
            func.extract('year', Transacao.data).label('ano'),
            func.extract('month', Transacao.data).label('mes'),
            func.sum(Transacao.valor)
        )
        .filter(
            Transacao.user_email == user_email,
            Transacao.tipo == 'despesa',
            Transacao.data >= inicio
        )
        .group_by('ano', 'mes')
        .all()
    )

    indice_por_mes = {(ano, mes): idx for idx, (ano, mes) in enumerate(meses)}

    for ano, mes, total in resultados:
        idx = indice_por_mes.get((int(ano), int(mes)))
        if idx is None:
            continue
        despesas[idx] = float(total)

    return {'labels': labels, 'despesas': despesas}

def total_por_categoria(user_email, tipo):
    resultados = (
        db.session.query(Transacao.categoria, func.sum(Transacao.valor))
        .filter(Transacao.user_email == user_email, Transacao.tipo == tipo)
        .group_by(Transacao.categoria)
        .all()
    )

    labels = [categoria.capitalize() for categoria, _ in resultados]
    valores = [float(total) for _, total in resultados]

    return {'labels': labels, 'valores': valores}