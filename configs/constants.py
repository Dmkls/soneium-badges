import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

LOG_DIR = os.path.join(ROOT_DIR, "log")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
CONFIGS_DIR = os.path.join(ROOT_DIR, "configs")
DATA_DIR = os.path.join(ROOT_DIR, "data")

PRIVATE_KEYS_PATH = os.path.join(CONFIGS_DIR, "private_keys.txt")
PROXIES_PATH = os.path.join(CONFIGS_DIR, "proxies.txt")
FAILED_PATH = os.path.join(RESULTS_DIR, 'failed.txt')
SUCCESS_PATH = os.path.join(RESULTS_DIR, 'success.txt')
DATABASE_PATH = os.path.join(DATA_DIR, 'data.db')
LOG_PATH = os.path.join(LOG_DIR, 'log.log')

TOKEN_ADDRESSES = {
    "ETH": "0x4200000000000000000000000000000000000006",
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDC": "0xbA9986D2381edf1DA03B0B9c1f8b00dc4AacC369",
    "USDT": "0x3A337a6adA9d885b6Ad95ec48F9b75f197b5AE35"
}