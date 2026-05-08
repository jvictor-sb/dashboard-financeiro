from flask import Blueprint, render_template

inicio = Blueprint('inicio', __name__)

@inicio.route('/inicio')
def index():
    return render_template('index.html')