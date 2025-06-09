# Ex: services/cliente_api/app.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
from database import engine, get_db
import logging
import elasticapm
from elasticapm.contrib.starlette import ElasticAPM
from elasticapm.traces import capture_span

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do APM
app = FastAPI()
apm = elasticapm.Client({
    'SERVICE_NAME': 'cliente_api',
    'SERVER_URL': 'http://apm-server:8200',
    'ENVIRONMENT': 'production',
    'CAPTURE_BODY': 'all',
    'CAPTURE_HEADERS': True,
    'CAPTURE_SQL_QUERIES': True,
    'TRANSACTION_MAX_SPANS': 500,
    'STACK_TRACE_LIMIT': 50
})

# Adiciona o middleware do APM
app.add_middleware(ElasticAPM, client=apm)

# Cria as tabelas
models.Base.metadata.create_all(bind=engine)

class Cliente(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

    class Config:
        orm_mode = True

@app.post("/cliente")
def cadastrar_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    logger.info(f"Recebendo requisição para cadastrar cliente: {cliente.dict()}")
    
    try:
        with capture_span('verificar_cliente_existente', 'db.query'):
            # Verifica se já existe um cliente com este email
            existing_cliente = db.query(models.Cliente).filter(models.Cliente.email == cliente.email).first()
            if existing_cliente:
                logger.error(f"Cliente com email {cliente.email} já existe")
                raise HTTPException(
                    status_code=400,
                    detail=f"Cliente com email {cliente.email} já existe"
                )

        with capture_span('criar_cliente', 'db.insert'):
            db_cliente = models.Cliente(
                nome=cliente.nome,
                email=cliente.email,
                telefone=cliente.telefone
            )
            
            db.add(db_cliente)
            db.commit()
            db.refresh(db_cliente)
        
        logger.info(f"Cliente cadastrado com sucesso: ID {db_cliente.id}")
        return {"status": "Cliente recebido com sucesso", "cliente": db_cliente}
    
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Erro de integridade ao cadastrar cliente: {str(e)}")
        elasticapm.capture_exception()
        raise HTTPException(
            status_code=400,
            detail="Erro de integridade ao cadastrar cliente. Possível duplicação de email."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao cadastrar cliente: {str(e)}")
        elasticapm.capture_exception()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao cadastrar cliente: {str(e)}"
        )

