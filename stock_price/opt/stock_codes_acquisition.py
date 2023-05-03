## 株の銘柄コード一覧の取得
# - 取得先
#     - 日本株：[JPX](https://www.jpx.co.jp/markets/statistics-equities/misc/01.html)
#     - 米国株：nasdaq

# import
import requests
import pandas as pd
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from __future__ import annotations
from tqdm import tqdm

# get a list of Japanese stock codes
def stock_list_acquisition_jp(url: str,
                              section_list: list[str],
                              output_dir: str,
                              raw_name: str,
                              renamed: str) -> pd.DataFrame:
    url = url
    req = requests.get(url)
    with open(output_dir+raw_name, 'wb') as output:
        output.write(req.content)

    # read excel
    os.rename(output_dir+raw_name, output_dir+renamed)
    stocklist_jp_df = pd.read_excel(output_dir+renamed)

    # extract specific sections
    stocklist_jp_df = stocklist_jp_df.loc[stocklist_jp_df["市場・商品区分"].isin(section_list)]
    stocklist_jp_df = stocklist_jp_df.reset_index(drop=True)

    # rename columns
    stocklist_jp_df.rename(columns={"日付":"updated_on", "コード":"code", "銘柄名":"name", "市場・商品区分":"market_segment",
                                    "33業種コード":"33_industry_code", "33業種区分":"33_industry_segment", "17業種コード":"17_industry_code",
                                    "17業種区分":"17_industry_segment", "規模コード":"scale_code", "規模区分":"scale_segment"},
                           inplace=True)

    stocklist_jp_df.to_csv(output_dir+renamed[:-4]+".csv", index = False, encoding = "utf-8_sig")

    return stocklist_jp_df


def acquire_stock_price_jp(df: pd.DataFrame,
                           n_year: int,
                           end_date: datetime,
                           output_dir: str,
                           stock_price_filename: str,
                           error_symbols_filename: str) -> pd.DataFrame:

    start_date = end_date - relativedelta(years = n_year)
    print(f"acquisition_range: {start_date} - {end_date}")

    stock_data_df_list = []
    error_symbols = []
    for code, name in zip(df.code, df.name):
        try:
            code_str = str(code) + ".T"
            stock_data_df = pdr.DataReader(code_str, start=start_date, end=end_date).reset_index(drop=False)
            stock_data_df["name"] = name
            stock_data_df_list.append(stock_data_df)
        except:
            print(f"{name} could not be acquired.")
            error_symbols.append(name)

    # dataをDataFrameに変換
    stock_price_df = pd.concat(stock_data_df_list, axis = 0, sort = False, ignore_index = True)
    # error_symbolsをDataFrameに変換
    error_symbols_df = pd.DataFrame({'error_symbols': error_symbols})

    # 出力
    stock_price_df.to_csv(output_dir+stock_price_filename, index = False, encoding = "utf-8_sig")
    error_symbols_df.to_csv(output_dir+error_symbols_filename, index = False, encoding = "utf-8_sig")

    return stock_price_df, error_symbols_df


### 米国株
# get a list of US stock codes
def stock_list_acquisition_us(output_dir: str,
                              filename: str) -> pd.DataFrame:

    # get a list of US stock codes
    stocklist_us_df = get_nasdaq_symbols()

    # extract specific sections
    stocklist_us_df = stocklist_us_df[stocklist_us_df["ETF"]==False]
    stocklist_us_df = stocklist_us_df.reset_index(drop=True)

    # output as csv
    stocklist_us_df.to_csv(output_dir+filename, encoding="utf-8_sig", index=False)

    return stocklist_us_df


def acquire_stock_price_us(df: pd.DataFrame,
                           n_year: int,
                           end_date: datetime,
                           output_dir: str,
                           stock_price_filename: str,
                           error_symbols_filename: str) -> pd.DataFrame:

    start_date = end_date - relativedelta(years = n_year)
    print(f"acquisition_range: {start_date} - {end_date}")

    stock_data_df_list = []
    error_symbols = []
    for symbol, name in zip(df["NASDAQ Symbol"], df["Security Name"]):
        try:
            stock_data_df = pdr.DataReader(str(symbol), start=start_date, end=end_date).reset_index(drop=False)
            stock_data_df["name"] = name
            stock_data_df_list.append(stock_data_df)
        except:
            print(f"{symbol} could not be acquired.")
            error_symbols.append(name)

    # dataをDataFrameに変換
    stock_price_df = pd.concat(stock_data_df_list, axis = 0, sort = False, ignore_index = True)
    # error_symbolsをDataFrameに変換
    error_symbols_df = pd.DataFrame({'error_symbols': error_symbols})

    # 出力
    stock_price_df.to_csv(output_dir+stock_price_filename, index = False, encoding = "utf-8_sig")
    error_symbols_df.to_csv(output_dir+error_symbols_filename, index = False, encoding = "utf-8_sig")

    return stock_price_df, error_symbols_df


# 日本株
os.makedirs("./output/", exist_ok = True)
url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
section_list = ["プライム（内国株式）", "スタンダード（内国株式）", "グロース（内国株式）"]
output_dir = "./output/"
raw_name = "data_j.xls"
renamed = "japanese_stock_codes_list.xls"
stocklist_jp_df = stock_list_acquisition_jp(url=url,
                                            section_list=section_list,
                                            output_dir=output_dir,
                                            raw_name=raw_name,
                                            renamed=renamed)
print(f"stocklist_jp_df: {stocklist_jp_df}")

# 取得期間
n_year = 10 # 取得年数
end_date = date.today()
stock_price_jp_df, error_symbols_jp_df = acquire_stock_price_jp(df=stocklist_jp_df,
                                                    n_year=n_year,
                                                    end_date=end_date,
                                                    output_dir=output_dir,
                                                    stock_price_filename="stock_price_jpx.csv",
                                                    error_symbols_filename="error_symbols_jpx.csv")
print(f"stock_price_jp_df: {stock_price_jp_df}")
print(f"error_symbols_jp_df: {error_symbols_jp_df}")


# 米国株
output_dir = "./output/"
filename="stocklist_us.csv"
stocklist_us_df = stock_list_acquisition_us(output_dir=output_dir,
                                            filename=filename)
print(f"stocklist_us_df: {stocklist_us_df}")

# 取得期間
n_year = 10 # 取得年数
end_date = date.today()
stock_price_us_df, error_symbols_us_df = acquire_stock_price_us(df=stocklist_us_df,
                                                    n_year=n_year,
                                                    end_date=end_date,
                                                    output_dir=output_dir,
                                                    stock_price_filename="stock_price_us.csv",
                                                    error_symbols_filename="error_symbols_us.csv")
print(f"stock_price_us_df: {stock_price_us_df}")
print(f"error_symbols_us_df: {error_symbols_us_df}")
