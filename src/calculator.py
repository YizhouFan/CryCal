import sys
from trader import Trader


def main(args):
    csv_path = args[1]
    trader = Trader(csv_path)
    trader.make_annual_reports()
    trader.print_annual_reports()


if __name__ == "__main__":
    main(sys.argv)
