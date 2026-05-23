import json
import os
import hashlib
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

caminho = os.path.join(os.path.dirname(__file__), '..', 'databases', 'usuarios.json')

def hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def ler_usuarios():
    if not os.path.exists(caminho):
        return []
    
    with open(caminho, 'r') as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(caminho, 'w') as f:
        json.dump(usuarios, f, indent=4)

def atualizar_senha(email, nova_senha):
    usuarios = ler_usuarios()
    for u in usuarios:
        if u['email'] == email:
            u['senha'] = hash_senha(nova_senha)
            salvar_usuarios(usuarios)
            return True
    return False

def criar_usuario(usuario):
    usuarios = ler_usuarios()
    usuario.senha = hash_senha(usuario.senha)
    usuarios.append(usuario.to_dict())
    salvar_usuarios(usuarios)

def buscar_por_email(email):
    usuarios = ler_usuarios()
    for u in usuarios:
        if u['email'] == email:
            return u
    return None

def gerar_token_recuperacao(email, senha_atual):
    chave = current_app.secret_key + senha_atual
    serializador = URLSafeTimedSerializer(chave)
    return serializador.dumps(email, salt='recuperar-senha')

def verificar_token(token, senha_atual, expira=900):
    chave = current_app.secret_key + senha_atual
    serializador = URLSafeTimedSerializer(chave)
    try:
        email = serializador.loads(token, salt='recuperar-senha', max_age=expira)
        return email
    except:
        return None