from flask import render_template, request, redirect, url_for
from models import Usuario
from db import db

def init_routes(app):


    # REGISTER PAGE
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip()
            senha = request.form.get("senha", "").strip()

            # Validação de campos
            if not nome or not email or not senha:
                return "Erro: Preencha todos os campos!"

            # Verificar duplicados
            if Usuario.query.filter_by(nome=nome).first():
                return f"Erro: O nome '{nome}' já está cadastrado!"
            if Usuario.query.filter_by(email=email).first():
                return f"Erro: O email '{email}' já está cadastrado!"

            # Criar novo usuário
            novo_usuario = Usuario(nome=nome, email=email, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()

            # Redireciona para login após cadastro
            return redirect(url_for("login"))

        # GET → exibe formulário
        return render_template("registerpage.html")

    # LOGIN PAGE
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            senha = request.form.get("senha", "").strip()

            # Validação simples
            if not email or not senha:
                return "Erro: Preencha todos os campos!"

            # Verificar usuário no banco
            usuario = Usuario.query.filter_by(email=email, senha=senha).first()
            if usuario:
                # Usuário encontrado → redireciona para homepage
                return redirect(url_for("homepage"))
            else:
                return "Erro: Email ou senha incorretos!"

        # GET → exibe formulário
        return render_template("loginpage.html")


    # HOMEPAGE
    @app.route("/")
    def homepage():
        return render_template("homepage.html")
