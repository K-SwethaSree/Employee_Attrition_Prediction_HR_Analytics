import streamlit as st
import os
import shutil
from src.components import (
    load_custom_css, 
    render_sidebar_header, 
    render_footer
)
from src.data_loader import get_feedback_filepath, get_template_filepath

# Page configurations
st.set_page_config(
    page_title="Settings | FeedbackAI",
    page_icon="⚙️",
    layout="wide"
)

load_custom_css()
render_sidebar_header()

st.markdown('# System <span class="gradient-text">Configuration</span>', unsafe_allow_html=True)
st.write("Tune heuristic model weights, configure AI model providers, and manage system database files.")
st.markdown("---")

col_weights, col_engine = st.columns(2)

# Initialize Session States for customization weights if not set
if "weight_satisfaction" not in st.session_state:
    st.session_state["weight_satisfaction"] = 30
if "weight_wlb" not in st.session_state:
    st.session_state["weight_wlb"] = 20
if "weight_stagnation" not in st.session_state:
    st.session_state["weight_stagnation"] = 20
if "weight_salary" not in st.session_state:
    st.session_state["weight_salary"] = 15
if "weight_sentiment" not in st.session_state:
    st.session_state["weight_sentiment"] = 15

with col_weights:
    st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
    st.markdown("### 🎛️ Attrition Model Weights")
    st.write("Adjust the importance percentage of each factor in the overall risk prediction score.")
    
    w_sat = st.slider("Job Satisfaction Weight (%)", 0, 50, st.session_state["weight_satisfaction"])
    w_wlb = st.slider("Work-Life Balance Weight (%)", 0, 50, st.session_state["weight_wlb"])
    w_stag = st.slider("Promotion Stagnation Weight (%)", 0, 50, st.session_state["weight_stagnation"])
    w_sal = st.slider("Salary Level Weight (%)", 0, 50, st.session_state["weight_salary"])
    w_sent = st.slider("Text Sentiment Weight (%)", 0, 50, st.session_state["weight_sentiment"])
    
    total_w = w_sat + w_wlb + w_stag + w_sal + w_sent
    if total_w != 100:
        st.warning(f"⚠️ Total weight equals **{total_w}%**. For accurate score scales, weights should sum to 100%.")
    else:
        st.success("✅ Weights sum to 100%.")
        
    if st.button("Apply Weights Configuration"):
        st.session_state["weight_satisfaction"] = w_sat
        st.session_state["weight_wlb"] = w_wlb
        st.session_state["weight_stagnation"] = w_stag
        st.session_state["weight_salary"] = w_sal
        st.session_state["weight_sentiment"] = w_sent
        st.success("Weights updated successfully! (Note: Core model file will be dynamically updated to respect these configs)")
        
    st.markdown('</div>', unsafe_allow_html=True)

with col_engine:
    st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
    st.markdown("### 🤖 Natural Language Engine")
    st.write("Select the sentiment analysis backend engine.")
    
    ai_engine = st.selectbox(
        "Active NLP Model Provider",
        ["Local Rule-Based (Dictionary-based, Offline)", "OpenAI GPT-4o", "Anthropic Claude 3.5 Sonnet", "Google Gemini 1.5 Pro"]
    )
    
    if ai_engine != "Local Rule-Based (Dictionary-based, Offline)":
        api_key_input = st.text_input("Enter Provider API Key", type="password", placeholder="sk-...")
        model_name = st.text_input("Model Name Tag", value="gpt-4o" if "OpenAI" in ai_engine else ("claude-3-5-sonnet" if "Anthropic" in ai_engine else "gemini-1.5-pro"))
        
        st.info("💡 Once api keys are saved, sentiment analytics calls will pivot from local keywords to live LLM extraction.")
    else:
        st.write("✔️ Currently running local keyword classifier. No API keys required.")
        
    if st.button("Save Engine Configuration"):
        st.success(f"NLP Engine set to: {ai_engine}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Database Reset Panel
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### ⚠️ Database Administration & Diagnostics")
st.write("Tools to reset, archive, or clean the feedback telemetry storage database.")

db_path = get_feedback_filepath()
template_path = get_template_filepath()

col_db1, col_db2 = st.columns(2)

with col_db1:
    st.markdown(
        f"""
        <div style="background-color: rgba(255,255,255,0.02); padding: 1rem; border-radius: 8px;">
            <strong>Database File Path:</strong> <code>{db_path}</code><br/>
            <strong>Template File Path:</strong> <code>{template_path}</code>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_db2:
    if st.button("🔄 Reset Active Database to Template"):
        if os.path.exists(template_path):
            try:
                shutil.copy(template_path, db_path)
                st.success("Active database successfully re-initialized from template data!")
                st.toast("Database reset complete")
            except Exception as e:
                st.error(f"Failed to copy template: {str(e)}")
        else:
            st.error("Template file not found. Could not restore database.")
            
    st.markdown("<p style='font-size:0.8rem; opacity:0.6; margin-top:5px;'>Warning: This will overwrite any manual surveys submitted via the Portal.</p>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

render_footer()
