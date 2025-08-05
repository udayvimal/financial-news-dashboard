import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

companies_expanded = {
    'Technology': ['Infosys', 'TCS', 'Wipro', 'HCL Technologies', 'Tech Mahindra', 'L&T Infotech', 'Mindtree', 'Mphasis', 'Persistent Systems', 'Coforge'],
    'Pharma': ['Sun Pharma', "Dr. Reddy's", 'Cipla', "Divi's Labs", 'Lupin', 'Biocon', 'Cadila Healthcare', 'Glenmark', 'Torrent Pharma', 'Alkem Labs'],
    'Banking': ['HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank', 'Kotak Mahindra', 'Punjab National Bank', 'Bank of Baroda', 'Canara Bank', 'IndusInd Bank', 'Federal Bank'],
    'Energy': ['Reliance', 'ONGC', 'Indian Oil', 'GAIL', 'NTPC', 'Power Grid', 'Adani Power', 'Torrent Power', 'Tata Power', 'Coal India'],
    'FMCG': ['HUL', 'Nestle India', 'ITC', 'Dabur', 'Britannia', 'Godrej Consumer', 'Marico', 'Colgate', 'Emami', 'Page Industries'],
    'Automobile': ['Maruti Suzuki', 'Tata Motors', 'Mahindra', 'Hero MotoCorp', 'Bajaj Auto', 'TVS Motors', 'Eicher Motors', 'Ashok Leyland', 'Bosch', 'Escorts'],
    'Metals': ['Tata Steel', 'JSW Steel', 'Hindalco', 'NMDC', 'Vedanta', 'Steel Authority', 'Jindal Steel', 'Jindal Stainless', 'Sail', 'Coal India'],
    'Telecom': ['Bharti Airtel', 'Jio', 'Vodafone Idea'],
    'Real Estate': ['DLF', 'Godrej Properties', 'Oberoi Realty', 'Prestige Estates', 'Sobha', 'Brigade Enterprises', 'Kolte Patil', 'Phoenix Mills'],
    'Infrastructure': ['Larsen & Toubro', 'Adani Ports', 'GMR Infrastructure', 'GIC Housing', 'Ashoka Buildcon', 'IRB Infrastructure', 'Sadbhav Engineering', 'NCC', 'Simplex Infrastructures']
}

sectors_expanded = list(companies_expanded.keys())

headline_templates_expanded = [
    "Shares of {company} in {sector} sector {movement} amid {reason}.",
    "{sector} stocks {movement} following {event}.",
    "Investors optimistic as {sector} sector {movement} on {reason}.",
    "{company} reports {result}, boosting {sector} sector.",
    "{sector} stocks face pressure due to {reason}.",
    "{company} announces {announcement}, impacting {sector} stocks.",
    "Market reacts to {event} in {sector} sector.",
    "{sector} companies see {movement} after {event}.",
    "Strong {sector} earnings drive market {movement}.",
    "{company} leads {sector} gains after {event}.",
    "Weakness in {sector} drags market down amid {reason}.",
    "{company} stock {movement} after {announcement}.",
    "{sector} sector performance mixed following {event}.",
    "Positive cues from {sector} sector as {company} {movement}.",
    "{company} eyes expansion, {sector} stocks {movement}.",
    "Concerns over {reason} cause {sector} slump.",
    "{sector} sector rallies on {event}.",
    "Earnings beat lifts {company} and {sector} sector.",
    "Regulatory changes impact {sector} sector, stocks {movement}.",
    "Market sentiment shifts on {event} affecting {sector}.",
    "Investors await {event}, {sector} stocks volatile.",
    "Strong demand boosts {sector} sector and {company} shares.",
    "{company} plans merger, causing {sector} rally.",
    "Global trends influence {sector} sector, stocks {movement}.",
    "{sector} outlook positive on {reason}.",
    "{company} faces challenges amid {reason}, shares {movement}.",
    "Mixed results from {sector} sector after {event}.",
    "Surge in {sector} stocks led by {company} amid {reason}.",
    "Market correction hits {sector} stocks after {event}.",
    "Tech innovation fuels {sector} sector gains."
]

reasons_expanded = [
    "better-than-expected quarterly results", "government policy reforms", "rising crude oil prices", "global market trends",
    "currency fluctuations", "regulatory changes", "strong export data", "new product launches",
    "merger and acquisition rumors", "inflation concerns", "interest rate hike", "monsoon impact on agriculture",
    "infrastructure spending boost", "geopolitical tensions", "supply chain disruptions", "rising raw material costs",
    "currency depreciation", "tax reforms", "sector-specific regulations", "consumer demand recovery", "technology adoption"
]

movements_expanded = ["rise", "fall", "soar", "dip", "recover", "plunge", "stabilize", "gain momentum"]

results_expanded = ["strong quarterly earnings", "record profits", "losses", "mixed results", "positive outlook", "negative outlook"]

