from auth.model import Usuario
from auth.utils import gerar_token_recuperacao, verificar_token
from flask import url_for
from flask_mail import Message
from auth.extensions import mail, db



def solicitar_recuperacao(email):
    dados = db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one_or_none()
    if not dados:
        return {'sucesso': False, 'erro': 'O e-mail informado não está cadastrado.'}

    token = gerar_token_recuperacao(email, dados.senha_hash)
    link = url_for('auth.password_change', token=token, email=email, _external=True)

    msg = Message(
        subject='Recuperação de senha',
        recipients=[email]
    )
    msg.body = f'Clique no link para redefinir sua senha: {link}'
    msg.html = f'''
        <h2>Recuperação de senha</h2>
        <p>Clique no botão abaixo para redefinir sua senha:</p>
        <a href="{link}" style="
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
        ">Redefinir senha</a>
        <p>O link expira em 15 minutos.</p>
        <p>Se você não solicitou a recuperação, ignore este e-mail.</p>
    '''

    mail.send(msg)
    return {'sucesso': True}



def registrar_usuario(nome, email, senha, confirmar):
    usuario = db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one_or_none()
    if usuario:
        raise ValueError("Email já cadastrado")
    
    if senha != confirmar:
        raise ValueError("As senhas não coincidem")
    
    usuario = Usuario(nome=nome, email=email)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()


def autenticar_usuario(email, senha):
    dados = db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one_or_none()

    if not dados:
        raise ValueError("Email não cadastrado")

    if not dados.verificar_senha(senha):
        raise ValueError("Senha incorreta")

    return dados

def iniciar_password_change(email, token):
    dados = db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one_or_none()
    if not dados or not verificar_token(token, dados.senha_hash):
        return {'sucesso': False, 'erro': 'Link inválido ou expirado.'}
    return {'sucesso': True}

def trocar_senha(email, token, nova_senha, confirmar):
    if nova_senha != confirmar:
        return {'sucesso': False, 'erro': 'As senhas não coincidem.'}

    dados = db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one_or_none()
    if not dados or not verificar_token(token, dados.senha_hash):
        return {'sucesso': False, 'erro': 'Link inválido ou expirado.', 'redirecionar': True}
    
    dados.set_senha(nova_senha)
    db.session.commit()