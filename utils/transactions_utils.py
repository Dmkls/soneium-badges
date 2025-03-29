from web3 import AsyncWeb3
from utils.w3 import w3
from utils.log_utils import logger

async def create_dict_transaction(wallet_address: str, multiplier: float = 1.3) -> dict:
    last_block = await w3.eth.get_block('latest')
    wallet_address = AsyncWeb3.to_checksum_address(wallet_address)
    max_priority_fee_per_gas = await w3.eth.max_priority_fee
    base_fee = int(last_block['baseFeePerGas'] * multiplier)
    max_fee_per_gas = base_fee + max_priority_fee_per_gas

    return {
        'chainId': await w3.eth.chain_id,
        'from': wallet_address,
        'maxPriorityFeePerGas': max_priority_fee_per_gas,
        'maxFeePerGas': max_fee_per_gas,
        'nonce': await w3.eth.get_transaction_count(wallet_address),
    }

async def send_txn(txn: dict, account, func: str | None = None):
    try:
        signed_txn = w3.eth.account.sign_transaction(txn, account.private_key)
        txn_hash = await w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        logger.success(f"{account.wallet_address} | {func} | {txn_hash.hex()}")
        return txn_hash.hex()
    except Exception as error:
        logger.error(f"{account.wallet_address} | {func} | {error}")