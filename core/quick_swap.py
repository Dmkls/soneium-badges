import asyncio
from web3.exceptions import ContractLogicError, Web3RPCError
import random
import time

from utils.get_coins_price import get_eth_price
from utils.w3 import w3
from utils.transactions_utils import create_dict_transaction, send_txn
from utils.account import Account
from configs import config
from configs.constants import TOKEN_ADDRESSES
from utils.log_utils import logger
from utils.Contracts import Contracts


async def swap(account: Account, token_from: str, token_to: str):
    token_from, token_to = token_from.upper(), token_to.upper()
    dict_transaction = await create_dict_transaction(account.wallet_address, multiplier=5)
    eth_price = await get_eth_price()

    amount = 0
    usdc_to_get = 0

    if token_from == 'ETH' and token_to == "USDC":
        precision = 10 ** 8
        amount = random.randint(
            int(config.QS_ETH_TO_USDC_AMOUNT[0] * precision),
            int(config.QS_ETH_TO_USDC_AMOUNT[1] * precision)
        ) * 10**10
        usdc_to_get = int(amount / 10 ** 12 * eth_price * 0.80)

    dict_transaction['value'] = amount

    try:
        txn_swap = await Contracts.quick_swap_swap.functions.exactInputSingle(
            [
                TOKEN_ADDRESSES[token_from],
                TOKEN_ADDRESSES[token_to],
                "0x0000000000000000000000000000000000000000",
                account.wallet_address,
                round(time.time()) + 60 * 20,
                amount,
                usdc_to_get,
                0
            ]
        ).build_transaction(dict_transaction)

        txn_swap['gas'] = int(txn_swap['gas'] * 1.1)

        txn_hash = await send_txn(txn_swap, account, f"Quick Swap: swap {token_from}->{token_to}")

        await asyncio.sleep(5)
        receipt = await w3.eth.get_transaction_receipt(txn_hash)
        return True if receipt.status == 1 else False

    except ContractLogicError or "insufficient" in Web3RPCError:
        logger.error(f"{account.wallet_address} |Недостаточно {token_from} для транзакции")
    except Web3RPCError as e:
        if 'insufficient funds for transfer' in e.message:
            logger.error(f"{account.wallet_address} | Quick Swap | Недостаточно {token_from} для выполнения свапа {token_from} -> {token_to}")
        else:
            logger.error(f"{account.wallet_address} | Quick Swap | Произошла ошибка: {e} во время выполнения свапа {token_from} -> {token_to}")
    except Exception as e:
        logger.error(f"{account.wallet_address} | Quick Swap | Произошла ошибка: {e} во время аппрува")

    return False
