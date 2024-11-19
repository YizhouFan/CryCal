# CryCal - Supports the latest bitFlyer version!
# クリカリ - 最新版ビットフライヤーを対応！
Cryptocurrency Calculator 暗号資産のための電卓

![ci badge](https://github.com/YizhouFan/CryCal/actions/workflows/ci.yml/badge.svg)

## Disclaimer 免責事項
This repository is not intended to offer legal, financial, or tax advice. By using this software, you acknowledge that the calculations are based on the inputs provided and may not reflect the most current laws or regulations. The creators of this repository make no representations or warranties regarding the accuracy, completeness, or reliability of the results generated. Users are encouraged to consult with a qualified tax professional or legal advisor to ensure compliance with all applicable laws and regulations. The creators are not liable for any errors, omissions, or consequences arising from the use of this software. Use at your own risk.

このリポジトリは、法的、財務的、または税務的なアドバイスを提供することを目的としていません。このソフトウェアを使用することにより、提供された入力に基づいて計算が行われ、最新の法律や規制を反映していない可能性があることを認識するものとします。このリポジトリの作成者は、生成された結果の正確性、完全性、または信頼性について、いかなる表明や保証も行いません。ユーザーは、適用されるすべての法律および規制を遵守するために、資格を持つ税務専門家または法的アドバイザーに相談することを推奨します。作成者は、このソフトウェアの使用に起因するいかなるエラー、脱漏、または結果についても責任を負いません。使用は自己責任で行ってください。

This repository is an endeavor to implement what is described in the following documents from the [National Tax Agency of Japan](https://www.nta.go.jp/).

このリポジトリは、[日本国税庁](https://www.nta.go.jp/)の以下の文書に記載されている内容を実装する試みです。

- https://www.nta.go.jp/publication/pamph/pdf/virtual_currency_faq_03.pdf

## Installation インストール
1. Install [uv](https://github.com/astral-sh/uv), the package and project manager

    パッケージおよびプロジェクトマネージャーの[uv](https://github.com/astral-sh/uv)をインストールします。
2. Set up the repo by `uv`

    `uv`を使ってリポジトリをセットアップします。
```
uv sync
```
3. Verify that the Python version is pinned to `3.12`.

    Pythonのバージョンが3.12に固定されていることを確認します。
```
uv run python --version
```

## Usage 使用方法
Download the full trade history from `bitFlyer` from [this link](https://bitflyer.com/en-jp/ex/TradeReportDownload). `Generate`, and then `Download` the `All Trades` under `Trade Reports (csv)`. A zip file containing a file named `TradeHistory.csv` will be downloaded.

[こちらのリンク](https://bitflyer.com/en-jp/ex/TradeReportDownload)からビットフライヤーの全取引履歴をダウンロードします。「取引履歴 (csv)」の下にある「すべてのお取引」を「申請」そして「ダウンロード」します。`TradeHistory.csv`という名前のファイルが含まれたZIPファイルがダウンロードされます。

Create a folder named `data` under the repository path, and put `TradeHistory.csv` inside the `data` folder. Then do the following to run the calculator. 

リポジトリのパスに`data`という名前のフォルダを作成し、その中に`TradeHistory.csv`を入れます。その後、以下のコマンドを実行して計算機能を実行します。
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
