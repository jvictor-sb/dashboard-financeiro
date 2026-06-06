from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .extensions import lm, db
from auth.model import Usuario
from auth import services  

auth = Blueprint('auth', __name__)

@lm.user_loader
def load_user(email):
    usuario = db.session.query(Usuario).filter_by(email=email).first()
    return usuario

@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            services.registrar_usuario(
                request.form['nome'],
                request.form['email'],
                request.form['senha'],
                request.form['confirmar_senha']
            )
            return redirect(url_for('auth.login'))
        except ValueError as e:
            return render_template('cadastro.html', erro=str(e))
    return render_template('cadastro.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            usuario = services.autenticar_usuario(
                request.form['email'],
                request.form['senha']
            )
            login_user(usuario)
            return redirect(url_for('dashboard.index'))
        except ValueError as e:
            return render_template('login.html', erro=str(e))
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        resultado = services.solicitar_recuperacao(
            request.form.get('email', '').strip()
        )
        if not resultado['sucesso']:
            return render_template('change_pass.html', erro=resultado['erro'])

        flash('E-mail de recuperação enviado!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('change_pass.html')

@auth.route('/password_change', methods=['GET', 'POST'])
def password_change():
    if request.method == 'GET':
        email = request.args.get('email')
        token = request.args.get('token', '').replace(' ', '+')

        resultado = services.iniciar_password_change(email, token)
        if not resultado['sucesso']:
            flash(resultado['erro'], 'danger')
            return redirect(url_for('auth.login'))

        return render_template('reset_pass.html', token=token, email=email)

    email = request.form.get('email')
    token = request.form.get('token', '').replace(' ', '+')

    resultado = services.trocar_senha(
        email, token,
        request.form.get('senha'),
        request.form.get('confirmar_senha')
    )

    if not resultado['sucesso']:
        if resultado.get('redirecionar'):
            flash(resultado['erro'], 'danger')
            return redirect(url_for('auth.login'))
        return render_template('reset_pass.html', token=token, email=email, erro=resultado['erro'])

    flash('Senha alterada com sucesso!', 'success')
    return redirect(url_for('auth.login'))