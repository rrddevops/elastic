from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Pedido(BaseModel):
    quantidade: int
    produto: str
    valor: float

@app.post("/pedido")
def cadastrar_pedido(pedido: Pedido):
    if pedido.quantidade <= 0 or pedido.valor <= 0:
        raise HTTPException(status_code=400, detail="Quantidade e valor devem ser positivos")
    return {"status": "Pedido recebido com sucesso"}