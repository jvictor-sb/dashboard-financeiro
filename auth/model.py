from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def get_id(self):
        return self.email
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha
        }
        