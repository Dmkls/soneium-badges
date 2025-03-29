import aiohttp
from random import choice
from utils.log_utils import logger
from utils.file_utils import read_proxies

ETH_URL = "https://www.binance.com/api/v3/depth?symbol=ETHUSDC&limit=1"
PROXIES = read_proxies()

async def get_eth_price() -> float:
    try:
        proxy = choice(PROXIES)
        async with aiohttp.ClientSession() as session:
            async with session.get(ETH_URL, proxy=proxy) as response:
                response_json = await response.json()
                return float(response_json["asks"][0][0])
    except:
        logger.error("Can't get ETH price")
