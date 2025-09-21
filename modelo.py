#arquivo responsável por guardar os modelos do banco de dados

from db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(320 ), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Usuario {self.nome}>'

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Produto {self.nome}>'