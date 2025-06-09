#!/bin/bash
set -e

echo "Starting initialization script..."
echo "PostgreSQL Host: $POSTGRES_HOST"
echo "PostgreSQL Port: 5432"

# Aguarda o PostgreSQL estar pronto
echo "Waiting for PostgreSQL..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing database initialization"

# Inicializa o banco de dados
echo "Creating database tables..."
python << END
import sys
try:
    from database import engine
    from models import Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {e}", file=sys.stderr)
    sys.exit(1)
END

echo "Starting FastAPI application..."
exec uvicorn app:app --host 0.0.0.0 --port 8000 --reload 