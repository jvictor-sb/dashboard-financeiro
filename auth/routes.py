from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .extensions import lm
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

@auth.route('/password_reset')
def reset_password():
    return render_template('change_pass.html')