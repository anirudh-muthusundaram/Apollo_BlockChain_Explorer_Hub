# src/models.py
from pydantic import BaseModel, Field
from typing import Optional, List

class ChainInfoOut(BaseModel):
    number: int
    hash: str
    gasUsed: int
    difficulty: Optional[int]

class AddressIn(BaseModel):
    address: str

class TokenBalance(BaseModel):
    token_address: Optional[str]
    symbol: Optional[str]
    raw: int
    human: float
    decimals: int

class AccountOut(BaseModel):
    address: str
    native_balance: float
    erc20_balances: List[TokenBalance] = []

class TxStatusIn(BaseModel):
    tx_hash: str

class TxStatusOut(BaseModel):
    status: str  # pending|confirmed|failed
    receipt: Optional[dict]