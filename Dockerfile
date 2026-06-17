FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

WORKDIR /app

# Instalar dependencias del sistema (por ejemplo, compilador para Qwen/DeepSeek si se requiere)
RUN apt-get update && apt-get install -y \
    g++ \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Dar permisos de ejecución al script de arranque
RUN chmod +x start_cloud.sh

# Puerto de la nube
ENV PORT=8000
EXPOSE $PORT

CMD ["./start_cloud.sh"]
