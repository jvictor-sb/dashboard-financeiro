from auth.model import Usuario
from auth.utils import criar_usuario, buscar_por_email, hash_senha
from auth.utils import gerar_token_recuperacao, verificar_token, atualizar_senha
from flask import url_for
from flask_mail import Message
from auth.extensions import mail

def solicitar_recuperacao(email):
    if not email:
        return {'sucesso': False, 'erro': 'Informe um e-mail.'}

    dados = buscar_por_email(email)
    if not dados:
        return {'sucesso': False, 'erro': 'O e-mail informado não está cadastrado.'}

    token = gerar_token_recuperacao(email, dados['senha'])
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
    if senha != confirmar:
        raise ValueError("As senhas não coincidem")

    if buscar_por_email(email):
        raise ValueError("Email já cadastrado")

    usuario = Usuario(nome, email, senha)
    criar_usuario(usuario)

def autenticar_usuario(email, senha):
    dados = buscar_por_email(email)

    if not dados:
        raise ValueError("Email não cadastrado")

    if dados['senha'] != hash_senha(senha):
        raise ValueError("Senha incorreta")

    return Usuario(dados['nome'], dados['email'], dados['senha'])

def iniciar_password_change(email, token):
    dados = buscar_por_email(email)
    if not dados or not verificar_token(token, dados['senha']):
        return {'sucesso': False, 'erro': 'Link inválido ou expirado.'}
    return {'sucesso': True}

def trocar_senha(email, token, nova_senha, confirmar):
    if nova_senha != confirmar:
        return {'sucesso': False, 'erro': 'As senhas não coincidem.'}

    dados = buscar_por_email(email)
    if not dados or not verificar_token(token, dados['senha']):
        return {'sucesso': False, 'erro': 'Link inválido ou expirado.', 'redirecionar': True}

    atualizar_senha(email, nova_senha)
    return {'sucesso': True}
