from flask import Flask
from auth.routes import auth
from inicio.routes import inicio

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

app.register_blueprint(auth)
app.register_blueprint(inicio)

if __name__ == '__main__':
    app.run(debug=True)