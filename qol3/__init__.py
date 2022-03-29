from __future__ import absolute_import

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    with app.app_context():
        from . import di
        di.bootstrap(app)

        from . import dbconfig
        dbconfig.load_toapp(app)

        from . import cli, http
        cli.init_app(app)
        http.init_app(app)

    return app

_ = create_app()
