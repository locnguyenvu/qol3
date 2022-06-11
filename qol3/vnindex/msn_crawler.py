import asyncio
import bs4
import json
from qol3 import ASSETS_PATH
from datetime import datetime
from flask import current_app
from os.path import join as path_join
from pyppeteer import launch


class Summary(object):

    def __init__(self,
                 open: float,
                 post: float,
                 changes_fix: float,
                 changes_percent: float,
                 reference_link: str):
        self.open = open
        self.post = post
        self.changes_fix = changes_fix
        self.changes_percent = changes_percent
        self.reference_link = reference_link

    def post_str(self) -> str:
        return f"{self.post:,}".replace('.', '\\.')

    def open_str(self) -> str:
        return f"{self.open:,}".replace('.', '\\.')

    def change_sign(self) -> str:
        sign = '📈'
        if self.changes_fix < 0:
            sign = '📉'
        return sign

    def changes_fix_str(self) -> str:
        return f"{self.changes_fix:,}".replace('.', '\\.').replace('-', '\\-')

    def changes_percent_str(self) -> str:
        return f"{self.changes_percent:.2f}".replace('.', '\\.').replace('-', '\\-')


def get_launch_option() -> dict:
    option = {
        "headless": True,
        "args": ['--no-sandbox', '--disable-gpu'],
    }
    if len(current_app.config.get("CHROMIUM_PATH")) > 0:
        option["executablePath"] = current_app.config.get("CHROMIUM_PATH")
    return option


async def screenshot_chart():
    launch_option = get_launch_option()
    browser = await launch(**launch_option)
    page = await browser.newPage()
    await page.setViewport(dict(width=1000, height=1200, isMobile=False))
    await page.goto(current_app.config.get("vnindex.image_crawler.screenshot_webpage_url"))
    await asyncio.sleep(3)
    file_path = path_join(ASSETS_PATH, "vnindex-" + datetime.now().strftime("%Y%m%d-%H%M" + ".png"))
    await page.screenshot({'path': file_path, 'clip': {'x': 0, 'y': 202.0, 'width': 950, 'height': 798}})
    await browser.close()
    return file_path
    pass


async def summary_on_end_session() -> Summary:
    launch_option = get_launch_option()
    browser = await launch(**launch_option)
    page = await browser.newPage()
    reference_url = current_app.config.get("vnindex.image_crawler.screenshot_webpage_url")
    await page.goto(reference_url)
    await asyncio.sleep(3)
    html_content = await page.content()
    await browser.close()

    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    chart_wrapper = soup.find_all(id='immersiveChartInstrumentationWrapper')
    chart_data = json.loads(chart_wrapper[0].attrs["data-config"])
    timeline_data = json.loads(chart_data["defaultData"])
    quotes = timeline_data[0]['Quotes']

    summary = Summary(quotes['Op'],
                      quotes['post'],
                      quotes['Ch'],
                      quotes['Chp'],
                      reference_url)
    return summary
