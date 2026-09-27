import json    
from validar import validar

def aceitar(resposta):
    try:
        dados = json.loads(resposta)
    except json.JSONDecodeError:
        return "recusado"
    if not isinstance(dados, dict):
        return "recusado"
    if dados.get("achou") is not True:
        return "recusado"
    if dados.get("moeda") != "BRL":
        return "recusado"
    if dados.get("data") != "2027-03-09":   
        return "recusado"
    if validar(dados.get("preco")) != "Preço válido":
        return "recusado"
    return "aceito" 

if __name__ == "__main__":
    boa = '{"preco": 3106.73, "moeda": "BRL", "data": "2027-03-09", "achou": true}'
    data_errada = '{"preco": 3106.73, "moeda": "BRL", "data": "2027-03-10", "achou": true}'
    quebrada = "o preço é 3106"
    print(aceitar(boa))
    print(aceitar(data_errada))
    print(aceitar(quebrada))