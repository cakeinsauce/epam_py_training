import asyncio
import time
from collections import namedtuple
from typing import List, Union

import aiohttp
from bs4 import BeautifulSoup


async def fetch(session: aiohttp.ClientSession, url: str) -> bytes:
    """Return content of the given url's page."""
    async with session.get(url) as response:
        return await response.content.read()


async def fetch_all(urls: List[str], loop) -> List[bytes]:
    """Return list of htmls of all pages at the given urls."""
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls])
        return results


async def get_exchange_rate() -> float:
    """Return current exchange rate USD-RUB."""
    exch_url = "http://www.cbr.ru/scripts/XML_daily.asp"
    async with aiohttp.ClientSession() as session:
        res = await fetch(session, exch_url)
    rate = (
        BeautifulSoup(res, "lxml")
        .find(id="R01235")
        .find("value")
        .text.replace(",", ".")
    )
    return float(rate)


async def get_profit_rate(soup: BeautifulSoup) -> Union[float, None]:
    """Return annual profit rate in percents if it's there, None otherwise."""
    try:
        side_chart = soup.find_all(class_="snapshot__highlow")[1].text.split()

        a = float(side_chart[0].replace(",", ""))
        b = float(side_chart[4].replace(",", ""))

        profit = round((b - a) / a * 100, 2)
    except:
        profit = None
    return profit


async def get_pe_ratio(soup: BeautifulSoup) -> Union[float, None]:
    """Return P/E ration if it's there, None otherwise."""
    try:
        pe = float(
            soup.find(class_="snapshot__header", text="P/E Ratio").parent.text.split()[
                0
            ]
        )
    except:
        pe = None
    return pe


async def get_price(soup: BeautifulSoup, exch_rate: float) -> Union[float, None]:
    """Return price of the company in Rubles."""
    try:
        price = round(
            float(
                soup.find(class_="price-section__current-value")
                .text.split()[0]
                .replace(",", "")
            )
            * exch_rate,
            2,
        )
    except:
        price = None
    return price


async def parse_company(
    company, loop: asyncio.AbstractEventLoop, base_url: str, exch_rate: float
) -> namedtuple:
    """Return info about given company."""
    company_data = company.text.split()

    name = company.find("a").get("title")
    growth = float(company_data[-1][:-1])

    company_href = base_url + company.find("a").get("href")

    company_html = await fetch_all([company_href], loop)

    company_soup = BeautifulSoup(company_html[0], "lxml")

    price = await get_price(company_soup, exch_rate)
    code = company_soup.find(class_="price-section__category").text.split()[-1]
    profit = await get_profit_rate(company_soup)
    pe = await get_pe_ratio(company_soup)

    Company = namedtuple("Company", "name code price pe growth profit")

    return Company(name, code, price, pe, growth, profit)


async def main():
    LOOP = asyncio.get_event_loop()
    BASE_URL = "https://markets.businessinsider.com"

    companies_lists_urls = [
        BASE_URL + f"/index/components/s&p_500?p={i}" for i in range(1, 11)
    ]

    print("Current exchange USD-RUB rate: {}".format(await get_exchange_rate()))

    print("Name | Code | Price | P/E | Growth | Profit")
    htmls = await fetch_all(companies_lists_urls, LOOP)
    exch_rate = await get_exchange_rate()

    async def one_iteration(company_page):
        print(await parse_company(company_page, LOOP, BASE_URL, exch_rate))

    coros = [
        one_iteration(company)
        for html in htmls
        for company in BeautifulSoup(html, "lxml")
        .find(class_="table table-small")
        .find_all("tr")[1:]
    ]

    await asyncio.gather(*coros)

    #
    # for html in htmls:
    #     for company in BeautifulSoup(html, "lxml").find(class_="table table-small").find_all("tr")[1:]:
    #         print(await parse_company(company, LOOP, BASE_URL, exch_rate))


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print("Time: ", time.time() - start)
