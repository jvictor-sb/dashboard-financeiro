from flask import current_app
from itsdangerous import URLSafeTimedSerializer

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