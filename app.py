import os
from flask import Flask
from dotenv import load_dotenv
from auth.routes import auth
from auth.extensions import lm, mail
from dashboard.routes import dashboard
from auth.errors import registrar_erros

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

app.config['MAIL_SERVER']          = 'smtp.gmail.com'
app.config['MAIL_PORT']            = 587
app.config['MAIL_USE_TLS']         = True
app.config['MAIL_USE_SSL']         = False
app.config['MAIL_USERNAME']        = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']        = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER']  = os.environ.get('MAIL_USERNAME')

mail.init_app(app)
lm.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(dashboard)
registrar_erros(app)

if __name__ == '__main__':
    app.run(debug=True)