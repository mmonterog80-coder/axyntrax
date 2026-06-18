FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Dar permisos de ejecución al script
RUN chmod +x start_cloud.sh

# Exponer puerto
EXPOSE 8080

# Comando de inicio
CMD ["bash", "start_cloud.sh"]
