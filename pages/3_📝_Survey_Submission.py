import streamlit as st
import datetime
from src.components import (
    load_custom_css, 
    render_sidebar_header, 
    render_footer
)
from src.data_loader import add_survey_response

# Page configurations
st.set_page_config(
    page_title="Submit Survey | FeedbackAI",
    page_icon="📝",
    layout="wide"
)

load_custom_css()
render_sidebar_header()

st.markdown('# Feedback <span class="gradient-text">Submission Portal</span>', unsafe_allow_html=True)
st.write("Submit employee feedback, work satisfaction telemetry, and tenure data to record organizational health metrics.")
st.markdown("---")

# Render a styled container form
st.markdown("### 📋 Employee Survey Response Form")
st.write("Please fill in all demographic and qualitative feedback details accurately.")

with st.form("survey_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        emp_id = st.text_input("Employee ID", placeholder="e.g. EMP013", help="Unique identifier, usually EMP followed by 3 digits.")
        emp_name = st.text_input("Employee Full Name", placeholder="e.g. Eleanor Vance")
        
        dept = st.selectbox(
            "Department",
            ["Engineering", "Sales", "HR", "Marketing", "Finance", "Product", "Operations"]
        )
        
        salary_lvl = st.selectbox(
            "Salary Category",
            ["Low", "Medium", "High"]
        )
        
    with col2:
        tenure = st.number_input(
            "Tenure at Company (Years)", 
            min_value=0.0, 
            max_value=40.0, 
            value=1.0, 
            step=0.5,
            help="Total years working at the organization."
        )
        
        promo = st.number_input(
            "Years since Last Promotion", 
            min_value=0.0, 
            max_value=40.0, 
            value=1.0, 
            step=0.5,
            help="Years since last role change or salary advancement."
        )
        
        satisfaction = st.slider(
            "Job Satisfaction Rating", 
            min_value=1, 
            max_value=5, 
            value=3,
            help="1 = Highly Dissatisfied, 5 = Highly Satisfied"
        )
        
        wlb = st.slider(
            "Work-Life Balance Rating", 
            min_value=1, 
            max_value=5, 
            value=3,
            help="1 = Highly Unbalanced, 5 = Highly Balanced"
        )
        
    feedback_txt = st.text_area(
        "Qualitative Comments & Feedback", 
        placeholder="Write comments about career progression, company culture, workload, salary feedback, or management styles...",
        height=150
    )
    
    # Form submission buttons
    submit_button = st.form_submit_button("Submit Response")

if submit_button:
    # Basic validation
    if not emp_id.strip():
        st.error("❌ Employee ID is required.")
    elif not emp_name.strip():
        st.error("❌ Employee Name is required.")
    elif not feedback_txt.strip():
        st.error("❌ Feedback comments cannot be empty.")
    elif promo > tenure:
        st.error("❌ Years since last promotion cannot exceed total tenure years.")
    else:
        # Format date
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        
        # Add response to CSV
        success = add_survey_response(
            employee_id=emp_id.strip().upper(),
            name=emp_name.strip(),
            department=dept,
            satisfaction_score=int(satisfaction),
            tenure_years=float(tenure),
            last_promotion_years=float(promo),
            work_life_balance=int(wlb),
            salary_level=salary_lvl,
            feedback_text=feedback_txt.strip(),
            timestamp=today_str
        )
        
        if success:
            st.success(f"✅ Feedback response for **{emp_name}** ({emp_id.upper()}) was successfully recorded!")
            st.balloons()
        else:
            st.error("❌ Failed to save feedback response. Please check write permissions on the data directory.")

render_footer()
