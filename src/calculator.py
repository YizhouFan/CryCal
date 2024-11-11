import csv
import sys
from dateutil import parser
from tqdm import tqdm

from custom_types import Transaction, Product


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


def make_annual_report(year: int, annual_trade_data: list[Transaction], annual_reports: dict[int, dict[str, Product]]):
    unique_products = set([t["product"] for t in annual_trade_data])
    product_annual_reports = {}
    for product in unique_products:
        if "/" not in product:
            # only look at crypto/JPY pairs
            continue
        # print(product)
        product_trade_data_buy = [t for t in annual_trade_data if t["product"] == product and t["type"] == "Buy"]
        product_trade_data_sell = [t for t in annual_trade_data if t["product"] == product and t["type"] == "Sell"]
        # print(product_trade_data_buy)
        product_total_buy_amount = sum([t["amount"] for t in product_trade_data_buy])
        product_total_buy_price_jpy = sum([t["total_price_jpy"] for t in product_trade_data_buy])
        product_total_sell_amount = sum([t["amount"] for t in product_trade_data_sell])
        product_annual_report: Product = {
            "name": product,
            "total_buy_amount": product_total_buy_amount,
            "total_buy_price_jpy": product_total_buy_price_jpy,
            "total_sell_amount": product_total_sell_amount,
            "annual_average_price_jpy": product_total_buy_price_jpy / product_total_buy_amount,
            "eoy_remaining_amount": product_total_buy_amount - product_total_sell_amount,
        }
        product_annual_reports[product] = product_annual_report
    annual_reports[year] = product_annual_reports


def current_year_enough_amount(transaction: Transaction, annual_trade_data: list[Transaction]):
    return True


def calculate_sell_profit(
    sell_transaction: Transaction, trade_data: list[Transaction], annual_reports: dict[int, dict[str, Product]]
):
    if current_year_enough_amount(sell_transaction, [t for t in trade_data if t["year"] == sell_transaction["year"]]):
        profit = (
            sell_transaction["total_price_jpy"]
            - sell_transaction["amount"]
            * annual_reports[sell_transaction["year"]][sell_transaction["product"]]["annual_average_price_jpy"]
        )
    else:
        profit = -1
    return profit


def calculate_amount_distribution(
    trade_data: list[Transaction], wallet_status: dict[str, dict[int, float]], min_year: int, max_year: int
):
    # assume transactions are ordered from oldest to latest
    for i in range(len(trade_data)):
        t = trade_data[i]
        if t["type"] == "Buy":
            wallet_status[t["product"]][t["year"]] += t["amount"]
        elif t["type"] == "Sell":
            year = t["year"]
            remainder = t["amount"]
            while year >= min_year:
                # check amount of crypto of current year,
                if wallet_status[t["product"]][year] >= remainder:
                    wallet_status[t["product"]][year] -= remainder
                    break
                else:
                    # if not enough for selling, always use up all amount of current year,
                    # then check one year back, and so on and so forth
                    # this is my interpretation of the laws in Japan
                    wallet_status[t["product"]][year] = 0.0
                    remainder = remainder - wallet_status[t["product"]][t["year"]]
                year -= 1
            assert remainder > 0, f"Error: Not enough {t["product"]} to sell for {t["id"]}"
        t["post_txn_wallet_status"] = wallet_status


def main(args):
    csv_path = args[1]
    trade_data = load_trade_history(csv_path)

    min_year = min([t["year"] for t in trade_data])
    max_year = max([t["year"] for t in trade_data])
    all_products = set([t["product"] for t in trade_data if "/" in t["product"]])  # all crypto/JPY pairs

    annual_reports = {}
    for year in range(min_year, max_year + 1):
        make_annual_report(year, [t for t in trade_data if t["year"] == year], annual_reports)
    print(annual_reports)

    wallet_status = {p: {y: 0.0 for y in range(min_year, max_year + 1)} for p in all_products}

    calculate_amount_distribution(trade_data, wallet_status, min_year, max_year)
    print(trade_data)

    sys.exit()
    sell_profit = {}
    for transaction in trade_data:
        if transaction["type"] == "Sell":
            profit = calculate_sell_profit(transaction, trade_data, annual_reports)
            sell_profit[transaction["id"]] = profit

    print(sell_profit)
    # print(trade_data[:10])


if __name__ == "__main__":
    main(sys.argv)
