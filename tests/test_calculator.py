import unittest
from pathlib import Path

import calculator

TEST_DATA_PATH = Path("tests/test_data")


class TestCalculator(unittest.TestCase):
    def test_calculator(self):
        calculator.main([None, TEST_DATA_PATH / "official.csv"])
