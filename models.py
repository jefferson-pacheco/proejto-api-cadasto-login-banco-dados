#O arquivo models fica responsavel por fazer a conexão ao banco e criar as tabela no banco
from sqlalchemy import create_engine, Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

USUARIO = "root"
SENHA = "*****"
HOST = "localhost"
BANCO = "aulaapis"
PORT = 3306
#Esse trecho vai imforma qual banco de dados vamos trabalhar f"mysql+pymysql" 
CONN = f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORT}/{BANCO}"

#Esse trecho faz parte da conexão do banco de dados. engine = create_engine(CONN, echo=True) mostra todos os passos 
#Ou engine = create_engine(CONN, echo=False) so mostra os principal erros. o restante do codigo se mante o mesmo 
engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

#Para criar as colunas no banco de dados 
class Pessoa(Base):
    __tablename__ = 'Pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    usuario = Column(String(20))
    senha = Column(String(10))

#Para conectar o id uma coluna no banco de dados para ser o id unico
class Tokens(Base):
    __tablename__ = 'Tokens'
    id = Column(Integer, primary_key=True)
    id_pessoa = Column(Integer, ForeignKey('Pessoa.id'))
    token =Column(String(100))
    data = Column(DateTime, default=datetime.datetime.utcnow())

Base.metadata.create_all(engine)

