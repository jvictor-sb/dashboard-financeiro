from flask import render_template

def registrar_erros(app):
    @app.errorhandler(404)
    def not_found(e):
        return "404 - Página não encontrada", 404

    @app.errorhandler(500)
    def internal_error(e):
        return "500 - Erro interno", 500