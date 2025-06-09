#!/bin/bash

# Exporta variáveis de ambiente para a sessão atual
export POSTGRES_HOST=localhost
export POSTGRES_PASSWORD=postgres
export POSTGRES_USER=postgres
export POSTGRES_DB=elastic_db

echo "Variáveis de ambiente definidas:"
echo "POSTGRES_HOST=$POSTGRES_HOST"
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD"
echo "POSTGRES_USER=$POSTGRES_USER"
echo "POSTGRES_DB=$POSTGRES_DB"
