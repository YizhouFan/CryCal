# CryCal クリカリ
Cryptocurrency Calculator

## Disclaimer
This repository is an endeavor to implement what is described in the following documents from the [National Tax Agency of Japan](https://www.nta.go.jp/).
https://www.nta.go.jp/publication/pamph/pdf/virtual_currency_faq_03.pdf

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
./format.sh
```
