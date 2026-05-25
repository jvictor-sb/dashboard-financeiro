from flask_login import LoginManager
from flask_mail import Mail

lm = LoginManager()
lm.login_view = 'auth.login'
lm.login_message = ''
mail = Mail()