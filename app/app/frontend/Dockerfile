FROM httpd:latest

# Instala as dependências necessárias
RUN apt-get update && \
    apt-get install -y curl gnupg dos2unix && \
    curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.13.0-amd64.deb && \
    dpkg -i filebeat-7.13.0-amd64.deb && \
    rm filebeat-7.13.0-amd64.deb && \
    apt-get clean

# Copia o index.html para o diretório padrão do Apache
COPY index.html /usr/local/apache2/htdocs/index.html

# Copia o arquivo de configuração do Filebeat
COPY filebeat.yml /etc/filebeat/filebeat.yml

# Corrige permissões do filebeat.yml
RUN chmod 600 /etc/filebeat/filebeat.yml

# Copia o script de entrada e corrige line endings
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Define o ponto de entrada
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
