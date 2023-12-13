import asyncio
import json
import aiohttp
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv

async def main(threshold:float = 1.0):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL_TOKEN_DAY) as response:
                response.raise_for_status()
                assert response.status == 200
                day = json.loads(await response.read())
        except Exception as e:
            print(f"Get error: to {API_URL_TOKEN_DAY} as {e}")
        finally:
            await session.close()
            
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL_TOKEN_DAY) as response:
                response.raise_for_status()
                assert response.status == 200
                seven_day = json.loads(await response.read())
        except Exception as e:
            print(f"Get error: to {API_URL_TOKEN_DAY} as {e}")
        finally:
            await session.close()
    
    day_eu = day.get("eu", {})    
    seven_day_eu = seven_day.get("eu", {})
    low = seven_day_eu.get('7_day_low', "N/A")
    high = seven_day_eu.get('7_day_high', "N/A")
    med = (high + low) / 2
    current_price = day_eu.get('current_price', 'N/A')
    time_of_change = day_eu.get('time_of_last_change_utc_timezone', 'N/A')
    
    FORMAT_FROM = "%Y-%m-%d %H:%M:%S"
    FORMAT_TO = "%H:%M"
    last_update_time = datetime.strptime(time_of_change, FORMAT_FROM)
    last_update_time = last_update_time + timedelta(hours=1)
    last_update_time = last_update_time.strftime(FORMAT_TO)
    
    med_with_treshold = med*threshold
    
    if(current_price<med_with_treshold):
        message = f"Currently: {current_price:,} 💰"+ f" as of {last_update_time} 🕛"
        # message = message + f"\n{API_URL_TOKEN_GRAPH}"
        
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
                    _ = json.loads(await response.read())
            except Exception as e:
                print(f"Get error: to {API_URL_NTFY_SERVER} as {e}")
            finally:
                await session.close()

if __name__ == '__main__':
    load_dotenv()
    
    API_URL_TOKEN_DAY:str = "https://wowtokenprices.com/current_prices.json"
    API_URL_TOKEN_SEVEN_DAY:str = "https://wowtokenprices.com/history_prices_7_day.json"
    NTFY_TOPIC:str = "wowtokens"
    API_URL_NTFY_SERVER:str = getenv("NTFY_SERVER_URL")+f"/{NTFY_TOPIC}/trigger"
    API_URL_TOKEN_GRAPH:str = "https://wowtokenprices.com"

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(threshold=1.033))

# sudo docker run -v /var/cache/ntfy:/var/cache/ntfy -v /etc/ntfy:/etc/ntfy -p 80:80 -itd binwiederhier/ntfy serve --cache-file /var/cache/ntfy/cache.db
# crontab -e
