import requests

URL = "https://passagens.voeazul.com.br/pt/voos-de-rio-de-janeiro-para-porto"
MARCA = "SDU) Para Porto (OPO) Ida: 09/03/2027"

def trecho_da_tarifa():
    resposta = requests.get(
    URL,
    timeout=20,
    headers={"User-Agent": "rastreador-de-precos/0.1"},
    )
    if resposta.status_code != 200:
        return None
    texto = resposta.text
    pos = texto.find(MARCA)
    if pos == -1:
        return None
    return texto[pos:pos + 110]

if __name__ == "__main__":
    print(trecho_da_tarifa())
    