import asyncio
from qol3 import ASSETS_PATH
from datetime import datetime
from flask import current_app
from os.path import join as path_join
from pyppeteer import launch


async def screenshot_chart():
    launch_option = {
        "headless": True,
        "args": ['--no-sandbox', '--disable-gpu'],
    }
    if len(current_app.config.get("CHROMIUM_PATH")) > 0:
        launch_option["executablePath"] = current_app.config.get("CHROMIUM_PATH")

    browser = await launch(**launch_option)
    page = await browser.newPage()
    await page.setViewport(dict(width=1000, height=1200, isMobile=False))
    await page.goto(current_app.config.get("vnindex.image_crawler.screenshot_webpage_url"))
    await asyncio.sleep(2)
    file_path = path_join(ASSETS_PATH, "vnindex-" + datetime.now().strftime("%Y%m%d-%H%M" + ".png"))
    await page.screenshot({'path': file_path, 'clip': {'x': 0, 'y': 202.0, 'width': 950, 'height': 798}})
    await browser.close()
    return file_path
    pass
