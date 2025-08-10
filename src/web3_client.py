# src/web3_client.py
from web3 import Web3
import os
from dotenv import load_dotenv
import requests

load_dotenv()

WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL")
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

# Simple health
def is_connected():
    return w3.is_connected()

# Chain info
def latest_block():
    block = w3.eth.get_block('latest')
    return {
        "number": block.number,
        "hash": block.hash.hex(),
        "gasUsed": block.gasUsed,
        "difficulty": getattr(block, "difficulty", None) or getattr(block, "totalDifficulty", None),
    }

# Get native balance (wei -> ether)
def native_balance(address: str):
    bal = w3.eth.get_balance(address)
    return w3.from_wei(bal, "ether")

# ERC20 balance (standard ABI for balanceOf)
ERC20_ABI = [
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
    {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},
    {"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"},
]

def erc20_balance(token_address: str, owner_address: str):
    token = w3.eth.contract(address=w3.to_checksum_address(token_address), abi=ERC20_ABI)
    raw = token.functions.balanceOf(w3.to_checksum_address(owner_address)).call()
    try:
        decimals = token.functions.decimals().call()
    except Exception:
        decimals = 18
    symbol = None
    try:
        symbol = token.functions.symbol().call()
    except:
        pass
    human = raw / (10**decimals)
    return {"raw": raw, "human": human, "decimals": decimals, "symbol": symbol}

# Tx status
def get_tx_receipt(tx_hash: str):
    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        return dict(receipt)
    except Exception:
        return None

# Fee estimation — we can use web3.eth.max_priority_fee / gasPrice depending
def estimate_fee():
    # EIP-1559 style: baseFee + priority
    try:
        block = w3.eth.get_block('pending')
        base_fee = getattr(block, "baseFeePerGas", None)
        priority = w3.eth.max_priority_fee
        return {"baseFee": base_fee, "priority": priority}
    except Exception:
        return {}