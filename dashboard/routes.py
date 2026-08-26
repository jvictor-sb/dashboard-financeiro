from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user 
from dashboard import services
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    despesas_totais = services.total_despesas(user_email=current_user.email)
    receitas_totais = services.total_receitas(user_email=current_user.email)
    saldo = float(receitas_totais) - float(despesas_totais)
    qtd_transacao = services.total_transacao(user_email=current_user.email)
    
    listar_transacao = services.listar_transacoes_recentes(user_email=current_user.email)
    
    grafico_receitas_despesas = services.receitas_despesas_ultimos_6_meses(user_email=current_user.email)
    grafico_categoria_despesas = services.total_por_categoria(user_email=current_user.email, tipo='despesa')
    grafico_categoria_receitas = services.total_por_categoria(user_email=current_user.email, tipo='receita')
    
    return render_template(
        'index.html', 
        active_page='visao_geral', 
        despesas_totais=despesas_totais,
        receitas_totais=receitas_totais,
        saldo_total=saldo,
        qtd_transacao=qtd_transacao,
        transacoes_recentes = listar_transacao,
        grafico_receitas_despesas=grafico_receitas_despesas,
        grafico_categoria_despesas=grafico_categoria_despesas,
        grafico_categoria_receitas=grafico_categoria_receitas
    )
    
@dashboard.route('/despesas', methods=['GET', 'POST'])
@login_required
def despesas():
    if request.method == 'POST':
        valor = float(request.form['valor'])
        data = request.form['data']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        
        data_objeto = datetime.strptime(data, '%Y-%m-%d').date()
        
        services.adicionar_transacao(
            user_email=current_user.email, 
            valor=valor,
            data=data_objeto, 
            categoria=categoria, 
            descricao=descricao,
            tipo='despesa'
        )
        return redirect(url_for('dashboard.despesas'))
        
    listar_despesas = services.listar_transacoes_por_tipo(user_email=current_user.email, tipo='despesa')
    despesas_totais = services.total_despesas(user_email=current_user.email)
    transacoes_despesas = len(listar_despesas)
    
    return render_template('despesas.html', active_page='despesas', despesas=listar_despesas, despesas_totais=despesas_totais, transacoes_despesas=transacoes_despesas)

@dashboard.route('/despesas/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_despesa(id):
    services.deletar_transacao(id, current_user.email) 
    return redirect(url_for('dashboard.despesas'))

@dashboard.route('/receitas', methods=['GET', 'POST'])
@login_required
def receitas():
    if request.method == 'POST':
        valor = float(request.form['valor'])
        data = request.form['data']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        
        data_objeto = datetime.strptime(data, '%Y-%m-%d').date()
        
        services.adicionar_transacao(
            user_email=current_user.email, 
            valor=valor,
            data=data_objeto, 
            categoria=categoria, 
            descricao=descricao,
            tipo='receita'
        )
        return redirect(url_for('dashboard.receitas'))

    listar_receitas = services.listar_transacoes_por_tipo(user_email=current_user.email, tipo='receita')
    receitas_totais = services.total_receitas(user_email=current_user.email) 
    transacoes_receitas = len(listar_receitas)
    
    return render_template('receitas.html', active_page='receitas', receitas=listar_receitas, receitas_totais=receitas_totais, transacoes_receitas=transacoes_receitas)

@dashboard.route('/receitas/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_receitas(id):
    services.deletar_transacao(id, current_user.email) 
    return redirect(url_for('dashboard.receitas'))