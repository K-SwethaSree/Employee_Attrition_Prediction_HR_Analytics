import streamlit as st
import pandas as pd
import plotly.express as px
from src.components import (
    load_custom_css, 
    render_sidebar_header, 
    get_sentiment_badge,
    render_footer
)
from src.data_loader import load_feedback_data
from src.sentiment_analyzer import analyze_sentiment, categorize_feedback, extract_keywords

# Page configurations
st.set_page_config(
    page_title="Feedback Analytics | FeedbackAI",
    page_icon="📊",
    layout="wide"
)

load_custom_css()
render_sidebar_header()

df = load_feedback_data()

# Preprocess DataFrame with sentiment and themes
if not df.empty:
    df["sentiment_score"] = df["feedback_text"].apply(lambda x: analyze_sentiment(str(x)))
    df["sentiment_label"] = df["sentiment_score"].apply(
        lambda x: "Positive" if x > 0.1 else ("Negative" if x < -0.1 else "Neutral")
    )
    df["themes"] = df["feedback_text"].apply(lambda x: categorize_feedback(str(x)))
    df["keywords"] = df["feedback_text"].apply(lambda x: extract_keywords(str(x)))
else:
    df["sentiment_score"] = []
    df["sentiment_label"] = []
    df["themes"] = []
    df["keywords"] = []

st.markdown('# Feedback <span class="gradient-text">Analytics Portal</span>', unsafe_allow_html=True)
st.write("Deep-dive textual diagnostics, natural language category mappings, and sentiment splits across company departments.")
st.markdown("---")

if df.empty:
    st.warning("⚠️ No feedback data available. Please submit feedback via the survey form to unlock insights.")
else:
    # Sidebar Filters
    st.sidebar.subheader("🔍 Filter Feedback")
    
    departments = ["All"] + sorted(df["department"].unique().tolist())
    selected_dept = st.sidebar.selectbox("Filter by Department", departments)
    
    sentiments = ["All", "Positive", "Neutral", "Negative"]
    selected_sent = st.sidebar.selectbox("Filter by Sentiment", sentiments)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_dept != "All":
        filtered_df = filtered_df[filtered_df["department"] == selected_dept]
    if selected_sent != "All":
        filtered_df = filtered_df[filtered_df["sentiment_label"] == selected_sent]
        
    # Stats Row
    total_filtered = len(filtered_df)
    
    st.write(f"Showing {total_filtered} of {len(df)} total submissions based on current filters.")
    
    # 2. Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🏷️ Top Feedback Themes")
        
        # Explode themes to count frequencies
        all_themes = []
        for themes_list in filtered_df["themes"]:
            all_themes.extend(themes_list)
            
        if all_themes:
            theme_counts = pd.Series(all_themes).value_counts().reset_index()
            theme_counts.columns = ["Theme", "Mentions"]
            
            fig_theme = px.bar(
                theme_counts,
                y="Theme",
                x="Mentions",
                orientation="h",
                color="Mentions",
                color_continuous_scale="Purples",
                height=300
            )
            fig_theme.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                coloraxis_showscale=False,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', dtick=1),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', categoryorder="total ascending")
            )
            st.plotly_chart(fig_theme, use_container_width=True)
        else:
            st.info("No themes extracted from the filtered feedback data.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔠 Common Feedback Keywords")
        
        # Aggregate keywords
        all_keywords = []
        for kw_list in filtered_df["keywords"]:
            all_keywords.extend(kw_list)
            
        if all_keywords:
            kw_counts = pd.Series(all_keywords).value_counts().reset_index()
            kw_counts.columns = ["Keyword", "Count"]
            kw_counts = kw_counts.head(10)
            
            fig_kw = px.scatter(
                kw_counts,
                x="Keyword",
                y="Count",
                size="Count",
                color="Count",
                color_continuous_scale="Teal",
                height=300
            )
            fig_kw.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                coloraxis_showscale=False,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig_kw, use_container_width=True)
        else:
            st.info("No prominent keywords extracted.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 3. Qualitative List
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Sentiment Review Feed")
    
    if filtered_df.empty:
        st.info("No feedback records match the active criteria.")
    else:
        for idx, row in filtered_df.sort_values(by="timestamp", ascending=False).iterrows():
            badge_html = get_sentiment_badge(row["sentiment_label"])
            themes_badges = "".join([f'<span class="badge" style="background-color: rgba(255,255,255,0.05); color: #ffffff; border: 1px solid rgba(255,255,255,0.1); margin-right: 5px;">{t}</span>' for t in row["themes"]])
            kws = ", ".join(row["keywords"])
            
            st.markdown(
                f"""
                <div style="background-color: rgba(255, 255, 255, 0.02); padding: 1.2rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div>
                            <strong>{row['name']}</strong> ({row['employee_id']}) • <span style="opacity: 0.6; font-size: 0.85rem;">{row['department']} • {row['timestamp']}</span>
                        </div>
                        <div>
                            {badge_html}
                        </div>
                    </div>
                    <p style="font-size: 0.95rem; line-height: 1.4; margin-bottom: 0.75rem;">
                        "{row['feedback_text']}"
                    </p>
                    <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 5px; font-size: 0.8rem;">
                        <span style="opacity: 0.5;">Themes:</span> {themes_badges}
                        <span style="opacity: 0.5; margin-left: 10px;">Keywords:</span> <span style="color: #818cf8; font-weight: 500;">{kws if kws else 'None'}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    st.markdown('</div>', unsafe_allow_html=True)

render_footer()
