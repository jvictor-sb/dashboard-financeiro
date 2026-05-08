import json
import os
import hashlib

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