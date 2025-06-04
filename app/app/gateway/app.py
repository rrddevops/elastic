from fastapi import FastAPI, HTTPException, Request 
from fastapi.middleware.cors import CORSMiddleware  # <-- importe o CORS middleware
import httpx

app = FastAPI()

# Adicionando o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque por ["http://localhost:8080"] ou domínio do front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/cadastro")
async def cadastro(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        try:
            cliente_response = await client.post("http://cliente_api:8000/cliente", json=data)
            if cliente_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Erro ao cadastrar cliente")

            pedido_response = await client.post("http://pedido_api:8000/pedido", json=data)
            if pedido_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Erro ao cadastrar pedido")

            entrega_response = await client.post("http://entrega_api:8000/entrega", json=data)
            if entrega_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Erro ao cadastrar entrega")

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Erro de comunicação com serviço: {str(e)}")

    return {"status": "Cadastro enviado com sucesso"}
