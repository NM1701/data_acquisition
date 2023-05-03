# Trip Adviser口コミのスクレイピング

# import
import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from datetime import date
from time import sleep


def scrape_from_trip_adviser(url_first_half: str = None,
                             url_second_half: str = None,
                             conj: str = "-or",
                             start: int = 0,
                             end: int = 100,
                             every: int = 3,
                             output_dir: str = None,
                            ) -> pd.DataFrame:
    """Trip_Adviserから口コミをスクレイピングする関数"""

    # スクレイピングした口コミをdf_listに格納していく
    df_list = []
    # 指定ページ分スクレイピング行う。
    pages = range(start, end, every)

    for page in pages:
        #　1ページ目と2ページ目以降で若干URLが異なるので条件分岐
        if page == 0:
            urlName = url_first_half + url_second_half
            print("------------------------------------------------------")
            print(f"page_now: {page+1}")
            try:
                url = requests.get(urlName, timeout=(7.5, 10.0))
            except Timeout:
                print(f"timeout occurred when url is {urlName}.")
                print(f"We will keep trying to request alternative url.")
                try:
                    urlName = url_first_half + url_second_half[:-10] + "Ka.html"
                    url = requests.get(urlName, timeout=(7.5, 10.0))
                except Timeout:
                    print(f"timeout occurred when url is {urlName}.")
                    print(f"We will keep trying to request alternative url.")
                    try:
                        urlName = url_first_half + url_second_half[:-10] + "Kan.html"
                        url = requests.get(urlName, timeout=(7.5, 10.0))
                    except Timeout:
                        print(f"timeout occurred when url is {urlName}.")
                        print(f"We will move on to the next loop.")
                        continue

        else:
            urlName = url_first_half + conj + str(page*10) + url_second_half
            print("------------------------------------------------------")
            print(f"page_now: {page+1}")
            try:
                url = requests.get(urlName, timeout=(7.5, 10.0))
            except Timeout:
                print(f"timeout occurred when url is {urlName}.")
                print(f"We will keep trying to request alternative url.")
                try:
                    urlName = url_first_half + conj + str(page*10) + url_second_half[:-10] + "Ka.html"
                    url = requests.get(urlName, timeout=(7.5, 10.0))
                except Timeout:
                    print(f"timeout occurred when url is {urlName}.")
                    print(f"We will keep trying to request alternative url.")
                    try:
                        urlName = url_first_half + conj + str(page*10) + url_second_half[:-10] + "Kan.html"
                        url = requests.get(urlName, timeout=(7.5, 10.0))
                    except Timeout:
                        print(f"timeout occurred when url is {urlName}.")
                        print(f"We will move on to the next loop.")
                        continue

        print(f"{urlName} found!")
        soup = BeautifulSoup(url.content, "html.parser")

        # HTMLの中から口コミに相当するタグとClassを指定
        review = soup.find_all('span', class_ = 'yCeTE')

        # 抜き出した口コミを順番に格納
        for i in range(len(review)):
            _df = pd.DataFrame({'Number':i+1,
                                'review':[review[i].text]})

            df_list.append(_df)

        # 間隔を空ける
        sleep(1.1)

    df_review = pd.concat(df_list).reset_index(drop=True)
    print(f"df_review.shape: {df_review.shape}")

    # 出力
    today=date.today()
    os.makedirs(output_dir, exist_ok=True)
    df_review.to_csv(output_dir+str(today)+"scraping_from_trip_adviser.csv", index = False, encoding="utf-8")
    return df_review

# 今回は"東京駅"の口コミを取得
# 任意のワードで検索する関数は別に用意（未定義）

url_first_half = "https://www.tripadvisor.jp/Attraction_Review-g14129528-d550327-Reviews"
url_second_half = "-Tokyo_Central_Railway_Station-Marunouchi_Chiyoda_Tokyo_Tokyo_Prefecture_Kanto.html"
start = 0
end = 500
every = 10
output_dir = "../output/"

df_review = scrape_from_trip_adviser(url_first_half=url_first_half,
                                     url_second_half=url_second_half,
                                     start=start,
                                     end=end,
                                     every=every,
                                     output_dir=output_dir,)
df_review
