# CryCal クリカリ
Cryptocurrency Calculator

![ci badge](https://github.com/YizhouFan/CryCal/actions/workflows/ci.yml/badge.svg)

## Disclaimer
This repository is not intended to offer legal, financial, or tax advice. By using this software, you acknowledge that the calculations are based on the inputs provided and may not reflect the most current laws or regulations. The creators of this repository make no representations or warranties regarding the accuracy, completeness, or reliability of the results generated. Users are encouraged to consult with a qualified tax professional or legal advisor to ensure compliance with all applicable laws and regulations. The creators are not liable for any errors, omissions, or consequences arising from the use of this software. Use at your own risk.

This repository is an endeavor to implement what is described in the following documents from the [National Tax Agency of Japan](https://www.nta.go.jp/).

- https://www.nta.go.jp/publication/pamph/pdf/virtual_currency_faq_03.pdf

## Installation
1. Install [uv](https://github.com/astral-sh/uv), the package and project manager
2. Set up the repo by `uv`
```
uv sync
```
3. Verify that the Python version is pinned to `3.12`.
```
uv run python --version
```

## Usage
```
uv run src/calculator.py data/TradeHistory.csv
```

## Contributing
To format
```
./format.sh fix
```
To run unit tests
```
uv run pytest
```
