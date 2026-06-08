from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from dashboard import services
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    dados_financeiros = {
        "saldo_total": "R$ 3.450,00",
        "receita_total": "R$ 5.000,00",
        "despesas_totais": "R$ 1.550,00",
        "qtd_transacao": 14
    }
    
    return render_template(
        'index.html', 
        active_page='visao_geral', 
        **dados_financeiros
    )
    
@dashboard.route('/despesas', methods=['GET', 'POST'])
@login_required
def despesas():
    if request.method == 'POST':
            valor = float(request.form['valor'])
            data = request.form['data']
            categoria = request.form['categoria']
            descricao = request.form['descricao']
            origem = request.form['origem'] 
            
            data_objeto = datetime.strptime(data, '%Y-%m-%d').date()
            
            services.adicionar_transacao(valor=valor,data=data_objeto, categoria=categoria, descricao=descricao,origem=origem)
            return redirect(url_for('dashboard.despesas'))
        
    listar_despesas = services.listar_transacoes()
    return render_template('despesas.html', active_page='despesas', despesas=listar_despesas)