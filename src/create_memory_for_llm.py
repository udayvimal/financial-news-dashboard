import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.docstore.document import Document

def row_to_doc(row):
    content = (
        f"Date: {row['date']}\n"
        f"Headline: {row['headline']}\n"
        f"Summary: {row['summary']}\n"
        f"Sector: {row['sector']}\n"
        f"Sentiment: {row['sentiment']}\n"
        f"Emotion: {row['emotion']}\n"
        f"Price Change: {row['price_change']}%\n"
        f"Trading Volume: ₹{row['trading_volume_crore']} Cr"
    )
    return Document(page_content=content)

def get_vectorstore(csv_path="C:\\Users\\AYUSH\\financial-news-dashboard\\data\\indian_stock_news_2024_25.csv"):
    print(f"📄 Loading data from {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} rows")

    docs = [row_to_doc(row) for _, row in df.iterrows()]
    print(f"🧾 Converted to {len(docs)} LangChain documents")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("🔗 Embeddings model loaded")

    vectorstore = FAISS.from_documents(docs, embedding=embeddings)
    print("🧠 FAISS vector store built")

    return vectorstore

if __name__ == "__main__":
    vectorstore = get_vectorstore()
    vectorstore.save_local("vectorstore")  # ✅ This saves the index to disk
    print("✅ FAISS Vector Store saved to 'vectorstore/' directory.")
