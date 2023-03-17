import asyncio
import sys

import aiohttp
import datetime
from aiohttp import ClientConnectionError
from pretty_view import ExchangeView

pretty = ExchangeView()


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            result = await res.json()
            return result


async def exchange_for_days(exch: str, days: int):
    list_results = []
    for i in range(days):
        check_day = datetime.date.today() - datetime.timedelta(days=i)
        formatted_date = check_day.strftime("%d.%m.%Y")
        try:
            result = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={formatted_date}')
            if result:
                list_results.append(result)
        except ClientConnectionError as err:
            print(f'Connection error {err}')
    res_list = []
    for el in list_results:
        for exchange_rate in el['exchangeRate']:
            if exchange_rate['currency'] == exch.upper():
                try:
                    res_list.append([el['date'], exchange_rate['purchaseRate'], exchange_rate['saleRate']])
                except KeyError:
                    pass
    if len(res_list) == 0:
        print(f'Не можемо найти курс валюти {exch.upper()}')
    else:
        return print(pretty.create_row(res_list, exch))

if __name__ == '__main__':
    if int(sys.argv[2]) <= 10:
        asyncio.run(exchange_for_days(str(sys.argv[1]).upper(), int(sys.argv[2])))
    else:
        print('Занадто багато днів. Вибери до 10 бо будеш довго чекати мене :)) ')

