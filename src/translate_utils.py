from google.cloud import translate_v2 as translate

def translate_text(text, target="ja"):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]
