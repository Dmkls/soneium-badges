from web3 import AsyncWeb3

from utils.file_utils import read_json
from utils.w3 import w3

class Contracts:

    # Quick Swap: swap
    # ETH to stable
    __quick_swap_swap_contract_address = AsyncWeb3.to_checksum_address("0xeba58c20629ddab41e21a3E4E2422E583ebD9719")
    __quick_swap_swap_abi = read_json("./data/abis/quick_swap_abi.json")
    quick_swap_swap = w3.eth.contract(__quick_swap_swap_contract_address, abi=__quick_swap_swap_abi)


    # Untitled bank
    # approve
    __untitled_bank_approve_contract_address = AsyncWeb3.to_checksum_address("0x905108D47409068Bbd771f7a5d8a89AFDA94050D")
    __untitled_bank_approve_abi = read_json("./data/abis/untitled_bank_abi_approve.json")
    untitled_bank_approve = w3.eth.contract(__untitled_bank_approve_contract_address, abi=__untitled_bank_approve_abi)

    # deposit
    __untitled_bank_deposit_contract_address = AsyncWeb3.to_checksum_address("0x905108D47409068Bbd771f7a5d8a89AFDA94050D")
    __untitled_bank_deposit_abi = read_json("./data/abis/untitled_bank_abi_deposit.json")
    untitled_bank_deposit = w3.eth.contract(__untitled_bank_deposit_contract_address, abi=__untitled_bank_deposit_abi)