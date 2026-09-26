import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.components import (
    load_custom_css, 
    render_sidebar_header, 
    render_metric_card, 
    get_risk_badge, 
    get_sentiment_badge,
    render_footer
)
from src.data_loader import load_feedback_data
from src.sentiment_analyzer import analyze_sentiment
from src.model_predictor import batch_assess_risk

# 1. Page Configuration
st.set_page_config(
    page_title="FeedbackAI | Talent Attrition & Sentiment Engine",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Styling and Sidebar Branding
load_custom_css()
render_sidebar_header()

# 3. Data Processing
df = load_feedback_data()

# Calculate sentiments and risks dynamically
if not df.empty:
    sentiments = [analyze_sentiment(str(text)) for text in df["feedback_text"]]
    df = batch_assess_risk(df, sentiments)
    df["sentiment_score"] = sentiments
    df["sentiment_label"] = df["sentiment_score"].apply(
        lambda x: "Positive" if x > 0.1 else ("Negative" if x < -0.1 else "Neutral")
    )
else:
    df["risk_score"] = []
    df["risk_level"] = []
    df["sentiment_score"] = []
    df["sentiment_label"] = []

# 4. Main Title
st.markdown('# Organization Health <span class="gradient-text">Overview</span>', unsafe_allow_html=True)
st.write("Real-time telemetry on organizational culture, feedback sentiment, and employee attrition vectors.")
st.markdown("---")

if df.empty:
    st.warning("⚠️ No employee feedback records found. Submit feedback via the 'Survey Submission' tab to get started!")
else:
    # 5. Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_responses = len(df)
    avg_sat = df["satisfaction_score"].mean()
    avg_wlb = df["work_life_balance"].mean()
    
    # Attrition Risk calculation
    high_risk_count = len(df[df["risk_level"] == "High"])
    high_risk_pct = (high_risk_count / total_responses) * 100
    
    # Sentiment calculation
    pos_sentiment_count = len(df[df["sentiment_label"] == "Positive"])
    pos_sentiment_pct = (pos_sentiment_count / total_responses) * 100
    
    with col1:
        render_metric_card(
            label="Total Submissions",
            value=f"{total_responses}",
            delta="New Feedbacks",
            delta_type="up"
        )
    with col2:
        risk_class = "danger" if high_risk_pct > 25 else ("warning" if high_risk_pct > 10 else "success")
        render_metric_card(
            label="Critical Attrition Risk",
            value=f"{high_risk_pct:.1f}%",
            delta=f"{high_risk_count} employees high risk",
            delta_type="down" if high_risk_pct > 15 else "up",
            status_class=risk_class
        )
    with col3:
        sent_class = "success" if pos_sentiment_pct > 60 else ("warning" if pos_sentiment_pct > 40 else "danger")
        render_metric_card(
            label="Positive Sentiment",
            value=f"{pos_sentiment_pct:.1f}%",
            delta="Overall Tone",
            delta_type="up" if pos_sentiment_pct > 50 else "down",
            status_class=sent_class
        )
    with col4:
        sat_class = "success" if avg_sat >= 3.8 else ("warning" if avg_sat >= 2.8 else "danger")
        render_metric_card(
            label="Avg Job Satisfaction",
            value=f"{avg_sat:.2f} / 5",
            delta=f"WLB: {avg_wlb:.1f}/5",
            delta_type="up" if avg_sat >= 3.0 else "down",
            status_class=sat_class
        )
        
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # 6. Graphs Grid
    graph_col1, graph_col2 = st.columns(2)
    
    with graph_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔮 Attrition Risk Distribution")
        risk_counts = df["risk_level"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Count"]
        
        # Color mapping matching badge styling
        color_map = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444"}
        fig_risk = px.pie(
            risk_counts,
            names="Risk Level",
            values="Count",
            color="Risk Level",
            color_discrete_map=color_map,
            hole=0.4,
            height=300
        )
        fig_risk.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with graph_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🏢 Average Attrition Risk by Department")
        dept_risk = df.groupby("department")["risk_score"].mean().reset_index().sort_values(by="risk_score", ascending=False)
        
        fig_dept = px.bar(
            dept_risk,
            x="department",
            y="risk_score",
            color="risk_score",
            color_continuous_scale="Viridis",
            labels={"department": "Department", "risk_score": "Avg Attrition Risk (%)"},
            height=300
        )
        fig_dept.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            coloraxis_showscale=False,
            margin=dict(t=10, b=10, l=10, r=10),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', range=[0, 100])
        )
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 7. Attention Required Alert Banner
    if high_risk_count > 0:
        st.markdown(
            f"""
            <div style="background-color: rgba(239, 68, 68, 0.15); border-left: 5px solid #ef4444; padding: 1rem 1.5rem; border-radius: 8px; margin: 1.5rem 0;">
                <h4 style="margin: 0; color: #ef4444; font-weight: 600;">🚨 Active Intervention Needed</h4>
                <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">
                    There are <strong>{high_risk_count} employees</strong> currently flagged with high attrition probability. 
                    Review risk indicators and proposed action roadmaps in the <strong>Attrition Risk</strong> module immediately.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # 8. Recent Employee Submissions Table
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Recent Feedback Submissions")
    
    # HTML representation table for gorgeous rendering of custom badges
    table_rows = []
    sorted_df = df.sort_values(by="timestamp", ascending=False)
    
    for _, row in sorted_df.iterrows():
        risk_badge = get_risk_badge(row['risk_level'])
        sent_badge = get_sentiment_badge(row['sentiment_label'])
        
        table_rows.append(
            f"""
            <tr>
                <td style="padding: 12px; font-weight: 500;">{row['employee_id']}</td>
                <td style="padding: 12px;">{row['name']}</td>
                <td style="padding: 12px;">{row['department']}</td>
                <td style="padding: 12px; text-align: center;">{row['satisfaction_score']} / 5</td>
                <td style="padding: 12px; text-align: center;">{row['work_life_balance']} / 5</td>
                <td style="padding: 12px; text-align: center;">{sent_badge}</td>
                <td style="padding: 12px; text-align: center;">{risk_badge}</td>
                <td style="padding: 12px; font-style: italic; opacity: 0.8; max-width: 300px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{row['feedback_text']}">{row['feedback_text']}</td>
            </tr>
            """
        )
        
    table_content = "".join(table_rows)
    st.markdown(
        f"""
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
                <thead>
                    <tr style="border-bottom: 2px solid rgba(255,255,255,0.1); opacity: 0.7;">
                        <th style="padding: 12px;">ID</th>
                        <th style="padding: 12px;">Employee</th>
                        <th style="padding: 12px;">Department</th>
                        <th style="padding: 12px; text-align: center;">Satisfaction</th>
                        <th style="padding: 12px; text-align: center;">WLB</th>
                        <th style="padding: 12px; text-align: center;">Sentiment</th>
                        <th style="padding: 12px; text-align: center;">Attrition Risk</th>
                        <th style="padding: 12px;">Raw Feedback Summary</th>
                    </tr>
                </thead>
                <tbody>
                    {table_content}
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

render_footer()
