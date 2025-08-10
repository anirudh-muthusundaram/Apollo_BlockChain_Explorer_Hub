# src/server.py
from fastmcp import FastMCP
from dotenv import load_dotenv
import os
from src.agents.chain_agent import get_chain_info
from src.agents.account_agent import get_account_info
from src.agents.tx_agent import get_tx_status, get_fee_estimate
from src.agents.analytics_agent import top_token_holders

load_dotenv()
HOST = os.getenv("MCP_HOST", "127.0.0.1")
PORT = int(os.getenv("MCP_PORT", 4000))

mcp = FastMCP("Blockchain Explorer Hub")

# import functions
# from agents.chain_agent import get_chain_info
# from agents.account_agent import get_account_info
# from agents.tx_agent import get_tx_status, get_fee_estimate
# from agents.analytics_agent import top_token_holders

@mcp.tool()
def chain_info() -> dict:
    return get_chain_info().dict()

@mcp.tool()
def account_info(address: str, tokens: list = None) -> dict:
    return get_account_info(address, tokens).dict()

@mcp.tool()
def tx_status(tx_hash: str) -> dict:
    return get_tx_status(tx_hash)

@mcp.tool()
def fee_estimate() -> dict:
    return get_fee_estimate()

@mcp.tool()
def top_holders(token_address: str, addresses: list, top_n: int = 10) -> dict:
    return top_token_holders(token_address, addresses, top_n)

if __name__ == "__main__":
    mcp.run()