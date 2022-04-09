import asyncio
from datetime import datetime
from typing import Union

import aiohttp
import bs4
from flask import current_app
from qol3.fund.dcvfm.util import numbers
from qol3.fund.fund import Fund, list_dcfvm
from qol3.fund.fund_nav_price_history import (FundNavPriceHistory, existed,
                                              mark_active)


class ajax(object):

    BASE_URL = current_app.config.get("fund.dcvfm.crawler.base_url_ajax")

    def __init__(self, session=aiohttp.ClientSession):
        self.session = session
        pass

    async def fetch_nav_price_history(self, fund_name:str) -> list:
        request_payload = {
            "action": "filter_old_nav_by_date",
            "selected_fund": fund_name,
            "pageNum": 1
        }
        resp = await self.session.request(method="POST", url=str(self.BASE_URL), data=request_payload)
        resp.raise_for_status()
        html = await resp.text()
        soup = bs4.BeautifulSoup(html, 'html.parser')

        price_histories = []
        price_histories_html = soup.find_all("tr")
        for elm in price_histories_html:
            columns = elm.find_all("td")
            if len(columns) == 0:
                continue
            price_histories.append({
                "update_date": datetime.strptime(columns[0].text, "%d/%m/%Y"),
                "dealing_date": datetime.strptime(columns[1].text, "%d/%m/%Y"),
                "nav_price": numbers.vncurrencyformat_tofloat(columns[2].text),
                "net_change": numbers.float_(columns[3].text),
                "probation_change": float(columns[4].text.replace("%", "")),
            })
        return price_histories


async def nav_today_by_fund(crawler: ajax, fund: Fund) -> Union[FundNavPriceHistory, None]:
    resultset = await crawler.fetch_nav_price_history(fund.code_alias)
    if not resultset or len(resultset) == 0:
        return None
    latest_result = resultset[0]
    latest_change = FundNavPriceHistory(fund.id, fund.code_alias)
    latest_change.dealing_date = latest_result["dealing_date"]
    latest_change.update_date = latest_result["update_date"]
    latest_change.price = latest_result["nav_price"]
    latest_change.net_change = latest_result["net_change"]
    latest_change.probation_change = latest_result["probation_change"]

    if not existed(latest_change):
        mark_active(latest_change)
        return latest_change
    return None


async def nav_today():
    funds = list_dcfvm(update_today=True)

    async with aiohttp.ClientSession() as session:
        crawler = ajax(session=session)
        tasks = []
        for fund in funds:
            if not fund.has_updated_today():
                tasks.append(nav_today_by_fund(crawler, fund))

        result = await asyncio.gather(*tasks)
        return result
