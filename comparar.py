import json
import os
import sqlite3
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
from validar import validar
from buscar import trecho_da_tarifa
from validar_json import aceitar

def decidir(preco_anterior, preco_hoje):
    if preco_hoje < preco_anterior:
        return "enviar"
    else:
        return "não enviar"

conexao = sqlite3.connect("precos.db")
chave = os.environ.get("SENDGRID_API_KEY")

trecho = trecho_da_tarifa()
resposta = ""
if trecho and "R$" in trecho:
    numero = trecho.split("R$")[1].split(" ")[0].replace("*", "")
    numero = numero.replace(".", "").replace(",", ".")
    resposta = json.dumps({
        "preco": float(numero),
        "moeda": "BRL",
        "data": "2027-03-09",
        "achou": True,
    })

if aceitar(resposta) != "aceito":
    print("leitura recusada, e-mail não saiu")
    conexao.close()
    raise SystemExit

preco_hoje = json.loads(resposta)["preco"]

linha = conexao.execute(
    """SELECT preco FROM leituras 
        WHERE origem = ? AND destino = ? AND data_viagem = ?
        ORDER BY id DESC LIMIT 1""",
        ("SDU", "OPO", "2027-03-09"),
).fetchone()

if linha is None:
    print("primeira leitura", preco_hoje)
else:
    preco_anterior = linha[0]
    decisao = decidir(preco_anterior, preco_hoje)
    print(preco_anterior, preco_hoje, decisao)
    if decisao == "enviar":
        print(f"A passagem caiu de {preco_anterior} para {preco_hoje}. Enviar alerta!")
        if chave:
            mensagem = Mail(
                from_email="sofiagamareis@gmail.com",
                to_emails="sofiagamareis@gmail.com",
                subject="Passagem SDU-OPO caiu",
                plain_text_content=f"A passagem caiu de {preco_anterior} para {preco_hoje}.",
            )
            try:
                resposta_email = SendGridAPIClient(chave).send(mensagem)
                print(resposta_email.status_code)
            except Exception as erro:
                print("e-mail não saiu:", erro)
        else: 
            print("Email não enviado. Chave não encontrada.")

conexao.execute(
        "INSERT INTO leituras (origem, destino, data_viagem, preco, lido_em) VALUES (?, ?, ?, ?, ?)",
        ("SDU", "OPO", "2027-03-09", preco_hoje, datetime.now().isoformat(timespec="seconds")),
    )
conexao.commit()      

ultima = conexao.execute(
    "SELECT id, origem, destino, data_viagem, preco, lido_em FROM leituras ORDER BY id DESC LIMIT 1"
).fetchone()
print(ultima)
conexao.close()