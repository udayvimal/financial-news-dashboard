import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.llm_helpers import load_data, generate_insight


# --- Enhanced dark mode for all charts with better quality ---
plt.style.use('dark_background')
sns.set_theme(
    style="darkgrid",
    rc={
        "axes.facecolor": "black",
        "figure.facecolor": "black",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "grid.color": "#444444",
        "text.color": "white",
        "axes.edgecolor": "white",
        "legend.facecolor": "#181826",
        "legend.edgecolor": "white",
        "axes.titlesize": 19,
        "axes.labelsize": 16,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "font.size": 15,
        "lines.linewidth": 2.2,
        "figure.dpi": 175,          # Higher resolution (for Streamlit rendering)
        "savefig.dpi": 240
    }
)

st.set_page_config(page_title="Finlytics AI", layout="wide")
st.title("📊 Finlytics AI")
st.markdown("### AI-Powered Financial News & Analysis Dashboard")


# --- Your branding/label ---
st.markdown(
    """
    <div style="display:flex;justify-content:space-between;align-items:center">
      <h1 style='margin-bottom:0;font-size:2.0rem;'> Financial News Dashboard with AI Insights</h1>
      <div style='font-size:1.12em; text-align:right'>
        Crafted by <a href="https://www.linkedin.com/in/udayvimal" target="_blank" style="color:#1589FF;font-weight:bold;text-decoration:none;">udayvimal</a>
      </div>
    </div>
    """, unsafe_allow_html=True
)

st.info("ℹ️ Use the sidebar to select filters and generate charts. If no chart appears, adjust your selections for sufficient data.")

df = load_data()

left, right = st.columns([1, 2])

