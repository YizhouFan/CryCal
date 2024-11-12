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
            "eoy_remaining_amount": product_total_buy_amount - product_total_sell_amount,  # this is broken right now
            "annual_sell_profit_jpy": 0.0,
        }
        product_annual_reports[product] = product_annual_report
    annual_reports[year] = product_annual_reports


def simulate_trades(
    trade_data: list[Transaction], wallet_status: dict[str, dict[int, float]],
    annual_reports: dict[int, dict[str, Product]], min_year: int, max_year: int
):
    # assume transactions are ordered from oldest to latest
    for i in tqdm(range(len(trade_data))):
        t = trade_data[i]
        if t["type"] == "Buy":
            wallet_status[t["product"]][t["year"]] += t["amount"]
        elif t["type"] == "Sell":
            sell_amount_distribution = {y: 0.0 for y in range(min_year, max_year + 1)}
            year = t["year"]
            remainder = t["amount"]
            while year >= min_year:
                # check amount of crypto of current year,
                if wallet_status[t["product"]][year] >= remainder:
                    wallet_status[t["product"]][year] -= remainder
                    sell_amount_distribution[year] = remainder
                    break
                else:
                    # if not enough for selling, always use up all amount of current year,
                    # then check one year back, and so on and so forth
                    # this is my interpretation of the laws in Japan
                    wallet_status[t["product"]][year] = 0.0
                    remainder = remainder - wallet_status[t["product"]][t["year"]]
                    sell_amount_distribution[year] = wallet_status[t["product"]][year]
                year -= 1
            assert remainder > 0, f"Error: Not enough {t["product"]} to sell for {t["id"]}"
            t["sell_amount_distribution"] = sell_amount_distribution
            sell_profit_jpy = sum([t["total_price_jpy"] - 
                                   sell_amount_distribution[y] * 
                                   annual_reports[y][t["product"]]["annual_average_price_jpy"] 
                                   for y in sell_amount_distribution if sell_amount_distribution[y] > 0])
            t["sell_profit_jpy"] = sell_profit_jpy
            annual_reports[t["year"]][t["product"]]["annual_sell_profit_jpy"] += sell_profit_jpy
        t["post_txn_wallet_status"] = wallet_status


def print_annual_reports(annual_reports: dict[int, dict[str, Product]], min_year: int, max_year: int):
    for year in range(min_year, max_year + 1):
        print(f"{year} ANNUAL PROFIT REPORT")
        print(f"  Total annual profit: {sum([p["annual_sell_profit_jpy"] for p in annual_reports[year].values()]):.0f} JPY")
        print("  Details:")
        for product_name, product in annual_reports[year].items():
            if product["total_sell_amount"] > 0:
                print(f"    {product_name} has a profit of {product["annual_sell_profit_jpy"]:.0f} JPY")


def main(args):
    csv_path = args[1]
    trade_data = load_trade_history(csv_path)

    min_year = min([t["year"] for t in trade_data])
    max_year = max([t["year"] for t in trade_data])
    all_products = set([t["product"] for t in trade_data if "/" in t["product"]])  # all crypto/JPY pairs

    annual_reports = {}
    for year in range(min_year, max_year + 1):
        make_annual_report(year, [t for t in trade_data if t["year"] == year], annual_reports)

    wallet_status = {p: {y: 0.0 for y in range(min_year, max_year + 1)} for p in all_products}

    simulate_trades(trade_data, wallet_status, annual_reports, min_year, max_year)
    print_annual_reports(annual_reports, min_year, max_year)

if __name__ == "__main__":
    main(sys.argv)
