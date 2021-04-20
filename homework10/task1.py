import asyncio
import heapq
import json
import time
from collections import namedtuple
from typing import List, NoReturn, Union

import aiofiles
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
        a = (
            soup.find(class_="snapshot__header", text="52 Week Low")
            .parent.text.split()[0]
            .replace(",", "")
        )
        b = (
            soup.find(class_="snapshot__header", text="52 Week High")
            .parent.text.split()[0]
            .replace(",", "")
        )

        a = float(a)
        b = float(b)

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

    company_href = base_url + company.find("a").get("href")
    company_html = await fetch_all([company_href], loop)
    company_soup = BeautifulSoup(company_html[0], "lxml")

    name = company.find("a").get("title")
    code = company_soup.find(class_="price-section__category").text.split()[-1]
    price = await get_price(company_soup, exch_rate)
    pe = await get_pe_ratio(company_soup)
    growth = float(company_data[-1][:-1])
    profit = await get_profit_rate(company_soup)

    Company = namedtuple("Company", "name code price pe growth profit")

    company_details = Company(name, code, price, pe, growth, profit)._asdict()
    return company_details


async def write_to_json(file_name: str, data: List[dict]) -> NoReturn:
    """Write data to JSON file."""
    async with aiofiles.open(f"{file_name}.json", "w") as outfile:
        await outfile.write(json.dumps(data, indent=4))


async def top_most_expensive(data: List[dict]) -> NoReturn:
    """Write to JSON 10 most expensive companies."""
    key = lambda x: x["price"] if x["price"] else -1
    top = heapq.nlargest(10, data, key=key)
    await write_to_json("most_expensive", top)


async def top_lowest_pe(data: List[dict]) -> NoReturn:
    """Write to JSON 10 companies with the best P/E ratio."""
    key = lambda x: x["pe"] if x["pe"] else 99999
    top = heapq.nsmallest(10, data, key=key)
    await write_to_json("lowest_pe", top)


async def top_best_growth_rate(data: List[dict]) -> NoReturn:
    """Write to JSON 10 fastest growing companies for the last year."""
    top = heapq.nlargest(10, data, key=lambda x: x["growth"])
    await write_to_json("best_growth_rate", top)


async def top_best_potential_profit(data: List[dict]) -> NoReturn:
    """Write to JSON 10 companies with the best potential profit."""
    key = lambda x: x["profit"] if x["profit"] else -999999
    top = heapq.nlargest(10, data, key=key)
    await write_to_json("best_potential_profit", top)


async def main():
    loop = asyncio.get_event_loop()
    base_url = "https://markets.businessinsider.com"

    companies_lists_urls = [
        base_url + f"/index/components/s&p_500?p={i}" for i in range(1, 11)
    ]

    htmls = await fetch_all(companies_lists_urls, loop)
    exch_rate = await get_exchange_rate()

    async def one_iteration(company_page):
        res = await parse_company(company_page, loop, base_url, exch_rate)
        return res

    coros = [
        one_iteration(company)
        for html in htmls
        for company in BeautifulSoup(html, "lxml")
        .find(class_="table table-small")
        .find_all("tr")[1:]
    ]

    result = await asyncio.gather(*coros)

    await asyncio.gather(
        top_most_expensive(result),
        top_lowest_pe(result),
        top_best_growth_rate(result),
        top_best_potential_profit(result),
    )


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print("Time: ", time.time() - start)
