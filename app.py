from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def inicial():
    return 'Hello World!'
    

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar = request.form['confirmar_senha']
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)