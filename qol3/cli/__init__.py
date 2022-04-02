import click
from flask.cli import AppGroup, with_appcontext

from . import bot, config, dcvfm


def init_app(app):
    app.cli.add_command(AppGroup("config", commands=[
        click.Command("set", callback=config.set,
                      params=[
                          click.Argument(["name"], required=True),
                          click.Argument(["value"], required=True),
                      ]),
    ]))

    app.cli.add_command(AppGroup("bot", commands=[
        click.Command("setup-webhook", callback=with_appcontext(bot.setup_webhook),
                      params=[click.Argument(["endpoint-url"], required=True)]),
    ]))

    app.cli.add_command(AppGroup("dcvfm", commands=[
        click.Command("nav-today", callback=with_appcontext(dcvfm.nav_today)),
    ]))
    pass
