import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta
from typing import List, Dict
from aiofile import AIOFile, Writer
from aiopath import AsyncPath
import websockets

API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
DEFAULT_CURRENCIES = ["EUR", "USD"]

class PrivatBankAPIClient:
    async def fetch_rates_for_date(self, session: aiohttp.ClientSession, date: str) -> Dict:
        url = API_URL.format(date=date)
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"date": date, "error": f"Status: {response.status}"}
        except aiohttp.ClientError as e:
            return {"date": date, "error": str(e)}

class CurrencyRateService:
    def __init__(self, currencies: List[str]):
        self.currencies = currencies
        self.client = PrivatBankAPIClient()

    async def get_currency_rates(self, days: int) -> List[Dict]:
        results = []
        async with aiohttp.ClientSession() as session:
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y")
                data = await self.client.fetch_rates_for_date(session, date)
                if "exchangeRate" in data:
                    rates = {}
                    for item in data["exchangeRate"]:
                        currency = item.get("currency")
                        if currency in self.currencies:
                            rates[currency] = {
                                "sale": item.get("saleRate"),
                                "purchase": item.get("purchaseRate")
                            }
                    results.append({data["date"]: rates})
        return results

async def log_exchange_command(command: str):
    log_path = AsyncPath("exchange.log")
    async with AIOFile(log_path, "a") as afp:
        writer = Writer(afp)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await writer(f"[{timestamp}] Executed command: {command}\n")

async def websocket_handler(websocket):
    async for message in websocket:
        if message.startswith("exchange"):
            parts = message.split()
            days = int(parts[1]) if len(parts) > 1 else 1
            currencies = parts[2:] if len(parts) > 2 else DEFAULT_CURRENCIES

            if days > 10:
                await websocket.send("You can only request up to 10 days of data.")
                continue

            await log_exchange_command(message)
            service = CurrencyRateService(currencies)
            result = await service.get_currency_rates(days)
            response_lines = []
            for day_data in result:
                for date, rates in day_data.items():
                    response_lines.append(f"{date}:")
                    for cur, val in rates.items():
                        response_lines.append(f"  {cur}: Sale - {val['sale']}, Purchase - {val['purchase']}")
            await websocket.send("\n".join(response_lines))
        else:
            await websocket.send(f"Unknown command: {message}")

async def main():
    parser = argparse.ArgumentParser(description="Get exchange rates from PrivatBank")
    parser.add_argument("--ws", action="store_true", help="Run as WebSocket server")
    parser.add_argument("days", type=int, help="Number of days (max 10)", nargs="?", default=1)
    parser.add_argument("--currencies", nargs="*", default=DEFAULT_CURRENCIES, help="Currencies to fetch")
    args = parser.parse_args()

    if args.ws:
        async with websockets.serve(websocket_handler, "localhost", 8765):
            print("WebSocket server started on ws://localhost:8765")
            await asyncio.Future()  # run forever
    else:
        if args.days > 10:
            print("You can only request up to 10 days of data.")
            return
        await log_exchange_command(f"exchange {args.days} {' '.join(args.currencies)}")
        service = CurrencyRateService(args.currencies)
        result = await service.get_currency_rates(args.days)
        print(result)

if __name__ == '__main__':
    asyncio.run(main())


# WebSocket-сервер, який приймає команди:
# exchange — поточний курс валют.
# exchange N — курс за останні N днів (до 10).
# exchange N USD EUR PLN — обрані валюти.
# Логування команд у exchange.log за допомогою aiofile та aiopath.
# Запуск у WebSocket-режимі:
# python main_3.py --ws
# Запуск CLI-режиму:
# python main.py 3 --currencies EUR USD PLN