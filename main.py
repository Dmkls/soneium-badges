from random import randint

from core import quick_swap
from core import untitled_bank
from utils.account import Account
from configs import config
from utils.file_utils import read_private_keys, read_proxies
from utils.log_utils import logger
import asyncio

PRIVATE_KEYS = read_private_keys()
PROXIES = read_proxies()

async def process_account(private_key):
    account = Account(private_key)

    if config.QS_ENABLE:
        logger.success(f"{account.wallet_address} | Quick Swap | Начинаю делать")
        successes = 0
        failed = 0
        while successes < config.QS_TOTAL_TRANSACTIONS and failed < 5:
            if await quick_swap.swap(account, "ETH", "USDC"):
                successes += 1
                logger.info(f"{account.wallet_address} | Quick Swap | Сделал свап, всего: {successes}/{config.QS_TOTAL_TRANSACTIONS}")
            else:
                failed += 1
                logger.error(f"{account.wallet_address} | Quick Swap | Не удалось сделать депозит")
            await asyncio.sleep(randint(config.QS_DELAY_BETWEEN_SWAPS[0], config.QS_DELAY_BETWEEN_SWAPS[1]))

    if config.UB_ENABLE:
        logger.success(f"{account.wallet_address} | Untitled bank | Начинаю делать")
        successes = 0
        failed = 0
        if await untitled_bank.approve(account):
            while successes < config.UB_TOTAL_TRANSACTION and failed < 5:
                if await untitled_bank.deposit(account):
                    successes += 1
                    logger.info(f"{account.wallet_address} | Untitled bank | Сделал депозит, всего: {successes}/{config.UB_TOTAL_TRANSACTION}")
                else:
                    failed += 1
                    logger.error(f"{account.wallet_address} | Untitled bank | Не удалось сделать депозит")
                await asyncio.sleep(config.UB_DELAY_BETWEEN_DEPOSITS[0], config.UB_DELAY_BETWEEN_DEPOSITS[1])

async def start():
    for private_key in PRIVATE_KEYS:
        asyncio.create_task(process_account(private_key))
        await asyncio.sleep(0.1)
    await asyncio.sleep(float("inf"))

if __name__ == '__main__':
    asyncio.run(start())