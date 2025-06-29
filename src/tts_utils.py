from google.cloud import texttospeech
from typing import Dict

def synthesize_speech(text: str, lang: str = "ja-JP", voice_name: str = "ja-JP-Neural2-B", emotion_params: Dict = None) -> bytes:
    """
    Sintetiza a fala com parâmetros emocionais dinâmicos.

    Args:
        text: O texto a ser sintetizado.
        lang: O código do idioma (ex: "ja-JP").
        voice_name: O nome da voz neural.
        emotion_params: Dicionário com 'pitch', 'speaking_rate' e 'volume_gain_db'.

    Returns:
        Os bytes do áudio gerado.
    """
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=lang, name=voice_name)

    # Parâmetros padrão caso não sejam fornecidos
    if emotion_params is None:
        emotion_params = {"pitch": 0.0, "speaking_rate": 1.0, "volume_gain_db": 0.0}

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.OGG_OPUS,
        pitch=emotion_params.get("pitch", 0.0),
        speaking_rate=emotion_params.get("speaking_rate", 1.0),
        volume_gain_db=emotion_params.get("volume_gain_db", 0.0)
    )

    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )
    return response.audio_content