from flask import Blueprint, render_template
from flask_login import login_required

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
    
