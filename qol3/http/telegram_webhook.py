from flask import abort, current_app, make_response, request

from qol3.bot import dispatcher

def telegram_webhook_callback():
    secret = request.args.get("x-bot")
    if secret is None or secret != current_app.config.get("TELEGRAM_WEBHOOK_SECRET"):
        return abort(401)

    payload = request.get_json(force=True)
    
    if payload == None:
        return make_response({"status": "Error"}, 400)
    dispatcher.dispatch(payload)

    return make_response({"status": "Success"}, 200)
