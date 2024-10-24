import requests
import os
from dotenv import load_dotenv

load_dotenv() #.envファイルから認証情報を読み込み

def main():
    id=os.getenv('CLIENT_ID')
    password=os.getenv('CLIENT_PASSWORD')
    auth_url="https://ip-data.jpo.go.jp/auth/token"

    access_token=get_access_token(auth_url,id,password)
    print(f"Access Token: {access_token}")

def get_access_token(auth_url,id,password):
    headers={ "Content-Type":"application/x-www-form-urlencoded" }
    data={
        "grant_type":"password",
        "username":id,
        "password":password
    }

    response=requests.post(auth_url,headers=headers,data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("認証エラー:",response.status_code,response.text)
        return None

if __name__ == "__main__":
    main()