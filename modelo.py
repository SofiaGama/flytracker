import os 
import requests

def pedir_json(trecho):
    chave = os.environ.get("GEMINI_API_KEY")
    if not chave or not trecho:
        return ""
    pedido = (
        "Leia somente o trecho abaixo. "
        "Devolva um JSON com preco (número), moeda, data e achou. "
        "moeda é BRL quando o valor está em reais. "
        "As datas do trecho estão em dia/mês/ano. "
        "No JSON, data fica AAAA-MM-DD. "
        "achou é true só se o trecho tiver a tarifa de ida SDU para OPO. "
        "Não invente outro voo. \n\n"
        f"Trecho:\n{trecho}"
    )
    resposta = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": chave,
        },
        json={
            "contents": [{"parts": [{"text": pedido}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        },
        timeout=30,
    )
    if resposta.status_code != 200:
        print("modelo não respondeu:", resposta.status_code)
        return ""
    dados = resposta.json()
    try:
        partes = dados["candidates"][0]["content"]["parts"]
        for parte in reversed(partes):
            if parte.get("text") and not parte.get("thought"):
                return parte["text"]
        return ""
    except (KeyError, IndexError, TypeError):
        return ""