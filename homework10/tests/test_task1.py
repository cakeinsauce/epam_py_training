from unittest import mock
from unittest.mock import MagicMock

import pytest
from task1 import *


def async_return(result):
    res = asyncio.Future()
    res.set_result(result)
    return res.result()


@pytest.mark.asyncio
@mock.patch("task1.fetch", return_value=async_return(b"Foo\n"))
async def test_fetch_all(mock_fetch):
    # Testing fetch_all
    actual_result = await fetch_all(["1", "2", "3"], asyncio.get_event_loop())
    assert actual_result == [b"Foo\n", b"Foo\n", b"Foo\n"]


xml_exchange = bytes(
    '<Valute ID="R01235"><NumCode>840</NumCode><CharCode>USD</CharCode>'
    "<Nominal>1</Nominal><Name>Доллар США</Name> <Value>75</Value></Valute>",
    "utf-8",
)


@pytest.mark.asyncio
@mock.patch("task1.fetch", return_value=async_return(xml_exchange))
async def test_get_exchange_rate(mock_fetch):
    # Testing get_exchange_rate function.
    actual_result = await get_exchange_rate()
    assert actual_result == 75.0


html_profit_rate = bytes(
    "<div>"
    "1,200"
    '<div class="snapshot__header">52 Week High</div>'
    "</div>"
    "<div>"
    "800"
    '<div class="snapshot__header">52 Week Low</div>'
    "</div>",
    "utf-8",
)


@pytest.mark.asyncio
async def test_get_profit_rate():
    # Testing get_profit_rate
    actual_result = await get_profit_rate(BeautifulSoup(html_profit_rate))
    assert actual_result == 50.0


@pytest.mark.asyncio
async def test_no_profit_rate_on_page():
    # Testing get_profit_rate when there's no week low and week hight on a page.
    actual_result = await get_profit_rate(BeautifulSoup(b"Nothing\n"))
    assert actual_result is None


html_pe_ratio = bytes(
    '<div class="snapshot__data-item">'
    "       19.91  "
    '<div class="snapshot__header">P/E Ratio</div>'
    "</div>",
    "utf-8",
)


@pytest.mark.asyncio
async def test_get_pe_ratio():
    # Testing get_pe_ratio
    actual_result = await get_pe_ratio(BeautifulSoup(html_pe_ratio))
    assert actual_result == 19.91


@pytest.mark.asyncio
async def test_no_pe_ratio_on_page():
    # Testing get_pe_ratio when there's no p/e ratio on a page.
    actual_result = await get_pe_ratio(BeautifulSoup(b"Nothing"))
    assert actual_result is None


html_price = bytes('<span class="price-section__current-value">200   </span>', "utf-8")


@pytest.mark.asyncio
async def test_get_price():
    # Testing get_price
    actual_result = await get_price(BeautifulSoup(html_price), 100)
    assert actual_result == 20000


@pytest.mark.asyncio
async def test_no_price_on_page():
    # Testing get_price when there's no price on a page.
    actual_result = await get_price(BeautifulSoup(b"Nothing"), 100)
    assert actual_result is None


company_table_html = bytes(
    "<tr>"
    "<td>"
    '<a href="/stocks/mmm-stock" title="3M"> 3M</a>'
    "</td>"
    '<td class="text-right">'
    '<span class="colorGreen"> 56.80</span><br>'
    '<span class="colorGreen"> 40.13%</span>'
    "</td>"
    "</tr>",
    "utf-8",
)

company_page_html = bytes(
    '<span class="price-section__category">'
    " Stock "
    "<span>"
    ", MMM"
    "</span></span>",
    "utf-8",
)


@pytest.mark.asyncio
@mock.patch("task1.fetch", return_value=async_return(b"<div>Foo</div>"))
@mock.patch("task1.BeautifulSoup", return_value=BeautifulSoup(company_page_html))
@mock.patch("task1.get_price", return_value=async_return(1000))
@mock.patch("task1.get_pe_ratio", return_value=async_return(10))
@mock.patch("task1.get_profit_rate", return_value=async_return(30))
async def test_parse_company(mock_fetch, mock_soup, mock_price, mock_pe, mock_profit):
    # Testing parse_company
    actual_result = await parse_company(
        BeautifulSoup(company_table_html), asyncio.get_event_loop(), "1", 100
    )
    assert actual_result == {
        "name": "3M",
        "code": "MMM",
        "price": 1000,
        "pe": 10,
        "growth": 40.13,
        "profit": 30,
    }
