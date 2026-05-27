from functools import wraps
from flask import session, redirect, url_for, flash
from .models import Usuario, db

# 1º Porteiro: Verifica apenas se a pessoa fez Login (para áreas gerais como Eventos)
def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logado_id' not in session:
            flash("Por favor, faça login para aceder a esta página.")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# 2º Porteiro (O VIP): Verifica se a pessoa tem o Cargo certo (ex: Pastor, Secretário)
def requer_cargo(*cargos_permitidos):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Primeiro, vê se está logado
            if 'usuario_logado_id' not in session:
                return redirect(url_for('auth.login'))
            
            # Vai buscar o utilizador à base de dados para ver o crachá (cargo)
            usuario = db.session.get(Usuario, session['usuario_logado_id'])
            
            # Se não tiver o crachá certo, é barrado e mandado para a homepage
            if not usuario or usuario.cargo not in cargos_permitidos:
                flash("Acesso Negado: Não tens autorização para entrar nesta área.")
                return redirect(url_for('home.homepage'))
            
            # Se tiver autorização, a porta abre!
            return f(*args, **kwargs)
        return decorated_function
    return decorator