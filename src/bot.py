import os
import logging
import json
import random
import time
import asyncio
from datetime import datetime
from io import BytesIO
from typing import Dict

import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Ferramentas de Nuvem e IA
from google.cloud import texttospeech, translate_v2 as translate
from langdetect import detect

# Módulos locais
from config import CONFIG

# --- Configuração de Logging e Clientes ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("KaorukoBotCPU")
translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()

# --- Funções Auxiliares de Imersão ---
def get_typing_delay(response_text: str) -> float:
    """Calcula um tempo de digitação mais natural."""
    base_delay = 1.0
    delay_per_char = random.uniform(0.05, 0.09)
    return min(base_delay + len(response_text) * delay_per_char, 7.0)

# --- Classe Principal do Bot (Versão CPU-Only) ---
class KaorukoBot:
    def __init__(self):
        os.makedirs(CONFIG.USER_DATA_DIR, exist_ok=True)
        self.app = None

    def load_user_data(self, user_id: str) -> Dict:
        path = os.path.join(CONFIG.USER_DATA_DIR, f"{user_id}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "name": "", "nickname": "", "history": [], "first_message_date": "",
            "affection_level": 0.3, "relationship_level": "desconhecido",
            "emotion": "doce", "last_emotion": "doce", "mood": "curiosa",
            "last_seen": time.time(), "conversation_count": 0
        }

    def save_user_data(self, user_id: str, data: Dict):
        path = os.path.join(CONFIG.USER_DATA_DIR, f"{user_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # --- Lógica de Personalidade e IA ---
    def build_mythomist_prompt(self, user_text: str, user_data: Dict) -> str:
        nickname = user_data.get("nickname", user_data.get("name", "usuário"))
        emotion = user_data['emotion']
        relationship = user_data['relationship_level']
        history = "\n".join([f"{h['role']}: {h['content']}" for h in user_data.get("history", [])[-6:]])

        relationship_directive = "Seja você mesma."
        if relationship == "desconhecido":
            relationship_directive = "Seja um pouco tímida, mas curiosa."
        elif relationship == "amigo":
            relationship_directive = "Seja mais descontraída e brincalhona."
        elif relationship == "namorado":
            relationship_directive = "Seja completamente apaixonada e íntima."

        instruction = (
            f"{CONFIG.BASE_PERSONALITY_PROMPT}\n"
            f"**Contexto:** Você está falando com {nickname}. Seu relacionamento é de {relationship}. {relationship_directive} Você está se sentindo {emotion}.\n"
            f"**Histórico:**\n{history}\n"
            f"**Tarefa:** Responda à mensagem do usuário de forma natural e criativa.\n"
            f"Usuário: {user_text}"
        )
        return f"### Instruction:\n{instruction}\n\n### Response:"

    async def get_ai_response(self, user_text: str, user_data: Dict) -> str:
        prompt = self.build_mythomist_prompt(user_text, user_data)
        payload = {
            "prompt": prompt,
            "temperature": 0.8,
            "top_p": 0.9,
            "n_predict": 200,
            "stop": ["### Instruction:", "Usuário:"]
        }
        try:
            response = requests.post(CONFIG.INFERENCE_SERVER_URL, json=payload, timeout=180)
            response.raise_for_status()
            return response.json().get("content", "").strip()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao contatar o servidor de IA: {e}")
            return "Aah... minha mente parece um pouco lenta agora... me desculpe. 🥺"

    # --- Handlers de Mensagens ---
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        user_text = update.message.text.strip()
        data = self.load_user_data(user_id)

        self.update_state(data, user_text)
        response_text = await self.get_ai_response(user_text, data)

        await update.message.chat.send_action("typing")
        await asyncio.sleep(get_typing_delay(response_text))

        self.add_to_history(data, "user", user_text)
        self.add_to_history(data, "assistant", response_text)
        self.save_user_data(user_id, data)

        # Tradução e Voz
        try:
            lang = detect(user_text)
            if lang not in ["pt", "en", "ja"]: lang = "pt"
        except Exception: lang = "pt"

        final_response, voice_text = self.prepare_multilingual_response(response_text, lang)
        await update.message.reply_text(final_response)

        if random.random() < 0.85:
            await self.send_voice_response(update, voice_text, data['emotion'])

    def prepare_multilingual_response(self, text: str, lang: str) -> tuple[str, str]:
        if lang == 'ja':
            return text, text
        try:
            translated_ja = translate_client.translate(text, target_language='ja')['translatedText']
            return f"{text}\n\n*{translated_ja}*", translated_ja
        except Exception as e:
            logger.error(f"Erro na tradução: {e}")
            return text, text

    async def send_voice_response(self, update: Update, text: str, emotion: str):
        try:
            await update.message.chat.send_action("record_voice")
            voice_params = CONFIG.VOICE_PROFILES.get(emotion, CONFIG.VOICE_PROFILES["default"])
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(language_code="ja-JP", name="ja-JP-Neural2-B")
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.OGG_OPUS, **voice_params)
            response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            await update.message.reply_voice(voice=BytesIO(response.audio_content))
        except Exception as e:
            logger.error(f"Erro na síntese de voz: {e}")

    # --- Funções de Estado e Histórico ---
    def update_state(self, data: Dict, user_text: str):
        if not data.get("name"): data["name"] = "Usuário"
        if not data.get("first_message_date"): data["first_message_date"] = datetime.now().strftime("%Y-%m-%d")
        data["conversation_count"] = data.get("conversation_count", 0) + 1
        data["last_seen"] = time.time()
        # ... (lógica de afeto, humor, etc. pode ser adicionada aqui) ...

    def add_to_history(self, data: Dict, role: str, content: str):
        history = data.get("history", [])
        history.append({"role": role, "content": content})
        data["history"] = history[-8:]

    # --- Main Loop ---
    def main(self):
        if CONFIG.TELEGRAM_TOKEN == "8196118567:AAHV47TmQiJ57Q_hBCUNZopvmdhwutRXV_w":
            logger.error("O TELEGRAM_TOKEN não foi configurado no script de inicialização!")
            return

        self.app = Application.builder().token(CONFIG.TELEGRAM_TOKEN).build()
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        logger.info("🌸 KaorukoBot (CPU-Only Cloud Version) iniciada! 🌸")
        self.app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    KaorukoBot().main()
