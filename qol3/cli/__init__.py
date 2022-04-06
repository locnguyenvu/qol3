import click
import asyncio
from flask.cli import AppGroup, with_appcontext
from pyppeteer import launch

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

    app.cli.add_command(click.Command("test", callback=real_test))
    pass


async def test():
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport(dict(width=1000, height=1200, isMobile=False))
    await page.goto('https://www.msn.com/vi-vn/money/indexdetails/fi-aqk2nm?duration=1D')
    await asyncio.sleep(3)
    # await page.screenshot({'path': 'vnindex-original.png'})
    await page.screenshot({'path': 'vnindex-clip.png', 'clip': {'x': 0, 'y': 202.0, 'width': 950, 'height': 798}})
    await browser.close()


def real_test():
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(test())
