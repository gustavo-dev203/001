from flask import Blueprint
from ..decorators import requer_cargo # Voltámos aos '..' !

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route("/")
@requer_cargo("Pastor") 
def painel_pastor():
    return "<h1>Gabinete do Pastor</h1><p>Bem-vindo, Reverendo. Se estás a ler isto, o nosso sistema de segurança RBAC funciona perfeitamente!</p>"