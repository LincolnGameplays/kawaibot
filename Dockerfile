FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os arquivos de dependência
COPY requirements.txt ./

# Instala as dependências Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto
COPY . .

# (Opcional) Copia as credenciais do Google Cloud. No deploy, prefira o Secret Manager.
# COPY cred.json /app/cred.json

# Porta não é obrigatória para bots Telegram (polling), mas pode deixar:
EXPOSE 8080

# Comando para rodar o bot
CMD ["python", "bot.py"]
