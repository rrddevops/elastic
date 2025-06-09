# Sistema de Pedidos com Monitoramento ELK

Este projeto é um sistema distribuído de pedidos com monitoramento completo usando a stack ELK (Elasticsearch, Logstash, Kibana) + APM + Beats, além de Grafana para visualização de métricas.

## Arquitetura

O sistema é composto por:

- Frontend (Apache)
- API Gateway
- Microserviços:
  - Cliente API
  - Pedido API
  - Entrega API
- Banco de Dados:
  - PostgreSQL
- Stack de Monitoramento:
  - Elasticsearch
  - Kibana
  - APM Server
  - Filebeat
  - Metricbeat
  - Heartbeat
  - Grafana

## Pré-requisitos

- Docker
- Docker Compose

## Como Executar

1. Clone o repositório:
```bash
git clone <repository-url>
cd elastic
```

2. Inicie a stack ELK:
```bash
docker-compose up -d
```

3. Inicie a aplicação:
```bash
cd app
docker-compose up -d
```

## Endpoints

### Frontend
- URL: http://localhost:8080
- Interface web para cadastro de pedidos

### APIs
- Gateway: http://localhost:8000
- Cliente API: http://localhost:8001
- Pedido API: http://localhost:8002
- Entrega API: http://localhost:8003

### Banco de Dados
- PostgreSQL: localhost:5432
- Banco: elastic_db
- Usuário: postgres
- Senha: postgres

### Monitoramento
- Kibana: http://localhost:5601
- APM: http://localhost:8200
- Grafana: http://localhost:3000

## Estrutura do Banco de Dados

O sistema utiliza PostgreSQL como banco de dados principal, com as seguintes tabelas:

### Tabela: clientes
- id (PK)
- nome
- email (unique)
- telefone

### Tabela: pedidos
- id (PK)
- cliente_id (FK)
- produto
- quantidade
- valor_total
- data_pedido
- status

### Tabela: entregas
- id (PK)
- pedido_id (FK)
- endereco
- status
- data_entrega
- data_criacao

## Exemplo de Uso via cURL

Para cadastrar um cliente:
```bash
curl -X POST http://localhost:8001/cliente \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "11999999999"
  }'
```

Para cadastrar um pedido:
```bash
curl -X POST http://localhost:8002/pedido \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "produto": "Produto Teste",
    "quantidade": 2,
    "valor_total": 99.99
  }'
```

Para cadastrar uma entrega:
```bash
curl -X POST http://localhost:8003/entrega \
  -H "Content-Type: application/json" \
  -d '{
    "pedido_id": 1,
    "endereco": "Rua Exemplo, 123",
    "cep": "12345678",
    "cidade": "São Paulo",
    "estado": "SP"
  }'
```

## Monitoramento

### APM (Application Performance Monitoring)
- Acesse o Kibana (http://localhost:5601)
- Navegue até "APM" no menu lateral
- Visualize traces, erros e métricas de todas as APIs
- Agora inclui monitoramento de operações do banco de dados

### Logs
- Os logs de todas as aplicações são coletados pelo Filebeat
- Visualize no Kibana em "Discover"
- Use o índice `filebeat-*` para logs do Apache
- Use o índice `apm-*` para logs das APIs

### Métricas
- Acesse o Grafana (http://localhost:3000)
- Credenciais padrão: admin/admin
- Dashboards disponíveis:
  - Métricas do Sistema
  - Performance das APIs
  - Métricas do Apache
  - Métricas do PostgreSQL

### Heartbeat
- Monitora a disponibilidade de todos os serviços
- Visualize no Kibana em "Uptime"

## Estrutura de Diretórios

```
.
├── app/
│   ├── frontend/
│   ├── gateway/
│   ├── cliente_api/
│   │   ├── app.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── requirements.txt
│   ├── pedido_api/
│   │   ├── app.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── requirements.txt
│   ├── entrega_api/
│   │   ├── app.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── requirements.txt
│   └── docker-compose.yml
├── apm/
├── beats/
│   ├── metric/
│   └── heartbeat/
├── elasticsearch_data/
├── docker-compose.yaml
└── README.md
```

## Configuração Inicial

Antes de executar o docker-compose up, crie a rede observability com o comando:
```bash
docker network create observability
```

Também é necessário criar a pasta elasticsearch_data no elastic na máquina local manualmente para evitar erro de permissionamento:
```bash
mkdir elasticsearch_data
```

Na pasta /beats/metric execute o seguinte comando:
```bash
sudo chown root metricbeat.yml
```

Caso ocorra o erro:
```
bootstrap check failure [1] of [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

Execute o comando:
```bash
sysctl -w vm.max_map_count=262144
```

## Iniciando os Serviços

1. Suba os containers da stack do Elastic:
```bash
docker compose up -d
```

2. Suba a aplicação:
```bash
cd app
docker compose up -d
```

Para reconstruir os containers após alterações:
```bash
docker-compose up --build
```

## Acessando os Serviços

- Kibana: http://localhost:5601
- Elasticsearch: http://elasticsearch:9200
- APM: http://localhost:8200
- Aplicação: http://localhost:8000

### RUM (Real User Monitoring)
O monitoramento de usuários reais (RUM) do Elastic APM captura as interações dos usuários com os navegadores.
Para habilitar:
```yaml
apm-server.rum.enabled: true
```
