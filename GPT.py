from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

# ベクトルデータをロードして検索用のリトリーバを設定
def load_vector_store():
    vectorstore = FAISS.load_local("patents_vectorstore", OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")))
    return vectorstore.as_retriever()

# RAGアプリケーションのメイン関数
def create_rag_app():
    load_dotenv()

    # OpenAIモデルを設定
    llm = OpenAI(
        model="gpt-4",  # 適切なモデル名を選択
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # ベクトル検索リトリーバを読み込み
    retriever = load_vector_store()

    # Retrieval-Augmented Generation (RAG) チェーンを作成
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True  # 必要に応じてソースを返す
    )

    return qa_chain

# ユーザー入力に基づくQA処理
if __name__ == "__main__":
    rag_app = create_rag_app()

    print("RAGアプリケーションが起動しました。質問を入力してください。")
    while True:
        query = input("\n質問 (終了するには 'exit' と入力): ")
        if query.lower() == "exit":
            print("終了します。")
            break

        # 質問をRAGに投げる
        response = rag_app.run(query)
        print("\n=== 回答 ===")
        print(response["result"])

        # ソースを表示 (必要に応じて)
        print("\n=== 参照ソース ===")
        for doc in response["source_documents"]:
            print(doc.page_content)
