import unittest
from pathlib import Path

from trader import Trader

TEST_DATA_PATH = Path("tests/test_data")


class TestTrader(unittest.TestCase):
    def test_official_test_case(self):
        """
        This test cases is provided in chapter 2-4 of the following document
        https://www.nta.go.jp/publication/pamph/pdf/virtual_currency_faq_03.pdf
        """
        trader = Trader(TEST_DATA_PATH / "official.csv")
        trader.make_annual_reports()
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["total_buy_amount"], 6.15)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["total_buy_price_jpy"], 4_037_800)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["average_buy_price_jpy"], 621_200)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["total_sell_amount"], 5.0)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["total_sell_price_jpy"], 5_295_000)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["average_sell_price_jpy"], 1_059_000)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["boy_amount"], 0.0)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["boy_evaluation_jpy"], 0.0)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["eoy_amount"], 1.5)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["eoy_evaluation_jpy"], 931_800)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["eoy_average_price_jpy"], 621_200)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["total_cost_jpy"], 3_106_000)
        self.assertEqual(trader.annual_reports[2020]["BTC/JPY"]["total_profit_jpy"], 2_189_000)

    def test_init(self):
        trader = Trader(TEST_DATA_PATH / "simple.csv")
        self.assertEqual(trader.num_trade_data, 4)
        self.assertEqual(trader.min_year, 2019)
        self.assertEqual(trader.max_year, 2024)
        self.assertEqual(trader.trade_years, range(2019, 2025))
        self.assertEqual(trader.annual_reports, {2019: {}, 2020: {}, 2021: {}, 2022: {}, 2023: {}, 2024: {}})
        trader.make_annual_reports()
        self.assertAlmostEqual(trader.annual_reports[2024]["BTC/JPY"]["total_profit_jpy"], 799_963)
        self.assertAlmostEqual(trader.annual_reports[2024]["BTC/JPY"]["total_cost_jpy"], 2_539_272)
        self.assertAlmostEqual(trader.annual_reports[2024]["BTC/JPY"]["eoy_amount"], 0.0)
        self.assertAlmostEqual(trader.annual_reports[2024]["BTC/JPY"]["eoy_evaluation_jpy"], 0)
