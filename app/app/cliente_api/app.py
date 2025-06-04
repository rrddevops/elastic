# Ex: services/cliente_api/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Cliente(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

@app.post("/cliente")
def cadastrar_cliente(cliente: Cliente):
    return {"status": "Cliente recebido com sucesso"}

