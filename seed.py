from app import create_app
from app.db import db
from app.models import Usuario, Sociedade, Departamento
from werkzeug.security import generate_password_hash

# Inicializa o motor da app para podermos mexer na base de dados
app = create_app()

def plantar_semente():
    with app.app_context():
        # Verifica se já existem sociedades para não criar em duplicado
        if Sociedade.query.first():
            print("A base de dados já tem informações! Abortando a semente.")
            return

        print("A plantar a semente inicial... 🌱")

        # 1. Criar as Sociedades Internas da IPB
        sociedades = [
            Sociedade(nome="União de Mocidade Presbiteriana", sigla="UMP"),
            Sociedade(nome="União Presbiteriana de Adolescentes", sigla="UPA"),
            Sociedade(nome="Sociedade Auxiliadora Feminina", sigla="SAF"),
            Sociedade(nome="União Presbiteriana de Homens", sigla="UPH"),
            Sociedade(nome="União de Crianças Presbiterianas", sigla="UCP")
        ]
        db.session.bulk_save_objects(sociedades)

        # 2. Criar os Departamentos
        departamentos = [
            Departamento(nome="Escola Bíblica Dominical (EBD)"),
            Departamento(nome="Ministério de Louvor"),
            Departamento(nome="Junta Diaconal")
        ]
        db.session.bulk_save_objects(departamentos)

        # 3. Criar a Conta do Pastor (Super Admin)
        senha_criptografada = generate_password_hash("123456") # Senha provisória
        pastor = Usuario(
            nome="Pastor Titular",
            email="pastor@igreja.com",
            senha=senha_criptografada,
            cargo="Pastor" # Este é o cargo que lhe dará poder total na Fase 3!
        )
        db.session.add(pastor)

        # Guarda tudo na base de dados
        db.session.commit()
        print("Semente plantada com sucesso! 🚀 As sociedades, departamentos e a conta do Pastor foram criados.")

if __name__ == "__main__":
    plantar_semente()