events_expanded = reasons_expanded

announcements_expanded = [
    "dividend declaration", "new product launch", "strategic partnership", "share buyback plan",
    "management change", "earnings guidance update", "capital expenditure plan", "expansion into new markets"
]

sentiments_expanded = ['Positive', 'Negative', 'Neutral', 'Mixed']

emotions_expanded = ['Optimism', 'Caution', 'Fear', 'Confidence', 'Uncertainty']

def generate_price_change(sentiment):
    if sentiment == 'Positive':
        return round(random.uniform(0.5, 7), 2)
    elif sentiment == 'Negative':
        return round(random.uniform(-7, -0.5), 2)
    elif sentiment == 'Mixed':
        return round(random.uniform(-3, 3), 2)
    else:
        return round(random.uniform(-1, 1), 2)

def generate_volume():
    return round(random.uniform(1, 1000), 2)

def generate_dataset(num_rows=2500, start_year=2024, file_name='data/indian_stock_news_2024_25.csv'):
    rows_expanded = []
    start_date_expanded = datetime.strptime(f"{start_year}-01-01", "%Y-%m-%d")
    max_days = 600  # Approx 1.5 years

    for _ in range(num_rows):
        sector = random.choice(sectors_expanded)
        company = random.choice(companies_expanded[sector])
        sentiment = random.choices(sentiments_expanded, weights=[0.4,0.3,0.2,0.1])[0]
        emotion = random.choice(emotions_expanded)
        price_change = generate_price_change(sentiment)
        volume = generate_volume()
        movement_word = 'rise' if price_change > 0 else 'fall' if price_change < 0 else 'stabilize'
        headline_template = random.choice(headline_templates_expanded)
        reason = random.choice(reasons_expanded)
        result = random.choice(results_expanded)
        event = random.choice(events_expanded)
        announcement = random.choice(announcements_expanded)
        headline = headline_template.format(
            company=company, sector=sector, movement=movement_word, reason=reason,
            result=result, event=event, announcement=announcement
        )
        summary = f"{company} in the {sector} sector has seen a {movement_word} of {price_change}% due to {reason}. Market sentiment is {sentiment} with {emotion} prevailing."
        rand_days = random.randint(0, max_days)
        date = start_date_expanded + timedelta(days=rand_days)
        rows_expanded.append([
            date.strftime("%Y-%m-%d"), headline, summary, sector, sentiment, emotion,
            price_change, volume
        ])
    df_expanded = pd.DataFrame(rows_expanded, columns=[
        'date', 'headline', 'summary', 'sector', 'sentiment', 'emotion',
        'price_change', 'trading_volume_crore'
    ])
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    df_expanded.to_csv(file_name, index=False)
    print(f"Dataset generated and saved to {file_name}")

def generate_dataset_large(num_rows=50000, start_year=2020, file_name='data/indian_stock_news_large_2020_25.csv'):
    rows_expanded = []
    start_date_expanded = datetime.strptime(f"{start_year}-01-01", "%Y-%m-%d")
    max_days = 5 * 365  # 5 years

    for _ in range(num_rows):
        sector = random.choice(sectors_expanded)
        company = random.choice(companies_expanded[sector])
        sentiment = random.choices(sentiments_expanded, weights=[0.4,0.3,0.2,0.1])[0]
        emotion = random.choice(emotions_expanded)
        price_change = generate_price_change(sentiment)
        volume = generate_volume()
        movement_word = 'rise' if price_change > 0 else 'fall' if price_change < 0 else 'stabilize'
        headline_template = random.choice(headline_templates_expanded)
        reason = random.choice(reasons_expanded)
        result = random.choice(results_expanded)
        event = random.choice(events_expanded)
        announcement = random.choice(announcements_expanded)
        headline = headline_template.format(
            company=company, sector=sector, movement=movement_word, reason=reason,
            result=result, event=event, announcement=announcement
        )
        summary = f"{company} in the {sector} sector has seen a {movement_word} of {price_change}% due to {reason}. Market sentiment is {sentiment} with {emotion} prevailing."
        rand_days = random.randint(0, max_days)
        date = start_date_expanded + timedelta(days=rand_days)
        rows_expanded.append([
            date.strftime("%Y-%m-%d"), headline, summary, sector, sentiment, emotion,
            price_change, volume
        ])
    df_expanded = pd.DataFrame(rows_expanded, columns=[
        'date', 'headline', 'summary', 'sector', 'sentiment', 'emotion',
        'price_change', 'trading_volume_crore'
    ])
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    df_expanded.to_csv(file_name, index=False)
    print(f"Large dataset generated and saved to {file_name}")

if __name__ == "__main__":
    # Choose which dataset to generate
    generate_dataset()      # Default smaller dataset
    # generate_dataset_large() # Uncomment to generate large scaled dataset
