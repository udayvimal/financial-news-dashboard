import pandas as pd
from src.insight_chain import generate_insight as _generate_insight

def load_data(path="data/indian_stock_news_2024_25.csv"):
    """
    Load and return the financial news dataset as a DataFrame.
    """
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

def generate_insight(user_question, filtered_df, chat_history):
    context = filtered_df[['date','headline','summary','sector','sentiment']].head(8).to_string(index=False)

    system_instruction = (
        "You are a senior financial analyst and strategic advisor for businesses and investors in the Indian market. "
        "Given the filtered financial news data and the user's question, provide a detailed and structured business insight. "
        "Your output should include: \n"
        "- Identification of sectors or companies gaining an edge and those showing weaknesses or risks. \n"
        "- A summary of key problems impacting the market or specific sectors, backed by data. \n"
        "- Practical and actionable recommendations or solutions for investors or business leaders. \n"
        "- Highlight the best and worst trends or entities with explanations. \n"
        "- Use bullet points, numbered lists, and clear sections for readability.\n"
        "- Avoid generic or vague statements and ensure insights are data-driven and tailored to the context. \n"
        "Format the response using markdown."
    )

    prompt = f"{system_instruction}\n\nDATA:\n{context}\n\nQUESTION: {user_question}\nINSIGHT REPORT:"

    answer, sources = _generate_insight(prompt, filtered_df, chat_history)
    return answer, sources

