import requests
import os
from dotenv import load_dotenv

load_dotenv() #.envファイルから認証情報を読み込み

def main():
    #環境変数からクライアントIDとパスワードを取得
    id=os.getenv('CLIENT_ID')
    password=os.getenv('CLIENT_PASSWORD')

    #認証URLとターゲットURLを設定
    auth_url='https://ip-data.jpo.go.jp/auth/token'
    target_url='https://ip-data.jpo.go.jp/api/patent/v1'

    #エンドポイントと出願番号を設定
    endpoint='app_progress'
    application_number='2020008423'

    try:
        access_token=get_access_token(auth_url,id,password) #アクセストークンを取得

        if access_token:
            print("Access tokenの取得に成功")

            paten_info=get_api_response(access_token,f"{target_url}/{endpoint}",application_number) #APIから特許情報を取得
            print(paten_info)
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

if __name__=="__main__":
    main()