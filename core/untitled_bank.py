import asyncio
from web3 import AsyncWeb3
import random

from utils.w3 import w3
from utils.transactions_utils import create_dict_transaction, send_txn
from utils.account import Account
from utils.log_utils import logger
from utils.Contracts import Contracts
from configs import config


async def approve(account: Account) -> bool:
    dict_transaction = await create_dict_transaction(account.wallet_address, multiplier=1.6)

    try:
        txn_approve = await Contracts.untitled_bank_approve.functions.approve(
            AsyncWeb3.to_checksum_address("0x2469362f63e9f593087EBbb5AC395CA607B5842F"),
            1000000
        ).build_transaction(dict_transaction)

        txn_hash = await send_txn(txn_approve, account, f"Untitled bank: approve")

        await asyncio.sleep(10)
        receipt = await w3.eth.get_transaction_receipt(txn_hash)
        return True if receipt.status == 1 else False

    except Exception as e:
        logger.error(f"{account.wallet_address} | Untitled bank | Произошла ошибка: {e} во время аппрува")

        return False


async def deposit(account: Account) -> bool:
    dict_transaction = await create_dict_transaction(account.wallet_address, multiplier=1.6)

    amount_in_wei = int(config.UB_AMOUNT_TO_DEPOSITS * 10 ** 6)

    amount = random.randint(amount_in_wei, int(amount_in_wei * 1.1)) if random.randint(1, 100) > 80 else amount_in_wei

    try:
        txn_swap = await Contracts.untitled_bank_deposit.functions.supplyCollateral(
            5,
            amount,
            '0x'
        ).build_transaction(dict_transaction)

        txn_hash = await send_txn(txn_swap, account, f"Untitled bank: deposit")

        await asyncio.sleep(5)
        receipt = await w3.eth.get_transaction_receipt(txn_hash)
        return True if receipt.status == 1 else False

    except Exception as e:
        logger.error(f"{account.wallet_address} | Untitled bank | Произошла ошибка: {e} во время депозита")

        return False
