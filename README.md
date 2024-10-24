# 特許庁APIを使用して特許調査できるアプリ

## 目的

- 出願番号から特許情報を取得
- エンドポイントを変更して取得する情報を変更できる
- アクセストークンを実行時に取得、取得したトークンからAPIにアクセス

## 起動方法

1. 特許庁APIのAPIキーを取得

- 一般にAPIを使うためにはAPIキーが必要になります。特許庁でもAPIサービスを利用するための申し込みが必要です。
- [特許庁API申し込み](https://www.jpo.go.jp/system/laws/sesaku/data/api-provision.html)

2. `.env`ファイルを作成し、IDとパスワードを環境変数として使えるようにする

    .envファイルを作成し、以下を追加。

    ```.env
    CLIENT_ID=取得したID
    CLIENT_PASSWORD=取得したパスワード
    ```

3. アプリの起動
    % python App.py