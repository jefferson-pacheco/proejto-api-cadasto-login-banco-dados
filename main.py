#os programas necessario para importa para api desse casdastro e login
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import CONN, Pessoa, Tokens
from secrets import token_hex

app = FastAPI()

#Para conectar ao banco na models  
def conectaBanco():
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

#para fazer o cadasto e fazer o filter do usuario e salvar no banco de dados usando o commit
@app.post('/cadastro')
def cadastro(nome: str, user: str, senha: str):
    session = conectaBanco()
    usuario = session.query(Pessoa).filter_by(usuario=user, senha=senha).all()
    if len(usuario) == 0:
        x = Pessoa(nome=nome, usuario=user, senha=senha)
        session.add(x)
        session.commit()
        return {'status': 'Sucesso'}
    elif len(usuario) > 0:
        return {'status': 'Usuario ja cadastrado'}

#para fazer o login e criar o token unico de cada usuario 
@app.post('/login')
def login(usuario: str, senha: str):
    session = conectaBanco()
    user = session.query(Pessoa).filter_by(usuario=usuario, senha=senha).all()
    if len(user) == 0:
        return {'status': 'usuario inexistente'}
    
    while True:
        token = token_hex(50)
        tokenExiste = session.query(Tokens).filter_by(token=token).all()
        if len(tokenExiste) == 0:
            pessoaExiste = session.query(Tokens).filter_by(id_pessoa=user[0].id).all()
            if len(pessoaExiste) == 0:
                novoToken = Tokens(id_pessoa=user[0].id, token=token)
                session.add(novoToken)
            elif len(pessoaExiste) > 0:
                pessoaExiste[0].token = token

            session.commit()

            break
    return token
