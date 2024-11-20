import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from django.conf import settings

# OpenAI API 키 설정
openai.api_key = settings.OPENAI_API_KEY


def get_langchain_response(user_input):
    # OpenAI Embeddings 초기화
    embeddings = OpenAIEmbeddings()

    # 기존 벡터 스토어 로드 또는 새로운 벡터 스토어 생성
    vector_store = FAISS.load_local("vector_store_path", embeddings)

    # ConversationalRetrievalChain을 사용하여 응답 생성
    chain = ConversationalRetrievalChain(retriever=vector_store.as_retriever())
    response = chain.run(user_input)

    return response
