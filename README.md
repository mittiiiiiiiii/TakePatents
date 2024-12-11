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
    POSTGRES_SUPERUSER_PASSWORD=スーパーユーザーのパスワード
    POSTGRES_REPLICATION_PASSWORD=レプリケーションユーザーのパスワード
    ```

3. データベースの作成
    1. Kubernetsの起動
        - 動作を確認するだけなのでminikubeを使用
        - 将来的には別の方法でKubernetes環境の構築を行いたい
        ```bash
        minikube start
        ````
    2. PostgreSQLの管理者ユーザの認証情報の設定と適用
        - シークレットを作成
        ```bash
        python generate_secret.py  #シークレットの作成を自動で行う
        ```
        - 設定を適応
        ```bash
        kubectl apply -f k8s/my-postgres-secret.yaml
        ```
    3. PostgreSQLのサーバ構成の設定と適用
        - 生成するテーブルの設定
        ```bash
        kubectl apply -f k8s/postgres-configmap.yaml
        ```
        - podを立ち上げる
        ```bash
        kubectl apply -f k8s/postgres-deployment.yaml
        ```
        - アクセスできるようにする
        ```bash
        kubectl apply -f k8s/postgres-service.yaml
        ```
    4. ポートフォワーディングを設定
        - ローカルからクラスターにアクセスをできるようにする
        ```bash
        kubectl port-forward svc/postgres-service 5432:5432
        ```
        - 別のターミナルを開く -> 4.アプリの起動へ
        - `Forwarding from [::1]:5432 -> 5432`が出力されたら成功

4. アプリの起動
    ```bash
    python App.py
    ```

    - 保存されているか確認
        - データベースに接続
        ```bash
        psql -h localhost -U postgres -d mydatabase
        ```
        - 接続できたらデータが保存されているか確認
        ```bash
        SELECT * FROM patents_info;
        ```
        - テーブルに取得したデータが保存されていれば成功

5. Ragの構築
    - データベースからベクトルを取得、保存
        ```bash
        python Get_Data.py
        ```