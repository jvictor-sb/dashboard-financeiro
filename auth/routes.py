from flask import Blueprint, render_template, request, redirect, url_for, session
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

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = buscar_por_email(email)

        if usuario and usuario['senha'] == hash_senha(senha):
            session['usuario'] = usuario['email']
            return redirect(url_for('dashboard.index'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('auth.login'))
