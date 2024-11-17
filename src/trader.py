from tabulate import tabulate

from custom_types import Product
from utils import load_trade_history


class Trader:
    def __init__(self, trade_history_csv):
        self.trade_data = load_trade_history(trade_history_csv)
        self.num_trade_data = len(self.trade_data)
        self.min_year = min([t["year"] for t in self.trade_data])
        self.max_year = max([t["year"] for t in self.trade_data])
        self.trade_years = range(self.min_year, self.max_year + 1)
        self.all_products = set([t["product"] for t in self.trade_data if "/" in t["product"]])  # all crypto/JPY pairs
        self.annual_reports = {y: {} for y in self.trade_years}

    def get_boy_values(self, product_name, year):
        while year > self.min_year:
            if product_name in self.annual_reports[year - 1]:
                return self.annual_reports[year - 1][product_name]["eoy_amount"], self.annual_reports[year - 1][
                    product_name
                ]["eoy_evaluation_jpy"]
            year -= 1
        return 0.0, 0.0

    def make_annual_reports(self):
        for year in self.trade_years:
            annual_trade_data = [t for t in self.trade_data if t["year"] == year]
            annual_products = set([t["product"] for t in annual_trade_data if "/" in t["product"]])
            product_annual_reports = {}
            for product in annual_products:
                trade_data_buy = [t for t in annual_trade_data if t["product"] == product and t["type"] == "Buy"]
                trade_data_sell = [t for t in annual_trade_data if t["product"] == product and t["type"] == "Sell"]
                total_buy_amount = sum([t["amount"] for t in trade_data_buy])
                total_buy_price_jpy = sum([t["total_price_jpy"] for t in trade_data_buy])
                average_buy_price_jpy = total_buy_price_jpy / total_buy_amount if total_buy_amount else 0.0
                total_sell_amount = sum([t["amount"] for t in trade_data_sell])
                total_sell_price_jpy = sum([t["total_price_jpy"] for t in trade_data_sell])
                average_sell_price_jpy = total_sell_price_jpy / total_sell_amount if total_sell_amount else 0.0
                boy_amount, boy_evaluation_jpy = self.get_boy_values(product, year)
                eoy_amount = boy_amount + total_buy_amount - total_sell_amount
                eoy_average_price_jpy = (boy_evaluation_jpy + total_buy_price_jpy) / (boy_amount + total_buy_amount)
                eoy_evaluation_jpy = eoy_average_price_jpy * eoy_amount
                total_cost_jpy = eoy_average_price_jpy * total_sell_amount
                total_profit_jpy = total_sell_price_jpy - total_cost_jpy if total_sell_amount else 0.0
                annual_report: Product = {
                    "name": product,
                    "total_buy_amount": total_buy_amount,
                    "total_buy_price_jpy": total_buy_price_jpy,
                    "average_buy_price_jpy": average_buy_price_jpy,
                    "total_sell_amount": total_sell_amount,
                    "total_sell_price_jpy": total_sell_price_jpy,
                    "average_sell_price_jpy": average_sell_price_jpy,
                    "boy_amount": boy_amount,
                    "boy_evaluation_jpy": boy_evaluation_jpy,
                    "eoy_amount": eoy_amount,
                    "eoy_evaluation_jpy": eoy_evaluation_jpy,
                    "eoy_average_price_jpy": eoy_average_price_jpy,
                    "total_cost_jpy": total_cost_jpy,
                    "total_profit_jpy": total_profit_jpy,
                }
                product_annual_reports[product] = annual_report
            self.annual_reports[year] = product_annual_reports

    def print_annual_reports(self):
        for year in self.trade_years:
            print(f"{year} ANNUAL PROFIT REPORT")
            print(
                f"Total annual profit: "
                f"{sum([p["total_profit_jpy"] for p in self.annual_reports[year].values()]):.0f} JPY"
            )
            print("Details per cryptocurrency/JPY pair:")
            report_tabulate = {}
            for _, product in self.annual_reports[year].items():
                for key, value in product.items():
                    report_tabulate[key] = report_tabulate.get(key, []) + [value]
            print(tabulate(report_tabulate, headers="keys"))
            print("\n")
