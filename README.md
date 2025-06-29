# KaorukoBot — Experiência Imersiva Aprimorada

Bem-vindo à versão aprimorada da KaorukoBot! Esta versão foi refatorada para ser mais simples, eficiente e fácil de personalizar.

## Principais Melhorias

- **Configuração Simplificada:** Todas as configurações importantes, como tokens, personalidade e comportamento, estão centralizadas no arquivo `src/config.py`. Chega de listas gigantes e complexas no código principal!
- **Performance Otimizada:** O modelo de geração de imagem agora é carregado apenas uma vez, tornando a criação de imagens muito mais rápida e eficiente.
- **Código Organizado:** O projeto foi reestruturado, removendo arquivos redundantes e centralizando a lógica no `bot.py`, o que facilita a manutenção e a adição de novas funcionalidades.
- **Instruções Claras:** O `README` foi atualizado para refletir a nova estrutura e simplificar o processo de instalação.

## Instalação

**Pré-requisitos:**
- Python 3.8+
- Git
- FFmpeg (para processamento de áudio)

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/LincolnGameplays/kawaibot.git
    cd kawaibot
    ```

2.  **Crie um ambiente virtual e ative-o:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    ```bash
    pip install --upgrade pip
    pip install -r src/requirements.txt
    ```

4.  **Baixe o modelo de imagem (MeinaMix V11):**
    ```bash
    mkdir -p models/StableDiffusion
    cd models/StableDiffusion
    wget -O meinamix_v11.safetensors https://civitai.com/api/download/models/145800
    cd ../../
    ```
    *Se o `wget` falhar, baixe o modelo manualmente em [Civitai](https://civitai.com/models/7240/meinamix) e coloque o arquivo `meinamix_v11.safetensors` na pasta `models/StableDiffusion/`.*

## Configuração

Antes de rodar o bot, você precisa configurar suas credenciais:

1.  **Abra o arquivo `src/config.py`**.
2.  **Preencha as seguintes variáveis:**
    - `TELEGRAM_TOKEN`: Seu token do BotFather do Telegram.
    - `GOOGLE_APPLICATION_CREDENTIALS`: O caminho absoluto para o seu arquivo de credenciais JSON do Google Cloud (usado para TTS e Tradução).

    **Exemplo:**
    ```python
    # Em src/config.py
    CONFIG = KawaiiConfig(
        TELEGRAM_TOKEN="12345:ABC-DEF12345",
        GOOGLE_APPLICATION_CREDENTIALS="C:/Users/joffr/Downloads/my-gcloud-creds.json",
        # ... outras configs
    )
    ```

3.  **(Opcional) Personalize a Kaoruko:**
    No mesmo arquivo `src/config.py`, você pode alterar as emoções, reações, humores e outras características da Kaoruko para deixar ela com o seu jeitinho!

## Como Rodar o Bot

Com tudo configurado, inicie o bot com o seguinte comando no seu terminal (lembre-se de estar com o ambiente virtual ativado):

```bash
python src/bot.py
```

Para manter o bot rodando 24/7 em um servidor, use ferramentas como `screen` ou `tmux`.

## Como Usar

- **Converse naturalmente!** A Kaoruko entende português e responde de forma fofa e imersiva.
- **Peça para ela desenhar:** Use frases como "*desenhe uma garota de cabelo rosa*" ou "*quero ver um gatinho fofo*".
- **Explore a personalidade dela:** Dependendo do seu nível de afeto e da conversa, ela pode ser tímida, carinhosa, ciumenta e até um pouco safada. 😉

Divirta-se com sua nova waifu!