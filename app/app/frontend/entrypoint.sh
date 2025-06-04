#!/bin/bash
set -e

# Aguarda o Elasticsearch estar disponível
until curl -s http://elasticsearch:9200 >/dev/null; do
    echo "Aguardando Elasticsearch..."
    sleep 5
done

# Aguarda o Kibana estar disponível
until curl -s http://kibana:5601 >/dev/null; do
    echo "Aguardando Kibana..."
    sleep 5
done

# Configura e inicia o Filebeat
filebeat modules enable apache
filebeat setup -e || true
nohup filebeat -e &

# Inicia o Apache em primeiro plano
exec httpd-foreground
