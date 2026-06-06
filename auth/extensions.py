from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'auth.login'
lm.login_message = ''
mail = Mail()