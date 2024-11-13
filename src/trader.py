from utils import load_trade_history
from tqdm import tqdm

from custom_types import Product


class Trader:
    def __init__(self, trade_history_csv):
        self.trade_data = load_trade_history(trade_history_csv)
        self.num_trade_data = len(self.trade_data)
        self.min_year = min([t["year"] for t in self.trade_data])
        self.max_year = max([t["year"] for t in self.trade_data])
        self.trade_years = range(self.min_year, self.max_year + 1)
        self.all_products = set([t["product"] for t in self.trade_data if "/" in t["product"]])  # all crypto/JPY pairs
        self.annual_reports = {y: {} for y in self.trade_years}
        self.wallet_status = {p: {y: 0.0 for y in self.trade_years} for p in self.all_products}

    def make_annual_reports(self):
        for year in self.trade_years:
            annual_trade_data = [t for t in self.trade_data if t["year"] == year]
            annual_products = set([t["product"] for t in annual_trade_data if "/" in t["product"]])
            product_annual_reports = {}
            for product in annual_products:
                product_trade_data_buy = \
                    [t for t in annual_trade_data if t["product"] == product and t["type"] == "Buy"]
                product_trade_data_sell = \
                    [t for t in annual_trade_data if t["product"] == product and t["type"] == "Sell"]
                product_total_buy_amount = sum([t["amount"] for t in product_trade_data_buy])
                product_total_buy_price_jpy = sum([t["total_price_jpy"] for t in product_trade_data_buy])
                product_total_sell_amount = sum([t["amount"] for t in product_trade_data_sell])
                product_annual_report: Product = {
                    "name": product,
                    "total_buy_amount": product_total_buy_amount,
                    "total_buy_price_jpy": product_total_buy_price_jpy,
                    "total_sell_amount": product_total_sell_amount,
                    "annual_average_price_jpy": product_total_buy_price_jpy / product_total_buy_amount,
                    "eoy_remaining_amount": product_total_buy_amount
                    - product_total_sell_amount,  # this is broken right now
                    "annual_sell_profit_jpy": 0.0,
                }
                product_annual_reports[product] = product_annual_report
            self.annual_reports[year] = product_annual_reports

    def simulate_trades(self):
        # assume transactions are ordered from oldest to latest
        for i in tqdm(range(self.num_trade_data)):
            t = self.trade_data[i]
            if t["type"] == "Buy":
                self.wallet_status[t["product"]][t["year"]] += t["amount"]
            elif t["type"] == "Sell":
                sell_amount_distribution = {y: 0.0 for y in self.trade_years}
                year = t["year"]
                remainder = t["amount"]
                while year >= self.min_year:
                    # check amount of crypto of current year,
                    if self.wallet_status[t["product"]][year] >= remainder:
                        self.wallet_status[t["product"]][year] -= remainder
                        sell_amount_distribution[year] = remainder
                        break
                    else:
                        # if not enough for selling, always use up all amount of current year,
                        # then check one year back, and so on and so forth
                        # this is my interpretation of the laws in Japan
                        self.wallet_status[t["product"]][year] = 0.0
                        remainder = remainder - self.wallet_status[t["product"]][t["year"]]
                        sell_amount_distribution[year] = self.wallet_status[t["product"]][year]
                    year -= 1
                assert remainder > 0, f"Error: Not enough {t["product"]} to sell for {t["id"]}"
                t["sell_amount_distribution"] = sell_amount_distribution
                sell_profit_jpy = sum([t["total_price_jpy"] - 
                                    sell_amount_distribution[y] * 
                                    self.annual_reports[y][t["product"]]["annual_average_price_jpy"] 
                                    for y in sell_amount_distribution if sell_amount_distribution[y] > 0])
                t["sell_profit_jpy"] = sell_profit_jpy
                self.annual_reports[t["year"]][t["product"]]["annual_sell_profit_jpy"] += sell_profit_jpy
            t["post_txn_wallet_status"] = self.wallet_status

    def print_annual_reports(self):
        for year in self.trade_years:
            print(f"{year} ANNUAL PROFIT REPORT")
            print(f"  Total annual profit: "
                  f"{sum([p["annual_sell_profit_jpy"] for p in self.annual_reports[year].values()]):.0f} JPY")
            print("  Details:")
            for product_name, product in self.annual_reports[year].items():
                if product["total_sell_amount"] > 0:
                    print(f"    {product_name} has a profit of {product["annual_sell_profit_jpy"]:.0f} JPY")