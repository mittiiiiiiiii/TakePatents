import requests
import os
import psycopg2
from dotenv import load_dotenv

def main():
    load_dotenv() #.envファイルから認証情報を読み込み

    #環境変数からクライアントIDとパスワードを取得
    id=os.getenv('CLIENT_ID')
    password=os.getenv('CLIENT_PASSWORD')

    #認証URLとターゲットURLを設定
    auth_url='https://ip-data.jpo.go.jp/auth/token'
    target_url='https://ip-data.jpo.go.jp/api/patent/v1'

    #エンドポイントと出願番号を設定
    endpoint='registration_info'
    application_number='2020034567'

    try:
        access_token=get_access_token(auth_url,id,password) #アクセストークンを取得

        if access_token:
            print("Access tokenの取得に成功")

            patent_info=get_api_response(access_token,f"{target_url}/{endpoint}",application_number) #APIから特許情報を取得
            print(patent_info)

            # SONから必要な情報を抽出
            registration_number = patent_info['result']['data']['registrationNumber']
            right_person_name = patent_info['result']['data']['rightPersonInformation'][0]['rightPersonName']
            invention_title = patent_info['result']['data']['inventionTitle']

            #データベースに保存
            insert_data(registration_number, right_person_name, invention_title)
            print("データベースに保存しました")

        else:
            raise Exception("Access token could not be retrieved")

    except Exception as e:
        print(f"Error:{e}")

def get_access_token(auth_url,id,password):
    #リクエストヘッダーとデータを設定
    headers={ "Content-Type":"application/x-www-form-urlencoded" }
    data={
        "grant_type":"password",
        "username":id,
        "password":password
    }

    response=requests.post(auth_url,headers=headers,data=data)  #認証リクエストを送信

    if response.status_code==200:   #取得成功
        return response.json()["access_token"]  #アクセストークンを返す
    else:   #取得失敗
        print("認証エラー:",response.status_code,response.text) #エラーメッセージ
        return None

def get_api_response(access_token,api_url,app_number):
    headers={"Authorization":f"Bearer {access_token}"}  #リクエストヘッダーを設定

    response=requests.get(f"{api_url}/{app_number}",headers=headers)    #APIリクエストを送信

    if response.status_code==200:   #取得成功
        return response.json()  #APIレスポンスを返す
    else:   #取得失敗
        print("進捗情報取得エラー:", response.status_code, response.text)   #エラーメッセージ
        return None

def insert_data(registration_number, right_person_name, invention_title):
    try:
        #PostgreSQLに接続
        conn = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password=os.getenv('POSTGRES_PASSWORD'),
            host="localhost",
            port="5432"  #ポートフォワーディングで使用したポート
        )
        cursor = conn.cursor()

        #データを挿入
        cursor.execute('''
            INSERT INTO patents_info (registration_number, right_person_name, invention_title)
            VALUES (%s, %s, %s)
        ''', (registration_number, right_person_name, invention_title))

        #変更をコミット
        conn.commit()

        #接続を閉じる
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"データベースエラー: {e}")

if __name__=="__main__":
    main()