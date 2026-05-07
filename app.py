from flask import Flask, render_template, request
from auth.routes import auth

app = Flask(__name__)

@app.route('/')
def inicial():
    return 'Hello World!'
    
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)