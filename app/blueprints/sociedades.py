from flask import Blueprint, render_template
from ..models import Sociedade, Usuario
from ..decorators import login_obrigatorio, db

sociedades_bp = Blueprint('sociedades', __name__, url_prefix='/sociedades')

@sociedades_bp.route('/')
@login_obrigatorio
def listar_sociedades():
    # Busca todas as sociedades (UMP, UPA...) que criamos no seed.py
    todas_sociedades = db.session.execute(db.select(Sociedade)).scalars().all()
    return render_template('sociedades_lista.html', sociedades=todas_sociedades)

@sociedades_bp.route('/<int:id>')
@login_obrigatorio
def detalhes_sociedade(id):
    sociedade = db.session.get(Sociedade, id) or render_template('404.html'), 404
    # Aqui buscaremos os membros vinculados a esta sociedade específica
    membros = db.session.execute(db.select(Usuario).filter_by(sociedade_id=id)).scalars().all()
    return render_template('sociedade_perfil.html', sociedade=sociedade, membros=membros)