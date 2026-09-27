# flytracker

Sends an email alert when the SDU–OPO fare on 9 March 2027 drops.

O script lê a tarifa de ida Santos Dumont (SDU) para Porto (OPO) em 9 de março de 2027 na página de ofertas da Azul. Grava cada leitura no arquivo `precos.db`, tabela `leituras`. Manda e-mail pelo SendGrid só quando o preço novo é menor que a última leitura dessa mesma passagem.

## Rodar uma vez

Na pasta do projeto, com a chave só no ambiente:

```bash
export SENDGRID_API_KEY="sua-chave"
python3 comparar.py