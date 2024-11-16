from datetime import datetime
from typing import TypedDict


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
    fee_jpy: float
    post_txn_wallet_status: dict
    sell_amount_distribution: dict
    sell_profit_jpy: float


class Product(TypedDict):
    name: str
    total_buy_amount: float
    total_buy_price_jpy: float
    average_buy_price_jpy: float
    total_sell_amount: float
    total_sell_price_jpy: float
    average_sell_price_jpy: float
    boy_amount: float
    boy_evaluation_jpy: float
    eoy_amount: float
    eoy_evaluation_jpy: float
    eoy_average_price_jpy: float
    total_profit_jpy: float
