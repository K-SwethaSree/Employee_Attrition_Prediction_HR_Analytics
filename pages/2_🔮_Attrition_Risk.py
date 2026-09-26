import streamlit as st
import pandas as pd
import plotly.express as px
from src.components import (
    load_custom_css, 
    render_sidebar_header, 
    get_risk_badge, 
    render_footer
)
from src.data_loader import load_feedback_data
from src.sentiment_analyzer import analyze_sentiment, get_action_recommendation
from src.model_predictor import batch_assess_risk, calculate_employee_risk

# Page configurations
st.set_page_config(
    page_title="Attrition Risk Assessment | FeedbackAI",
    page_icon="🔮",
    layout="wide"
)

load_custom_css()
render_sidebar_header()

df = load_feedback_data()

# Process sentiment and risk
if not df.empty:
    sentiments = [analyze_sentiment(str(text)) for text in df["feedback_text"]]
    df = batch_assess_risk(df, sentiments)
    df["sentiment_score"] = sentiments
    
    # Extract distinct list of all risk drivers for aggregation
    all_drivers = []
    for idx, row in df.iterrows():
        _, _, drivers = calculate_employee_risk(row, row["sentiment_score"])
        all_drivers.extend(drivers)
else:
    all_drivers = []

st.markdown('# Attrition Risk <span class="gradient-text">Predictor & Diagnostics</span>', unsafe_allow_html=True)
st.write("Predictive modeling based on work characteristics, satisfaction ratings, tenure details, and feedback sentiment.")
st.markdown("---")

if df.empty:
    st.warning("⚠️ No employee data available. Please submit feedback via the survey form to unlock risk assessments.")
