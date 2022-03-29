from flask import current_app
from qol3.di import get_bot

bot = get_bot()

def setup_webhook(endpoint_url:str):
    webhook_endpoint = f"{endpoint_url}?x-bot={current_app.config.get('TELEGRAM_WEBHOOK_SECRET')}"
    result = bot.setWebhook(webhook_endpoint)
    print("Setup bot webhook endpoint {} result: {}".format(webhook_endpoint, result))
