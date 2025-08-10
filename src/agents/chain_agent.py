# src/agents/chain_agent.py
from src.web3_client import latest_block, is_connected
from src.models import ChainInfoOut

def get_chain_info() -> ChainInfoOut:
    if not is_connected():
        raise RuntimeError("Web3 provider not connected")
    info = latest_block()
    return ChainInfoOut(**info)