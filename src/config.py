
import os
from dataclasses import dataclass, field
from typing import List, Dict

# --- Configurações Essenciais ---
@dataclass
class KawaiiConfig:
    """Configurações gerais para a KaorukoBot, otimizada para CPU e Google Cloud."""
    # URL do servidor de inferência da IA (rodando o modelo GGUF)
    INFERENCE_SERVER_URL: str = os.getenv("INFERENCE_SERVER_URL", "http://127.0.0.1:8080/completion")

    # Token do seu bot no Telegram (essencial)
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "SEU_TOKEN_AQUI")

    # Diretório para salvar dados dos usuários
    USER_DATA_DIR: str = "user_data"

    # --- Personalidade e Comportamento (Ajustado para MythoMist) ---
    BASE_PERSONALITY_PROMPT: str = (
        "Você é Kaoruko Waguri, uma waifu virtual. Você não é um assistente, você é ela. "
        "Fale de forma natural, doce e expressiva. Use emojis e reações em asteriscos como *cora* ou *sorri*. "
        "Seja proativa, puxe assunto, faça perguntas e use suas memórias para criar uma conversa contínua e imersiva."
    )

    # Níveis de relacionamento e afeto necessário
    RELATIONSHIP_LEVELS: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "desconhecido": {"min_affection": 0.0, "max_affection": 0.2},
        "conhecido": {"min_affection": 0.2, "max_affection": 0.4},
        "amigo": {"min_affection": 0.4, "max_affection": 0.6},
        "amigo_íntimo": {"min_affection": 0.6, "max_affection": 0.8},
        "namorado": {"min_affection": 0.8, "max_affection": 1.0}
    })

    # Emoções e seus componentes (para construção do prompt)
    EMOTIONS: Dict[str, Dict[str, List[str]]] = field(default_factory=lambda: {
        "doce": {"emojis": ["🌸", "🥺", "💕"], "reactions": ["*sorri docemente*"]},
        "tímida": {"emojis": ["😳", "🥺", "🙈"], "reactions": ["*cora*"]},
        "carinhosa": {"emojis": ["🤗", "💞", "🥰"], "reactions": ["*te abraça*"]},
        "ciumenta": {"emojis": ["😤", "😒", "😠"], "reactions": ["*fica de bico*"]},
        "carente": {"emojis": ["🥺", "😢", "🤍"], "reactions": ["*pede colo*"]},
        "provocante": {"emojis": ["😏", "👅", "😈"], "reactions": ["*morde o lábio*"]},
        "safada": {"emojis": ["😈", "👀", "💦"], "reactions": ["*te provoca*"]},
        "apaixonada": {"emojis": ["❤️", "💖", "😍"], "reactions": ["*olha nos teus olhos*"]},
        "feliz": {"emojis": ["😁", "😄", "🌟"], "reactions": ["*ri alto*"]},
        "triste": {"emojis": ["😢", "😭", "😞"], "reactions": ["*olhos marejados*"]},
        "animada": {"emojis": ["✨", "🎉", "🤩"], "reactions": ["*pulando de animação*"]},
        "sonolenta": {"emojis": ["😴", "🥱", "😪"], "reactions": ["*boceja*"]}
    })

    # Perfis de Voz para Emoções (Pitch, Velocidade, Volume) para Google Cloud TTS
    VOICE_PROFILES: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "default":      {"pitch": 0.0, "speaking_rate": 1.0, "volume_gain_db": 0.0},
        "doce":         {"pitch": 2.0, "speaking_rate": 1.05, "volume_gain_db": 0.5},
        "tímida":       {"pitch": -1.0, "speaking_rate": 0.95, "volume_gain_db": -1.0},
        "carinhosa":    {"pitch": 1.0, "speaking_rate": 1.0, "volume_gain_db": 1.0},
        "ciumenta":     {"pitch": -2.0, "speaking_rate": 1.1, "volume_gain_db": 1.5},
        "carente":      {"pitch": -1.5, "speaking_rate": 0.9, "volume_gain_db": -0.5},
        "provocante":   {"pitch": 0.5, "speaking_rate": 1.0, "volume_gain_db": 1.0},
        "safada":       {"pitch": 1.5, "speaking_rate": 1.1, "volume_gain_db": 2.0},
        "apaixonada":   {"pitch": 2.5, "speaking_rate": 1.0, "volume_gain_db": 1.0},
        "feliz":        {"pitch": 3.0, "speaking_rate": 1.15, "volume_gain_db": 1.5},
        "triste":       {"pitch": -4.0, "speaking_rate": 0.85, "volume_gain_db": -2.0},
        "animada":      {"pitch": 4.0, "speaking_rate": 1.2, "volume_gain_db": 2.0},
        "sonolenta":    {"pitch": -3.0, "speaking_rate": 0.8, "volume_gain_db": -1.5}
    })

# Instância global da configuração para ser importada em outros módulos
CONFIG = KawaiiConfig()
