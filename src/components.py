import streamlit as st
import os

def load_custom_css():
    """Loads and injects the assets/custom.css stylesheet into the Streamlit app."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "custom.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        # Fallback inline basic style if file is missing
        st.markdown("""
            <style>
                .glass-card { background-color: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; margin-bottom: 15px; }
            </style>
        """, unsafe_allow_html=True)

def render_sidebar_header():
    """Renders a premium sidebar branding header."""
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 1.5rem 0rem 1rem 0rem;">
            <span style="font-size: 3rem;">🛰️</span>
            <h2 style="margin: 10px 0 0 0; font-weight: 700; font-size: 1.5rem;">
                <span class="gradient-text">FeedbackAI</span>
            </h2>
            <p style="font-size: 0.8rem; opacity: 0.6; margin-top: 5px;">
                Talent Attrition & Sentiment Engine
            </p>
        </div>
        <hr style="border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 1.5rem;" />
        """, 
        unsafe_allow_html=True
    )

def render_glass_card(title: str, content: str):
    """Renders content in a styled glassmorphic container."""
    st.markdown(
        f"""
        <div class="glass-card">
            <h3 style="margin-top: 0; margin-bottom: 1rem; font-weight: 600; font-size: 1.2rem;">{title}</h3>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_metric_card(label: str, value: str, delta: str = "", delta_type: str = "up", status_class: str = ""):
    """
    Renders a custom glassmorphic metric card.
    status_class can be: 'success', 'warning', 'danger', or '' (default)
    delta_type can be: 'up' (green), 'down' (red)
    """
    delta_html = ""
    if delta:
        cls = "up" if delta_type == "up" else "down"
        arrow = "↑" if delta_type == "up" else "↓"
        delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>'
        
    st.markdown(
        f"""
        <div class="metric-container {status_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def get_risk_badge(risk_level: str) -> str:
    """Returns the HTML markup for a styled attrition risk badge."""
    level = str(risk_level).lower().strip()
    if level == "high":
        return '<span class="badge badge-high">High Risk</span>'
    elif level == "medium":
        return '<span class="badge badge-medium">Medium Risk</span>'
    else:
        return '<span class="badge badge-low">Low Risk</span>'

def get_sentiment_badge(sentiment: str) -> str:
    """Returns the HTML markup for a styled sentiment badge."""
    level = str(sentiment).lower().strip()
    if level in ["negative", "neg", "low"]:
        return '<span class="badge badge-high">Negative</span>'
    elif level in ["neutral", "neu", "medium"]:
        return '<span class="badge badge-medium">Neutral</span>'
    else:
        return '<span class="badge badge-low">Positive</span>'

def render_footer():
    """Renders a clean footer alignment."""
    st.markdown(
        """
        <div style="text-align: center; margin-top: 3rem; padding: 1.5rem 0; font-size: 0.75rem; opacity: 0.4; border-top: 1px solid rgba(255,255,255,0.05);">
            Employee Feedback AI & Attrition Risk Portal • Developed with Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )
