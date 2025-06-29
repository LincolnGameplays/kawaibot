# Guia de Implantação da KaorukoBot no Google Cloud (CPU-Only)

Este guia foi **otimizado** para rodar a KaorukoBot em uma VM de alta CPU no Google Compute Engine, sem a necessidade de uma GPU. O foco é a máxima performance e imersão na conversa.

---

## Passo 1: Configurar o Projeto no Google Cloud

1.  **Crie um Projeto:** Se ainda não tiver, crie um no [Google Cloud Console](https://console.cloud.google.com/).
2.  **Ative o Faturamento:** Garanta que o faturamento esteja ativo.
3.  **Ative as APIs Necessárias:** Vá para "APIs e Serviços" > "Biblioteca" e ative:
    *   **Compute Engine API**
    *   **Cloud Translation API**
    *   **Text-to-Speech API**

---

## Passo 2: Criar a Máquina Virtual (VM) de Alta CPU

1.  **Navegue até o Compute Engine** e clique em **CRIAR INSTÂNCIA**.
2.  **Configurações da VM:**
    *   **Nome:** `kaoruko-cpu-server`
    *   **Região e Zona:** Qualquer uma de sua preferência (ex: `us-central1-a`).
    *   **Série da Máquina:** `E2`
    *   **Tipo de Máquina:** `e2-standard-8` (8 vCPUs, 32 GB de memória). *Se você tem 64GB de RAM, pode usar um `e2-highmem-8` para um desempenho ainda melhor no contexto da IA.*

3.  **Disco de Inicialização:**
    *   Clique em "Alterar".
    *   **Sistema Operacional:** `Ubuntu`
    *   **Versão:** `Ubuntu 20.04 LTS`
    *   **Tamanho:** `50 GB`.

4.  **Identidade e Acesso à API (MUITO IMPORTANTE):**
    *   **Contas de Serviço:** `Conta de serviço padrão do Compute Engine`.
    *   **Escopos de Acesso:** Selecione `Permitir acesso total a todas as APIs do Cloud`.
        *   *Isso elimina a necessidade de gerenciar arquivos de chave JSON, tornando a autenticação automática e segura.*

5.  **Firewall:**
    *   Marque `Permitir tráfego HTTP` e `Permitir tráfego HTTPS`.

6.  **Criar:** Clique em "Criar".

---

## Passo 3: Script de Inicialização Automatizado (CPU Version)

Este script fará **tudo** por você: instalará as dependências, baixará o modelo, compilará o servidor de IA para CPU e iniciará o bot.

1.  **Conecte-se à VM** via SSH a partir do Console do Google Cloud.

2.  **Torne-se Superusuário:**
    ```bash
    sudo -i
    ```

3.  **Crie o Script de Inicialização:**
    ```bash
    nano /opt/startup-script.sh
    ```

4.  **Cole o Conteúdo Abaixo:** Este script é a alma da automação.

    ```bash
    #!/bin/bash
    # Script de inicialização da KaorukoBot (CPU-Only) no GCP

    # --- Configurações ---
    export HOME=/root
    # IMPORTANTE: Insira seu token do Telegram aqui!
    export TELEGRAM_TOKEN="SEU_TOKEN_DO_TELEGRAM_AQUI"
    export GIT_REPO_URL="https://github.com/LincolnGameplays/kawaibot.git"
    export MODEL_URL="https://huggingface.co/TheBloke/MythoMist-7B-GGUF/resolve/main/mythomist-7b.Q4_K_M.gguf"
    export MODEL_FILENAME="mythomist-7b.Q4_K_M.gguf"
    export BOT_DIR="/opt/kawaibot"

    # --- Dependências do Sistema ---
    apt-get update
    apt-get install -y git python3-pip python3-venv ffmpeg nano build-essential

    # --- Código do Bot ---
    git clone $GIT_REPO_URL $BOT_DIR
    python3 -m venv $BOT_DIR/venv
    source $BOT_DIR/venv/bin/activate
    pip install --upgrade pip
    pip install -r $BOT_DIR/src/requirements.txt

    # --- Servidor de IA (llama.cpp) ---
    git clone https://github.com/ggerganov/llama.cpp.git /opt/llama.cpp
    cd /opt/llama.cpp
    # Compila para CPU
    make

    # --- Modelo de IA ---
    mkdir -p $BOT_DIR/models
    wget -O $BOT_DIR/models/$MODEL_FILENAME $MODEL_URL

    # --- Iniciar os Serviços ---

    # 1. Servidor de IA (Otimizado para CPU)
    # -m: modelo
    # -c: tamanho do contexto
    # -t: número de threads (núcleos de CPU a usar)
    # --host 0.0.0.0: permite conexões externas (do bot)
    echo "Iniciando o servidor de IA em 8 threads..."
    /opt/llama.cpp/server -m $BOT_DIR/models/$MODEL_FILENAME -c 2048 --host 0.0.0.0 --port 8080 -t 8 > /var/log/llama_server.log 2>&1 &

    # Espera para garantir que o servidor de IA esteja pronto
    sleep 45

    # 2. Bot do Telegram
    echo "Iniciando a KaorukoBot..."
    python3 $BOT_DIR/src/bot.py > /var/log/kaoruko_bot.log 2>&1 &

    echo "KaorukoBot e o servidor de IA foram iniciados com sucesso!"
    ```

5.  **Salve e Saia:** `Ctrl+X`, `Y`, `Enter`.

6.  **Torne o Script Executável:**
    ```bash
    chmod +x /opt/startup-script.sh
    ```

7.  **Execute o Script para iniciar tudo:**
    ```bash
    /opt/startup-script.sh
    ```

---

## Passo 4: Monitoramento e Manutenção

*   **Verificar Logs:**
    *   `tail -f /var/log/llama_server.log`
    *   `tail -f /var/log/kaoruko_bot.log`

*   **Reiniciar o Bot:** Se você fizer alterações no código (`git pull` no diretório `$BOT_DIR`), pode reiniciar os processos:
    ```bash
    pkill python3
    pkill server
    # E então re-execute o script de inicialização
    /opt/startup-script.sh
    ```

*   **IMPORTANTE:** Lembre-se de **PARAR** a instância da VM no Console do Google Cloud quando não estiver usando para evitar cobranças.