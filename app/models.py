from .db import db
from datetime import datetime, timezone

# ==========================================
# 1. USUÁRIOS E CONTROLE DE ACESSO (RBAC)
# ==========================================
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True) 
    senha = db.Column(db.String(255), nullable=False) 
    
    # --- Regras da IPB (RBAC) ---
    cargo = db.Column(db.String(50), default='Membro') # Ex: Pastor, Presidente, Secretário, Conselheiro
    sociedade_id = db.Column(db.Integer, db.ForeignKey('sociedades.id'), nullable=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=True)

    # --- Segurança e Auditoria ---
    ativo = db.Column(db.Boolean, default=True) # Soft Delete: Ninguém apaga, só inativamos!
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) # Uso de timezone-aware datetime

# ==========================================
# 2. SOCIEDADES INTERNAS (UPA, UMP, SAF...)
# ==========================================
class Sociedade(db.Model):
    __tablename__ = 'sociedades'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) # Ex: União de Mocidade Presbiteriana
    sigla = db.Column(db.String(10), nullable=False) # Ex: UMP
    
    # O Conselheiro é sempre um Presbítero (Usuário)
    conselheiro_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    
    # Relação: Uma sociedade tem vários membros (usuários) e eventos
    membros = db.relationship('Usuario', backref='sociedade_vinculada', foreign_keys=[Usuario.sociedade_id])
    eventos = db.relationship('Evento', backref='sociedade_dona', lazy=True)

# ==========================================
# 3. DEPARTAMENTOS (EBD, Música, etc.)
# ==========================================
class Departamento(db.Model):
    __tablename__ = 'departamentos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) # Ex: Escola Bíblica Dominical
    
    # O Líder/Superintendente do departamento
    lider_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

# ==========================================
# 4. EVENTOS (Calendário)
# ==========================================
class Evento(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False) 
    data = db.Column(db.String(20), nullable=False)    
    hora = db.Column(db.String(10), nullable=False)   
    descricao = db.Column(db.Text, nullable=True)
    
    # De quem é este evento? (Pode ser geral da igreja, ou específico de uma sociedade)
    sociedade_id = db.Column(db.Integer, db.ForeignKey('sociedades.id'), nullable=True)
    
    # Auditoria: Quem criou este evento?
    criado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# ==========================================
# 5. ATAS (O Módulo DMS / Arquivo Digital)
# ==========================================
class Ata(db.Model):
    __tablename__ = 'atas'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False) # Ex: Ata da Plenária de Março
    data_plenaria = db.Column(db.Date, nullable=False)
    nome_arquivo = db.Column(db.String(255), nullable=False) # Nome do PDF no servidor
    
    # De qual sociedade é esta ata? Quem fez o upload?
    sociedade_id = db.Column(db.Integer, db.ForeignKey('sociedades.id'), nullable=False)
    enviado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_upload = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))