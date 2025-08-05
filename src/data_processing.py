import pandas as pd

def load_data(csv_path='data/indian_stock_news_2024_25.csv'):
    """
    Load dataset CSV into a pandas DataFrame with date parsing.
    
    Args:
        csv_path (str): Path to the CSV data file.
        
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    df = pd.read_csv(csv_path, parse_dates=['date'])
    return df

def clean_data(df):
    """
    Perform basic data cleaning:
    - Drop duplicates
    - Remove rows with missing critical fields
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = df.drop_duplicates()
    df = df.dropna(subset=['date', 'headline', 'sector', 'sentiment', 'price_change', 'trading_volume_crore'])
    return df

def feature_engineering(df):
    """
    Add useful engineered features for analysis and visualization:
    - Categorize price change direction (Positive, Negative, Neutral)
    - Normalize sentiment text casing
    - Add price_change_abs for magnitude analysis
    
    Args:
        df (pd.DataFrame): DataFrame to enrich.
        
    Returns:
        pd.DataFrame: Enriched DataFrame.
    """
    df['price_movement'] = df['price_change'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
    df['sentiment'] = df['sentiment'].str.capitalize()
    df['price_change_abs'] = df['price_change'].abs()
    
    # Example: You can add new columns here, e.g. weekly/monthly aggregates, event flags, etc.
    
    return df

def aggregate_trends(df, freq='W'):
    """
    Aggregate sentiment and emotion trends by sector over time.
    
    Args:
        df (pd.DataFrame): Processed DataFrame.
        freq (str): Frequency string for resampling (e.g., 'D' daily, 'W' weekly, 'M' monthly).
    
    Returns:
        pd.DataFrame: Aggregated trend DataFrame with multi-index (date, sector).
    """
    df_agg = df.set_index('date').groupby(['sector', pd.Grouper(freq=freq)]).agg(
        sentiment_positive_pct=('sentiment', lambda x: (x == 'Positive').mean()),
        sentiment_negative_pct=('sentiment', lambda x: (x == 'Negative').mean()),
        avg_price_change=('price_change', 'mean'),
        avg_trading_volume=('trading_volume_crore', 'mean')
    ).reset_index()
    return df_agg

def preprocess(csv_path='data/indian_stock_news_2024_25.csv'):
    """
    Full preprocessing pipeline: load, clean, engineer features.
    
    Args:
        csv_path (str): Path to data CSV.
    
    Returns:
        pd.DataFrame: Final processed DataFrame.
    """
    df = load_data(csv_path)
    df = clean_data(df)
    df = feature_engineering(df)
    return df

if __name__ == "__main__":
    df_processed = preprocess()
    print("Sample processed data:")
    print(df_processed.head())

    # Example aggregation
    df_trends = aggregate_trends(df_processed)
    print("\nSample aggregated sentiment trends by sector (weekly):")
    print(df_trends.head())