with right:
    st.header("📈 Dashboard")

    with st.sidebar:
        st.header("Filter Options")
        min_date, max_date = df['date'].min(), df['date'].max()
        start_date, end_date = st.date_input(
            "Select Date Range",
            value=(min_date, max_date), min_value=min_date, max_value=max_date
        )

        sectors = df['sector'].unique().tolist()
        sentiments = df['sentiment'].unique().tolist()

        # Start with no default selection, user selects at least one
        selected_sectors = st.multiselect(
            "Select Sector(s)", options=sectors,
            default=[]
        )
        selected_sentiments = st.multiselect(
            "Select Sentiment(s)", options=sentiments,
            default=[]
        )

    # If user hasn't selected sectors or sentiments - empty dataframe
    if not selected_sectors or not selected_sentiments:
        filtered_df = pd.DataFrame()  # empty df
    else:
        filtered_df = df[
            (df['date'] >= pd.to_datetime(start_date)) &
            (df['date'] <= pd.to_datetime(end_date)) &
            (df['sector'].isin(selected_sectors)) &
            (df['sentiment'].isin(selected_sentiments))
        ]

    st.markdown(f"### Displaying {len(filtered_df)} records after filtering")

    dashboard_options = [
        "Price Change Over Time",
        "Trading Volume by Sector",
        "Sentiment Distribution",
        "Emotion Trends Over Time"
    ]
    selected_dashboard = st.selectbox("Select Dashboard View", options=dashboard_options)

    def darkize_ax(ax):
        ax.tick_params(colors="white", which="both")
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        plt.setp(ax.get_xticklabels(), color="white")
        plt.setp(ax.get_yticklabels(), color="white")
        for spine in ax.spines.values():
            spine.set_edgecolor("white")
        legend = ax.get_legend()
        if legend:
            for text in legend.get_texts():
                text.set_color('white')
            legend.get_frame().set_edgecolor('white')
            legend.get_frame().set_facecolor('#181826')

    if filtered_df.empty:
        st.warning("No data available for selected filters. Please select at least one sector and one sentiment in the sidebar.")
    else:
        try:
            if selected_dashboard == "Price Change Over Time":
                if filtered_df['sector'].nunique() < 1 or filtered_df['date'].nunique() < 2:
                    st.info("Not enough data to plot trends. Try broadening your selection.")
                else:
                    st.subheader("Price Change Over Time")
                    fig, ax = plt.subplots(figsize=(13, 6))
                    sns.lineplot(data=filtered_df, x='date', y='price_change', hue='sector', marker="o", ax=ax, linewidth=2.5)
                    ax.set_ylabel("Price Change (%)")
                    ax.set_xlabel("Date")
                    ax.set_title("Price Change Trends by Sector")
                    darkize_ax(ax)
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.clf()

            elif selected_dashboard == "Trading Volume by Sector":
                if filtered_df['sector'].nunique() < 1:
                    st.info("Not enough sectors for a trading volume chart. Try more sectors.")
                else:
                    st.subheader("Trading Volume by Sector")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    volume_by_sector = filtered_df.groupby('sector')['trading_volume_crore'].sum().sort_values(ascending=False)
                    volume_by_sector.plot(kind='bar', ax=ax)
                    ax.set_ylabel("Trading Volume (cr)")
                    ax.set_title("Trading Volume by Sector")
                    darkize_ax(ax)
                    st.pyplot(fig)
                    plt.clf()

            elif selected_dashboard == "Sentiment Distribution":
                if filtered_df['sentiment'].nunique() < 1:
                    st.info("No sentiment data to display.")
                else:
                    st.subheader("Sentiment Distribution")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    sentiment_counts = filtered_df['sentiment'].value_counts()
                    sentiment_counts.plot(kind='bar', ax=ax)
                    ax.set_ylabel("Count")
                    ax.set_title("Sentiment Distribution")
                    darkize_ax(ax)
                    st.pyplot(fig)
                    plt.clf()

            elif selected_dashboard == "Emotion Trends Over Time":
                if filtered_df['emotion'].nunique() < 1 or filtered_df['date'].nunique() < 2:
                    st.info("Not enough emotion data to plot trends.")
                else:
                    st.subheader("Emotion Trends Over Time")
                    fig, ax = plt.subplots(figsize=(12, 5))
                    emotion_date_counts = filtered_df.groupby(['date', 'emotion']).size().unstack(fill_value=0)
                    emotion_date_counts.plot(kind='line', ax=ax)
                    ax.set_ylabel("Count")
                    ax.set_xlabel("Date")
                    ax.set_title("Emotions Over Time")
                    plt.xticks(rotation=45)
                    darkize_ax(ax)
                    st.pyplot(fig)
                    plt.clf()
        except Exception as e:
            st.error(f"An error occurred generating the chart: {e}")

        # --- Filter Summary and Stats with edge-safety ---
        summary_col, stat_col = st.columns([3, 2])
        with summary_col:
            total_records = len(filtered_df)
            avg_price_change = filtered_df.groupby('sector')['price_change'].mean().sort_values(ascending=False)
            top_volume = filtered_df.groupby('sector')['trading_volume_crore'].sum().sort_values(ascending=False).head(3)

            def get_top(top_vol, idx):
                if len(top_vol) > idx:
                    s = top_vol.index[idx]
                    v = top_vol.values[idx]
                    return f"{s}: {v:,.2f} crore"
                else:
                    return "N/A"

            summary_md = f"""
| KPI | Value |
|---|---|
| **Total records** | {total_records} |
| **Avg Price Change (Top)** | {avg_price_change.idxmax() if not avg_price_change.empty else 'N/A'}: {avg_price_change.max():.2f}% |
| **Top 1 by Volume** | {get_top(top_volume, 0)} |
| **Top 2 by Volume** | {get_top(top_volume, 1)} |
| **Top 3 by Volume** | {get_top(top_volume, 2)} |
"""
            st.markdown("#### 📊 Filter Summary")
            st.markdown(summary_md)

        with stat_col:
            if selected_dashboard != "Sentiment Distribution":
                sentiment_counts = filtered_df['sentiment'].value_counts()
                st.markdown("#### Sentiment Breakdown")
                if not sentiment_counts.empty:
                    most_common = sentiment_counts.idxmax()
                    st.markdown(f"**Most common sentiment:** {most_common} ({sentiment_counts.max()} times)")
                    st.markdown("- Others: " + ", ".join([f"{k}: {v}" for k, v in sentiment_counts.items() if k != most_common]))
                else:
                    st.markdown("_No sentiment data in filter._")

            avg_by_selected = filtered_df.groupby('sector')['price_change'].mean().reindex(selected_sectors).dropna()
            if not avg_by_selected.empty:
                st.markdown("#### Avg. Price Change per Selected Sector")
                st.markdown(
                    "<ul style='margin-bottom:0'>" +
                    "".join([f"<li>{sector}: {pct:.2f}%</li>" for sector, pct in avg_by_selected.items()]) +
                    "</ul>", unsafe_allow_html=True
                )
            else:
                st.markdown("_No sectors selected or no data to compute price change._")


with left:
    st.header("💬 Analyst AI Chatbot")

    if filtered_df.empty:
        st.info("Adjust filters on the right to unlock analysis.")
    else:
        user_question = st.text_input("Ask your question:", key="user_input")
        if st.button("Ask Analyst AI"):
            if not user_question.strip():
                st.warning("Please type a question!")
            else:
                # Directly call generate_insight without chat history or spinner for faster response
                answer, sources = generate_insight(user_question, filtered_df, [])
                
                st.markdown("### Overview & Recommendations")
                st.markdown(answer)
