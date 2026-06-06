from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin, db.Model):
    __tablename__ = 'users'

    nome = db.Column(db.String(120), nullable=False)
    email =db.Column(db.String(120), primary_key=True)
    senha_hash = db.Column(db.String(), nullable=False)
    
    def get_id(self):
        return str(self.email)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    