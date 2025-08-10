# src/agents/analytics_agent.py
from typing import List
from src.agents.account_agent import get_account_info
from src.db import save_analytics_result

def top_token_holders(token_address: str, addresses: List[str], top_n: int = 10):
    holders = []
    for addr in addresses:
        try:
            info = get_account_info(addr, tokens=[token_address])
            bal = info.erc20_balances[0].human if info.erc20_balances else 0.0
            holders.append({"address": addr, "balance": bal})
        except Exception:
            continue
    holders_sorted = sorted(holders, key=lambda x: x["balance"], reverse=True)[:top_n]
    save_analytics_result({"token": token_address, "holders": holders_sorted})
    return holders_sorted