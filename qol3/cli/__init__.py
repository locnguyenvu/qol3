import click
from flask.cli import AppGroup, with_appcontext
from . import bot, config, dcvfm, holiday, vnindex


def init_app(app):
    app.cli.add_command(AppGroup("config", commands=[
        click.Command("set", callback=config.set, params=[
            click.Argument(["name"], required=True),
            click.Argument(["value"], required=True)]),
    ]))
    app.cli.add_command(AppGroup("bot", commands=[
        click.Command("setup-webhook", callback=with_appcontext(bot.setup_webhook),
                      params=[click.Argument(["endpoint-url"], required=True)]),
    ]))
    app.cli.add_command(AppGroup("dcvfm", commands=[
        click.Command("nav-today", callback=with_appcontext(dcvfm.nav_today)),
    ]))
    app.cli.add_command(AppGroup("holiday", commands=[
        click.Command("list", callback=with_appcontext(holiday.list)),
        click.Command("set", callback=with_appcontext(holiday.set), params=[
            click.Argument(["name"], required=True),
            click.Argument(["start-at"], required=True),
            click.Argument(["end-at"], required=True)])
    ]))
    app.cli.add_command(AppGroup("vnindex", commands=[
        click.Command("daily-report", callback=with_appcontext(vnindex.daily_report))
    ]))
    pass
