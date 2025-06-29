# Escolhe imagem base com Python
FROM python:3.10-slim

# Define a pasta de trabalho
WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código para dentro do container
COPY . .

# Expõe a porta que o Flask vai rodar
EXPOSE 5000

# Comando para iniciar o app em produção
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