else:
    # Set up interactive view tabs
    tab_overview, tab_individual = st.tabs(["📊 Organization-Wide Diagnostics", "👤 Individual Employee Audit"])
    
    # ------------------ TAB 1: OVERVIEW ------------------
    with tab_overview:
        col_summary, col_chart = st.columns([1, 1])
        
        with col_summary:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("### 🔍 Risk Indicators Frequency")
            st.write("Aggregated breakdown of risk flags triggered across the entire organization.")
            
            # Exclude default success flag from counts if present
            meaningful_drivers = [d for d in all_drivers if "No active risk" not in d]
            
            if meaningful_drivers:
                driver_counts = pd.Series(meaningful_drivers).value_counts().reset_index()
                driver_counts.columns = ["Risk Factor", "Trigger Count"]
                
                fig_factors = px.bar(
                    driver_counts,
                    x="Trigger Count",
                    y="Risk Factor",
                    orientation="h",
                    color="Trigger Count",
                    color_continuous_scale="Reds",
                    height=280
                )
                fig_factors.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    coloraxis_showscale=False,
                    margin=dict(t=10, b=10, l=10, r=10),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.05)', dtick=1),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.05)', categoryorder="total ascending")
                )
                st.plotly_chart(fig_factors, use_container_width=True)
            else:
                st.success("✅ No negative risk factors detected across the organization.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_chart:
            st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("### 🏢 Attrition Risk Heatmap")
            st.write("Cross-comparison of average Job Satisfaction vs Attrition Risk Score by Department.")
            
            dept_stats = df.groupby("department").agg(
                avg_risk=("risk_score", "mean"),
                avg_sat=("satisfaction_score", "mean"),
                count=("employee_id", "count")
            ).reset_index()
            
            fig_scatter = px.scatter(
                dept_stats,
                x="avg_sat",
                y="avg_risk",
                size="count",
                color="avg_risk",
                hover_name="department",
                labels={"avg_sat": "Average Satisfaction", "avg_risk": "Average Risk (%)"},
                color_continuous_scale="RdYlGn_r",
                size_max=30,
                height=260
            )
            fig_scatter.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                coloraxis_showscale=False,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', range=[0.8, 5.2]),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', range=[0, 100])
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Risk Registry
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Attrition Risk Registry")
        
        # Filters for registry table
        filter_cols = st.columns(3)
        with filter_cols[0]:
            sel_dept = st.selectbox("Department Filter", ["All"] + sorted(df["department"].unique().tolist()), key="overview_dept")
        with filter_cols[1]:
            sel_level = st.selectbox("Risk Level Filter", ["All", "High", "Medium", "Low"], key="overview_level")
        with filter_cols[2]:
            search_query = st.text_input("Search Employee ID or Name", "")
            
        reg_df = df.copy()
        if sel_dept != "All":
            reg_df = reg_df[reg_df["department"] == sel_dept]
        if sel_level != "All":
            reg_df = reg_df[reg_df["risk_level"] == sel_level]
        if search_query:
            reg_df = reg_df[
                reg_df["name"].str.contains(search_query, case=False) |
                reg_df["employee_id"].str.contains(search_query, case=False)
            ]
            
        if reg_df.empty:
            st.info("No employee records match the registry filters.")
        else:
            table_rows = []
            for _, row in reg_df.sort_values(by="risk_score", ascending=False).iterrows():
                risk_badge = get_risk_badge(row['risk_level'])
                table_rows.append(
                    f"""
                    <tr>
                        <td style="padding: 10px; font-weight: 500;">{row['employee_id']}</td>
                        <td style="padding: 10px;">{row['name']}</td>
                        <td style="padding: 10px;">{row['department']}</td>
                        <td style="padding: 10px; text-align: center;">{row['tenure_years']} yrs</td>
                        <td style="padding: 10px; text-align: center;">{row['last_promotion_years']} yrs</td>
                        <td style="padding: 10px; text-align: center;">{row['salary_level']}</td>
                        <td style="padding: 10px; text-align: center; font-weight: bold; color: {'#ef4444' if row['risk_score']>=70 else ('#f59e0b' if row['risk_score']>=35 else '#10b981')}">{row['risk_score']}%</td>
                        <td style="padding: 10px; text-align: center;">{risk_badge}</td>
                        <td style="padding: 10px; font-size: 0.85rem; max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{row['risk_drivers']}">{row['risk_drivers']}</td>
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
                                <th style="padding: 10px;">ID</th>
                                <th style="padding: 10px;">Employee</th>
                                <th style="padding: 10px;">Department</th>
                                <th style="padding: 10px; text-align: center;">Tenure</th>
                                <th style="padding: 10px; text-align: center;">Time since Promo</th>
                                <th style="padding: 10px; text-align: center;">Salary</th>
                                <th style="padding: 10px; text-align: center;">Risk Score</th>
                                <th style="padding: 10px; text-align: center;">Risk Level</th>
                                <th style="padding: 10px;">Primary Drivers</th>
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
        
    # ------------------ TAB 2: INDIVIDUAL ------------------
    with tab_individual:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 👤 Employee Diagnostic Workspace")
        
        # Employee Selector
        emp_options = {f"{row['employee_id']} - {row['name']}": row for _, row in df.iterrows()}
        selected_emp_label = st.selectbox("Select Employee to Audit", list(emp_options.keys()))
        
        if selected_emp_label:
            emp_row = emp_options[selected_emp_label]
            
            # Recalculate drivers and recommendation list
            score, level, drivers = calculate_employee_risk(emp_row, emp_row["sentiment_score"])
            recommendations = get_action_recommendation(drivers)
            
            # Sub layout
            sub_col1, sub_col2 = st.columns([1, 1.2])
            
            with sub_col1:
                # Gauge representation of risk score
                st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                
                # Visual Risk Card
                color = "#ef4444" if level == "High" else ("#f59e0b" if level == "Medium" else "#10b981")
                st.markdown(
                    f"""
                    <div style="background-color: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                        <h4 style="margin: 0; opacity: 0.7; font-size: 0.9rem;">ASSESSED ATTRITION RISK</h4>
                        <div style="font-size: 3.5rem; font-weight: 800; color: {color}; margin: 10px 0;">{score}%</div>
                        <div>{get_risk_badge(level)}</div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Employee Demographic info list
                st.markdown(
                    f"""
                    <div style="text-align: left; padding: 1rem; border-left: 3px solid {color}; background-color: rgba(255,255,255,0.01);">
                        <strong>Department:</strong> {emp_row['department']}<br/>
                        <strong>Tenure:</strong> {emp_row['tenure_years']} Years<br/>
                        <strong>Last Promotion:</strong> {emp_row['last_promotion_years']} Years Ago<br/>
                        <strong>Salary Category:</strong> {emp_row['salary_level']}<br/>
                        <strong>Survey Satisfaction:</strong> {emp_row['satisfaction_score']}/5<br/>
                        <strong>Work Life Balance:</strong> {emp_row['work_life_balance']}/5
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
            with sub_col2:
                # Risk Drivers and Recommendations
                st.markdown("#### 🚨 Primary Drivers")
                for d in drivers:
                    st.markdown(f"- {d}")
                    
                st.markdown("#### 🛠️ Proposed Management Action Roadmap")
                for r in recommendations:
                    st.markdown(f"👉 **{r}**")
                    
                # Display employee's text comments
                st.markdown("#### 💬 Feedback Submitted")
                st.markdown(
                    f"""
                    <blockquote style="font-style: italic; background-color: rgba(255, 255, 255, 0.02); border-left: 4px solid #6366f1; padding: 10px 15px; margin: 0; border-radius: 0 8px 8px 0;">
                        "{emp_row['feedback_text']}"
                    </blockquote>
                    """,
                    unsafe_allow_html=True
                )
                
        st.markdown('</div>', unsafe_allow_html=True)

render_footer()
