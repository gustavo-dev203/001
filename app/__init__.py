import os
from flask import Flask
from .db import db

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
    # Garante que a app não inicia sem uma chave secreta por segurança
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-provisoria-de-desenvolvimento')
    
    if not os.getenv('SECRET_KEY') and not app.debug:
        print("AVISO: SECRET_KEY não configurada no ambiente!")
    
    db.init_app(app)
    
    # ==========================================
    # REGISTO DOS BLUEPRINTS (As nossas "Salas")
    # ==========================================
    
    # 1. Autenticação
    from .blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # 2. Principal (Homepage e Eventos)
    from .blueprints.home import home_bp
    app.register_blueprint(home_bp)
    
    # 3. Painel Administrativo (Conselho/Pastor)
    from .blueprints.admin import admin_bp
    app.register_blueprint(admin_bp)

    from .blueprints.sociedades import sociedades_bp
    app.register_blueprint(sociedades_bp)
    
    return app