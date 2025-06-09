from fastapi import FastAPI, HTTPException, Request 
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json

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
            # Dados para o cliente_api
            cliente_data = {
                "nome": data["nome"],
                "email": data["email"],
                "telefone": data["telefone"]
            }
            print(f"Enviando dados para cliente_api: {json.dumps(cliente_data)}")
            
            cliente_response = await client.post(
                "http://cliente_api:8000/cliente",
                json=cliente_data,
                timeout=30.0
            )
            
            response_text = await cliente_response.aread()
            print(f"Resposta do cliente_api: {response_text}")
            
            if cliente_response.status_code != 200:
                error_detail = cliente_response.json().get('detail', 'Erro desconhecido')
                raise HTTPException(
                    status_code=400,
                    detail=f"Erro ao cadastrar cliente: {error_detail}"
                )
            
            cliente_info = cliente_response.json()
            cliente_id = cliente_info["cliente"]["id"]

            # Dados para o pedido_api
            pedido_data = {
                "cliente_id": cliente_id,
                "produto": data["produto"],
                "quantidade": int(data["quantidade"]),
                "valor_total": float(data["valor"])
            }
            print(f"Enviando dados para pedido_api: {json.dumps(pedido_data)}")
            
            pedido_response = await client.post(
                "http://pedido_api:8000/pedido",
                json=pedido_data,
                timeout=30.0
            )
            
            if pedido_response.status_code != 200:
                error_detail = pedido_response.json().get('detail', 'Erro desconhecido')
                raise HTTPException(
                    status_code=400,
                    detail=f"Erro ao cadastrar pedido: {error_detail}"
                )
            
            pedido_info = pedido_response.json()
            pedido_id = pedido_info["pedido"]["id"]

            # Dados para o entrega_api
            entrega_data = {
                "pedido_id": pedido_id,
                "endereco": data["endereco"],
                "cep": data["cep"].replace("-", ""),
                "cidade": data["cidade"],
                "estado": data["estado"]
            }
            print(f"Enviando dados para entrega_api: {json.dumps(entrega_data)}")
            
            entrega_response = await client.post(
                "http://entrega_api:8000/entrega",
                json=entrega_data,
                timeout=30.0
            )
            
            if entrega_response.status_code != 200:
                error_detail = entrega_response.json().get('detail', 'Erro desconhecido')
                raise HTTPException(
                    status_code=400,
                    detail=f"Erro ao cadastrar entrega: {error_detail}"
                )

            return {
                "status": "Cadastro enviado com sucesso",
                "cliente": cliente_info["cliente"],
                "pedido": pedido_info["pedido"],
                "entrega": entrega_response.json()["entrega"]
            }

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro de comunicação com serviço: {str(e)}"
            )
        except KeyError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Campo obrigatório ausente: {str(e)}"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Erro de validação: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro inesperado: {str(e)}"
            )
