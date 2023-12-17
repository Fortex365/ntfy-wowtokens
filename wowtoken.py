import asyncio
import json
import aiohttp
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv

async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            assert response.status == 200
            return await response.read()
    except Exception as e:
        print(f"HTTP Error (GET): to {url} thrown an exception:\n {e}")
        return None

async def main(threshold: float = 1.0):
    load_dotenv()
    
    API_URL_TOKEN_CURRENT = "https://wowtokenprices.com/current_prices.json"
    API_URL_TOKEN_SEVEN_DAY = "https://wowtokenprices.com/history_prices_7_day.json"
    API_URL_TOKEN_THIRTY_DAYS = "https://wowtokenprices.com/history_prices_30_day.json"
    NTFY_TOPIC = getenv("NTFY_TOPIC")
    API_URL_NTFY_SERVER = getenv("NTFY_SERVER_URL") + f"/{NTFY_TOPIC}/trigger"
    
    async with aiohttp.ClientSession() as session:
        current_data = await fetch_data(session, API_URL_TOKEN_CURRENT)
        seven_day_data = await fetch_data(session, API_URL_TOKEN_SEVEN_DAY)
    
    if current_data is None:
        print(f"External server error: response request can't be parsed for daily. Original response:\n{current_data}")
        return
    if seven_day_data is None:
        print(f"External server error: response request can't be parsed for weekly. Original response:\n{seven_day_data}")
        return
    
    current_data:list = json.loads(current_data).get("eu", {})
    seven_day_eu:list = json.loads(seven_day_data).get("eu", {})
    
    current_price:int = current_data.get('current_price', 'N/A')
    low_7:int = current_data.get('7_day_low', 'N/A')
    high_7 = current_data.get('7_day_high', 'N/A')
    low_30:int = current_data.get('30_day_low', 'N/A')
    high_30 = current_data.get('30_day_high', 'N/A')
    
    median:int = (low_7 + high_7) / 2
    time_of_change = current_data.get('time_of_last_change_utc_timezone', 'N/A')
    
    FORMAT_FROM = "%Y-%m-%d %H:%M:%S"
    FORMAT_TO = "%H:%M"
    
    last_update_time = datetime.strptime(time_of_change, FORMAT_FROM)
    last_update_time = last_update_time + timedelta(hours=1)
    last_update_time = last_update_time.strftime(FORMAT_TO)
    
    med_with_threshold = median * threshold
    
    if current_price > med_with_threshold:
        message = f"Currently: {current_price:,} 💰" + f" as of {last_update_time} 🕛"
        message = message + f"\n7_low: {low_7:,}\t 7_high: {high_7:,}"
        
        header = {
            "Priority": "high",
            "Tags": "ghost",
            "Title": "WoW Token Spy"
        }
        payload = f"{message}".encode(encoding='utf-8')
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(API_URL_NTFY_SERVER, headers=header, data=payload) as response:
                    response.raise_for_status()
                    assert response.status == 200
            except Exception as e:
                print(f"HTTP Error (GET): to {API_URL_NTFY_SERVER} thrown an exception:\n {e}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(threshold=1.033))


# sudo docker run -v /var/cache/ntfy:/var/cache/ntfy -v /etc/ntfy:/etc/ntfy -p 80:80 -itd binwiederhier/ntfy serve --cache-file /var/cache/ntfy/cache.db
# crontab -e
