from flask import Blueprint, make_response
from .telegram_webhook import telegram_webhook_callback

telegram_webhook = Blueprint('telegram_webhook', '__name__')
telegram_webhook.add_url_rule("/telegram", methods=["POST",], view_func=telegram_webhook_callback)

healthcheck = Blueprint("health_check", __name__)
@healthcheck.route("/health-check", methods=["GET",])
def health_check():
    return make_response({
        "status": "ok"
    })

def init_app(app):
    app.register_blueprint(telegram_webhook)
    app.register_blueprint(healthcheck)
    pass