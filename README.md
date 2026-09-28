# flytracker

Sends an email alert when the SDU–OPO fare on 9 March 2027 drops.

O script lê a tarifa de ida Santos Dumont (SDU) para Porto (OPO) em 9 de março de 2027 na página de ofertas da Azul. O modelo Gemini lê só o trecho da tarifa e devolve um JSON com preço, moeda, data e se achou. `validar_json.py` recusa texto quebrado, data diferente de `2027-03-09`, moeda diferente de BRL e preço fora da faixa de 50 a 20000. Resposta recusada não gera e-mail e não entra no banco.

Cada leitura aceita vai para o `precos.db`, tabela `leituras`. O SendGrid manda e-mail só quando o preço novo é menor que a última leitura dessa mesma passagem.

## Rodar uma vez

Na pasta do projeto, com as chaves só no ambiente:

```bash
export SENDGRID_API_KEY="sua-chave"
export GEMINI_API_KEY="sua-chave"
python3 comparar.py