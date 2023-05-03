# Twitterスクレイピング（＋感情分析）

- twitter-APIを用いたスクレイピング

- 事前にtwitter-APIのアカウント登録を行い、以下の情報を取得
    - API Key
    - API Key Secret
    - Bearer Token
    - Client ID
    - Client Secret

<br>
- 今回は以下4項目を取得
    - tweet_id
    - text
    - created_at
    - author_id

<br>
- 取得データに対して感情分析（ネガポジ判定）を実施し、上記取得データのデータフレームにネガポジ判定結果と判定スコアを格納。
