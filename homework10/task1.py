import asyncio
import time
from collections import namedtuple

import aiohttp
from bs4 import BeautifulSoup


async def fetch(session, url):
    # Get page content.
    async with session.get(url) as response:
        return await response.content.read()


async def fetch_all(urls, loop):
    # Get all pages content.
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls])
        return results


async def get_exchange_rate():
    # Get current rate USD-RUB.
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


if __name__ == "__main__":
    start = time.time()

    BASE_URL = "https://markets.businessinsider.com"
    LOOP = asyncio.get_event_loop()

    Company = namedtuple("Company", "price code pe growth profit52")

    companies_lists_urls = [
        BASE_URL + f"/index/components/s&p_500?p={i}" for i in range(1, 11)
    ]

    print(
        "Current exchange USD-RUB rate: {}".format(
            LOOP.run_until_complete(get_exchange_rate())
        )
    )

    htmls = LOOP.run_until_complete(fetch_all(companies_lists_urls, LOOP))

    companies = []

    for html in htmls:
        soup = BeautifulSoup(html, "lxml")

        for i in soup.find(class_="table table-small").find_all("tr")[1:]:
            company_data = i.text.split()

            name = company_data[0]
            growth = float(company_data[-1][:-1])

            company_href = BASE_URL + i.find("a").get("href")
            company_data.append(company_href)
            companies.append(company_data)
            print(company_data)

    # companies_urls = [i[-1] for i in companies]
    #
    # companies_htmls = LOOP.run_until_complete(fetch_all(companies_urls, LOOP))
    #
    # for html in companies_htmls:
    #     soup = BeautifulSoup(html, 'lxml')
    #     price = soup.find(class_="price-section__current-value").text.split()[0]
    #     code = soup.find(class_="price-section__category").text.split()[-1]
    #     pe = soup.find(class_="responsivePosition", id="snapshot").find_all(class_="snapshot__data-item")[8].text.split()[0]
    #     # growth = soup.find()
    #     print(price, code, pe)
    print("Time: ", time.time() - start)
