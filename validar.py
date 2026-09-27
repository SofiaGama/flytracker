def validar(preco):
    if not isinstance(preco, (int, float)):
        return "Preço inválido"
    if preco < 50 or preco > 20000:
        return "Preço inválido" 
    else: 
        return "Preço válido"


