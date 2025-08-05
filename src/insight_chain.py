from src.custom_mistral_llm import ask_question

def generate_insight(user_question, filtered_df, chat_history):
    """
    Takes the constructed prompt from llm_helpers and queries the LLM pipeline.
    """
    answer, sources = ask_question(user_question, chat_history)
    return answer, sources
