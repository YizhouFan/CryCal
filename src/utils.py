import csv

from dateutil import parser
from tqdm import tqdm

from custom_types import Transaction


def verify_trade_history(trade_history: list):
    assert trade_history
    assert trade_history[0] == [
        '\ufeff"Trade Date"',
        "Product",
        "Trade Type",
        "Traded Price",
        "Currency 1",
        "Amount (Currency 1)",
        "Fee",
        "JPY Rate (Currency 1)",
        "Currency 2",
        "Amount (Currency 2)",
        "Fees (JPY)",
        "Tax category",
        "Counter Party",
        "Order ID",
        "Details",
    ]
    for row in trade_history:
        assert len(row) == 15


def convert_trade_history(trade_history: list, default_fee_rate: float = 0.001):
    result = []
    for row in tqdm(trade_history[1:]):
        ts_str = row[0]
        ts_datetime = parser.parse(ts_str)
        total_price_jpy = abs(float(row[9].replace(",", "")))
        fee_jpy = row[10]
        if fee_jpy:
            fee_jpy = float(fee_jpy.replace(",", ""))
        else:
            # fee can be empty. Use 0.1% as the default fee rate
            fee_jpy = default_fee_rate * total_price_jpy
        transaction: Transaction = {
            "id": row[13],
            "ts": ts_datetime,
            "year": ts_datetime.year,
            "product": row[1],
            "type": row[2],
            "unit_price_jpy": float(row[3].replace(",", "")),
            "currency": row[4],
            "amount": abs(float(row[5].replace(",", ""))),
            "total_price_jpy": total_price_jpy,
            "fee_jpy": fee_jpy,
        }
        result.append(transaction)
    # sort the transaction from oldest to latest
    result = sorted(result, key=lambda d: d["ts"])
    return result


def load_trade_history(csv_path):
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(
            csv_file,
            delimiter=",",
        )
        data = [row for row in csv_reader]

    verify_trade_history(data)
    return convert_trade_history(data)
