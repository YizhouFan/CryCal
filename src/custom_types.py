from typing import TypedDict
from datetime import datetime


class Transaction(TypedDict):
    id: str
    ts: datetime
    year: int
    product: str
    type: str
    unit_price_jpy: float
    total_price_jpy: float
    currency: str
    amount: float
    fee_fpy: float
    post_txn_wallet_status: dict


class Product(TypedDict):
    name: str
    total_buy_amount: float
    total_buy_price_jpy: float
    total_sell_amount: float
    annual_average_price_jpy: float
    eoy_remaining_amount: float
