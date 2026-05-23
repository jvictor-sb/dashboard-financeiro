from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .extensions import lm
from .utils import gerar_token_recuperacao, verificar_token, atualizar_senha
from auth.model import Usuario
from auth.utils import criar_usuario, buscar_por_email, hash_senha

auth = Blueprint('auth', __name__)

@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar = request.form['confirmar_senha']

        if senha != confirmar:
            return render_template('cadastro.html', erro='As senhas não coincidem')

        if buscar_por_email(email):
            return render_template('cadastro.html', erro='Email já cadastrado')
        
        usuario = Usuario(nome, email, senha)
        criar_usuario(usuario)
        return redirect(url_for('auth.login'))
    return render_template('cadastro.html')

@lm.user_loader
def load_user(email):
    dados = buscar_por_email(email)
    if dados:
        return Usuario(dados['nome'], dados['email'], dados['senha'])
    return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        dados = buscar_por_email(email)
        
        if not dados:
            return render_template('login.html', erro='Email não cadastrado')
        
        if dados['senha'] != hash_senha(senha):
            return render_template('login.html', erro='Senha incorreta')
        
        usuario = Usuario(dados['nome'], dados['email'], dados['senha'])
        login_user(usuario)

        return redirect(url_for('dashboard.index'))
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            return render_template('change_pass.html')
        
        dados = buscar_por_email(email)
        
        if not dados:
            return render_template('change_pass.html', erro="O e-mail informado não está cadastrado")
        
        token = gerar_token_recuperacao(email, dados['senha'])
        link_rec = url_for('auth.password_change', token=token, email=email, _external=True)
        print("\n" + "="*50)
        print(f"LINK DE RECUPERAÇÃO GERADO:\n{link_rec}")
        print("="*50 + "\n")
            
        return redirect(url_for('auth.login'))
    return render_template('change_pass.html')

@auth.route('/password_change', methods=['GET', 'POST'])
def password_change():
    email = request.args.get('email')
    token = request.args.get('token')

    dados = buscar_por_email(email)
    if not dados:
        return redirect(url_for('auth.login'))
    
    email_validado = verificar_token(token, dados['senha'])
    
    if not email_validado:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nova_senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')

        if nova_senha != confirmar_senha:
            return render_template('reset_pass.html', token=token, email=email, erro="As senhas não coincidem. Tente novamente.")

        atualizar_senha(email, nova_senha)
        
        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for('auth.login'))    
    return render_template('reset_pass.html', token=token, email=email)