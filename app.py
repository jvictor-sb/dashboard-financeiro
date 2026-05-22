from flask import Flask
from auth.routes import auth
from auth.extensions import lm
from dashboard.routes import dashboard

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

lm.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(dashboard)

if __name__ == '__main__':
    app.run(debug=True)