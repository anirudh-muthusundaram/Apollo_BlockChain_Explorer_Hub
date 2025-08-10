# src/agents/account_agent.py
from typing import List
from src.models import AddressIn, AccountOut, TokenBalance
from src.web3_client import native_balance, erc20_balance, w3

def get_account_info(address: str, tokens: List[str] = None) -> AccountOut:
    native = native_balance(address)
    erc20s = []
    if tokens:
        for t in tokens:
            try:
                b = erc20_balance(t, address)
                erc20s.append(TokenBalance(
                    token_address=t,
                    symbol=b.get("symbol"),
                    raw=b["raw"],
                    human=b["human"],
                    decimals=b["decimals"]
                ))
            except Exception:
                continue
    return AccountOut(address=address, native_balance=float(native), erc20_balances=erc20s)