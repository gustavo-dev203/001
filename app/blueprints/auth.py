from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import Usuario
from ..db import db

# Criamos o nosso Blueprint (A nossa "Sala" de autenticação)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        if not nome or not email or not senha:
            return "Erro: Preencha todos os campos!"

        if Usuario.query.filter_by(nome=nome).first():
            return f"Erro: O nome '{nome}' já está cadastrado!"
        if Usuario.query.filter_by(email=email).first():
            return f"Erro: O email '{email}' já está cadastrado!"

        senha_criptografada = generate_password_hash(senha)

        novo_usuario = Usuario(nome=nome, email=email, senha=senha_criptografada)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for("auth.login")) # Nota: Agora chamamos 'auth.login'

    return render_template("registerpage.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    print(f"Tentativa de login com: {request.form.get('email')}")
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_logado_id'] = usuario.id
            return redirect(url_for("home.homepage")) # Vamos criar o 'home' em breve!
        else:
            flash("E-mail ou senha incorretos.")
            return redirect(url_for("auth.login"))

    return render_template("loginpage.html")

@auth_bp.route("/logout")
def logout():
    session.pop('usuario_logado_id', None)
    return redirect(url_for("auth.login"))