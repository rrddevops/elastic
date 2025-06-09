# Dockerfile (em cada pasta de microserviço)
FROM python:3.9

WORKDIR /app
COPY . .

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y postgresql-client netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Configura o script de inicialização
RUN chmod +x start.sh

CMD ["./start.sh"]