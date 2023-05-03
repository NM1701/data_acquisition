# 株価取得プログラム
### 銘柄ごとに株価の推移を日足で取得し、その後時系列分析により有望銘柄の抽出を行う

- 取得の流れ
    1. 銘柄リストを取得しcsv出力
    2. 各銘柄の指定期間の株価を日足で取得しcsv出力

- 取得対象
    - 日本株
    - 米国株

- 使い方
    - stock_codes_acquisition.py: 銘柄一覧と各銘柄の株価を取得するプログラム
      ターミナルにて以下コマンドで実行
      sh
      ```
      python stock_codes_acquisition.py
      ```

### 参考
- [【Pythonコード解説】yahoo_finance_api2で日本株の株価データを取得する](https://myfrankblog.com/stock_price_with_yahoo_finance_api2/)
- [【日本株対応】Pythonで株価のローソク足データを取得する方法まとめ【CSV、ライブラリ、スクレイピング】](https://myfrankblog.com/how_to_get_stock_price_with_python/#i-5)
- [Python初心者が株価確認を自動化してみた【コピペでOK】](https://tetsulog2020.com/python-automation/)
- [【Python】米国株の株価データを取得する](https://non-dimension.com/get-usstock-data/#toc4)
- [Pythonで株の銘柄コード一覧を取得する方法](https://book-read-yoshi.hatenablog.com/entry/get_stock_codelist)

### notes
- pandas_datareaderのDataReader()関数で株価情報を取得できなくなっているため、yfinance経由で取得。[pandas_datareaderで、データが取得できなくなりました](https://teratail.com/questions/9q8zc5eccp9796)
