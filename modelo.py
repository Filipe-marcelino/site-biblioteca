# Guardar os modelos do banco de dados

from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///dados.db')
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    email = Column(String(320 ), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f'<Produto {self.nome}>'
    
Base.metadata.create_all(engine)