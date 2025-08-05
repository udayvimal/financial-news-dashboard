from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables. Please set it before running.")

DB_FAISS_PATH = "vectorstore/"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

llm = ChatOpenAI(
    openai_api_key=HF_TOKEN,
    openai_api_base="https://router.huggingface.co/v1",
    model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
    temperature=0.5,
    max_tokens=512,
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=db.as_retriever(search_kwargs={'k': 3}),
    return_source_documents=True,
)

def ask_question(user_question, chat_history):
    response = qa_chain({"question": user_question, "chat_history": chat_history})
    answer = response.get("answer") or response.get("result")
    source_docs = response.get("source_documents", [])
    return answer, source_docs
