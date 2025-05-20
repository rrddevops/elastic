Antes de executar o docker-compose up, crie a rede observability com o comando

$ docker network create observability 
Também é necessário criar a pasta elasticsearch_data no fc2-observabilidade-elastic na máquina local manualmente para evitar erro de permissionamento

$ mkdir elasticsearch_data
Na pasta /beats/metric execute o seguinte comando:

$ sudo chown root metricbeat.yml 
Caso ocorra o erro 

bootstrap check failure [1] of [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
Execute o comando 

sysctl -w vm.max_map_count=262144

docker compose up -d

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
cd app
docker compose up -d

http://localhost:8000/exemplo

Frontend criando a RUM:
    <script src="https://unpkg.com/@elastic/apm-rum@5.4.0/dist/bundles/elastic-apm-rum.umd.min.js" crossorigin></script>
    <script>
        elasticApm.init({
        serviceName: "codeprogress-rum",
        pageLoadTraceId: "{{ apm.trace_id }}",
        pageLoadSpanId: "{{ apm.span_id }}",
        pageLoadSampled: {{ apm.is_sampled_js }},
        serverUrl: "http://localhost:8200",
    })
    </script>

Backend enviando dados para o APM: 
ELASTIC_APM = {
  # Set required service name. Allowed characters:
  # a-z, A-Z, 0-9, -, _, and space
  'SERVICE_NAME': 'codeprogress',

  # Set custom APM Server URL (default: http://localhost:8200)
  'SERVER_URL': 'http://apm:8200',
  'DEBUG': True,
  'ENVIRONMENT': 'production',
}