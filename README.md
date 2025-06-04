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

### Monitoramento
- Kibana: http://localhost:5601
- APM: http://localhost:8200
- Grafana: http://localhost:3000

## Exemplo de Uso via cURL

Para cadastrar um pedido diretamente via API:

```bash
curl -X POST http://localhost:8000/cadastro \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "11999999999",
    "quantidade": 2,
    "produto": "Produto Teste",
    "valor": 99.99,
    "endereco": "Rua Exemplo, 123",
    "cep": "12345-678",
    "cidade": "São Paulo",
    "estado": "SP"
  }'
```

## Monitoramento

### APM (Application Performance Monitoring)
- Acesse o Kibana (http://localhost:5601)
- Navegue até "APM" no menu lateral
- Visualize traces, erros e métricas de todas as APIs

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
│   ├── pedido_api/
│   ├── entrega_api/
│   └── docker-compose.yml
├── apm/
├── beats/
│   ├── metric/
│   └── heartbeat/
├── elasticsearch_data/
├── docker-compose.yaml
└── README.md
```

Antes de executar o docker-compose up, crie a rede observability com o comando:
```
$ docker network create observability
```

Também é necessário criar a pasta elasticsearch_data no elastic na máquina local manualmente para evitar erro de permissionamento:
```
$ mkdir elasticsearch_data
```

Na pasta /beats/metric execute o seguinte comando:
```
$ sudo chown root metricbeat.yml
```

Caso ocorra o erro:
```
bootstrap check failure [1] of [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

Execute o comando:
```
sysctl -w vm.max_map_count=262144
```

Suba os containers da stack do Elastic:
```
docker compose up -d
```

Kibana: 
http://localhost:5601

Elstic Search: 
http://elasticsearch:9200

APM:
http://localhost:8200
RUM real user monitoring 
 O monitoramento de usuários reais (RUM) do Elastic APM captura as interações dos usuários com os navegadores.
apm-server.rum.enabled: true

Suba a aplicação: 
http://localhost:8000

```
cd app
docker compose up -d

Caso tenha feito alguma alteraçao no projeto execute:
rm db.sqlite3
docker-compose up --build