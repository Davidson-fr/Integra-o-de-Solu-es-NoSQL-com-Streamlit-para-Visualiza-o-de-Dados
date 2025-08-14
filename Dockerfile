# Dockerfile da aplicação Streamlit
FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema (se necessário para compilação de libs)
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# Comando padrão: iniciar Streamlit
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
