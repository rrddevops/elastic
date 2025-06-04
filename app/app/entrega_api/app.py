from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Entrega(BaseModel):
    endereco: str
    cep: str
    cidade: str
    estado: str

@app.post("/entrega")
def cadastrar_entrega(entrega: Entrega):
    # Remove o hífen antes de validar
    cep = entrega.cep.replace('-', '')
    
    if not cep.isdigit() or len(cep) < 8:
        raise HTTPException(status_code=400, detail="CEP inválido")
    
    return {"status": "Entrega recebida com sucesso"}