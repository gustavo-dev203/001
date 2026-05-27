from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from ..models import Evento
from ..db import db
from ..decorators import login_obrigatorio

# Criamos a nossa "Sala" principal
home_bp = Blueprint('home', __name__)

@home_bp.route("/")
def homepage():
    # Vai buscar todos os eventos ao banco de dados
    todos_eventos = db.session.execute(db.select(Evento)).scalars().all()
    return render_template("homepage.html", eventos=todos_eventos)

@home_bp.route("/novo_evento", methods=["GET", "POST"])
@login_obrigatorio
def novo_evento():
    hoje = date.today()

    if request.method == "POST":
        titulo = request.form.get("titulo")
        data_str = request.form.get("data")
        hora = request.form.get("hora")
        descricao = request.form.get("descricao")

        data_evento = datetime.strptime(data_str, '%Y-%m-%d').date()

        if data_evento < hoje:
            flash("Erro: Não podes criar eventos numa data que já passou!")
            return redirect(url_for("home.novo_evento"))

        evento_criado = Evento(titulo=titulo, data=data_str, hora=hora, descricao=descricao)
        db.session.add(evento_criado)
        db.session.commit()

        return redirect(url_for("home.homepage"))

    return render_template("novo_evento.html", data_hoje=hoje.strftime('%Y-%m-%d'))