# qol3
Telegram bot help tracking on nav price

# Setup

## Requirement
    * python3 (>=3.9)
    * postgreSQL (>=10.19)

## Development environemnt
Init python venv and enable vitualenv
```
python3 -m venv .venv
```

*Windows* (Powershell)
```
.\.venv\script\activate
```
*Unix*
```
source .\.venv\bin\activate
```

Create `.env` file
```
APP_LANG=vi

DB_URL=postgresql://root:root@localhost:5432/qol3

TELEGRAM_SECRET=<telegram-bot-secret>
TELEGRAM_WEBHOOK_SECRET=<secret-params-on-webhook>
```

Install dependencies
```
python -m pip install -e .
```

Set environment variable

*Windows* (Powershell)
```
$env:FLASK_APP='qol3'
$env:FLASK_ENV='development'
```

*Unix*
```
export FLASK_APP=qol3 
export FLASK_ENV=development
```
