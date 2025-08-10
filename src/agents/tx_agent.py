# src/agents/tx_agent.py
from src.web3_client import get_tx_receipt, estimate_fee, w3

def get_tx_status(tx_hash: str):
    receipt = get_tx_receipt(tx_hash)
    if receipt is None:
        try:
            tx = w3.eth.get_transaction(tx_hash)
            if tx:
                return {"status": "pending", "receipt": None}
        except:
            return {"status": "unknown", "receipt": None}
    else:
        status = "confirmed" if receipt.get("status", 1) == 1 else "failed"
        return {"status": status, "receipt": receipt}

def get_fee_estimate():
    return estimate_fee()