from flask import Blueprint, render_template, session, redirect, url_for

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
        
    return render_template('index.html')