# flytracker

Sends an email alert when the SDU–OPO fare on 9 March 2027 drops.

The script reads the one-way fare from Santos Dumont (SDU) to Porto (OPO) on 9 March 2027 on Azul's deals page. Gemini reads only that fare snippet and returns JSON with the price, currency, date, and whether it found the fare. `validar_json.py` rejects broken text, a date other than `2027-03-09`, a currency other than BRL, and a price outside 50 to 20000. A rejected response does not send email and does not enter the database.

Each accepted reading is stored in `precos.db`, table `leituras`. SendGrid sends email only when the new price is lower than the last reading of this same fare.

## Run once

From the project folder, with both keys only in the environment:

```bash
export SENDGRID_API_KEY="your-key"
export GEMINI_API_KEY="your-key"
python3 comparar.py
```
The first reading of this route is stored and does not send email. Later runs compare it with the previous SDU–OPO row for `2027-03-09`.

## Where the data lives

`precos.db`, table `leituras`: origin, destination, travel date, price, and time of the reading. The file stays on the machine and is not in this repository.

## Every day at midnight

Cron runs the same script. Both keys stay on the scheduler line, outside this repository. The Mac has to be awake at midnight.

## What the check rejects

```bash
python3 validar_json.py
```
The expected output is aceito, recusado, recusado. Those are the words the program prints.
