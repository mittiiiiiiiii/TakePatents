from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
import psycopg2
from dotenv import load_dotenv

def fetch_patent_data(): #データベースからデータを取得
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT registration_number, invention_title, right_person_name FROM patents_info")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    print(data)

    return data

def create_vector_store():
    load_dotenv()
    data = fetch_patent_data()
    documents=[f"{row[1]} by {row[2]}" for row in data]
    embeddings=OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore=FAISS.from_texts(documents,embeddings)
    vectorstore.save_local("patents_vectorstore")


create_vector_store()