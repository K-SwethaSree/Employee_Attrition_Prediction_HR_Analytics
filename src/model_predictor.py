import pandas as pd
from typing import Dict, Any, List, Tuple

def calculate_employee_risk(row: pd.Series, sentiment_score: float = 0.0) -> Tuple[float, str, List[str]]:
    """
    Calculates an attrition risk score (0-100), risk level, and key drivers.
    
    Parameters:
      row: A pandas Series containing employee attributes (satisfaction_score, tenure_years, etc.)
      sentiment_score: Sentiment polarity score between -1.0 (very negative) and 1.0 (very positive)
      
    Returns:
      tuple of (risk_score, risk_level, drivers)
    """
    score = 0.0
    drivers = []
    
    # 1. Job Satisfaction (Max weight: 30%)
    sat = row.get("satisfaction_score", 3)
    if pd.isna(sat):
        sat = 3
    
    if sat == 1:
        score += 30
        drivers.append("Critical low job satisfaction (1/5)")
    elif sat == 2:
        score += 20
        drivers.append("Low job satisfaction (2/5)")
    elif sat == 3:
        score += 10
        # No driver for neutral satisfaction
        
    # 2. Work Life Balance (Max weight: 20%)
    wlb = row.get("work_life_balance", 3)
    if pd.isna(wlb):
        wlb = 3
        
    if wlb == 1:
        score += 20
        drivers.append("Critical work-life imbalance (1/5)")
    elif wlb == 2:
        score += 12
        drivers.append("Poor work-life balance (2/5)")
    elif wlb == 3:
        score += 5
        
    # 3. Tenure & Promotion Stagnation (Max weight: 20%)
    tenure = row.get("tenure_years", 0)
    promotion = row.get("last_promotion_years", 0)
    
    # If they have been here a while and haven't been promoted
    if not pd.isna(tenure) and not pd.isna(promotion):
        stagnation = promotion
        if stagnation >= 4.0:
            score += 20
            drivers.append(f"Severe promotion stagnation ({stagnation:.1f} yrs since promotion)")
        elif stagnation >= 2.5:
            score += 12
            drivers.append(f"Lack of promotion/role change ({stagnation:.1f} yrs)")
            
    # 4. Salary Level (Max weight: 15%)
    sal = str(row.get("salary_level", "Medium")).strip().lower()
    if sal == "low":
        score += 15
        drivers.append("Below market salary level")
    elif sal == "medium":
        score += 5
        
    # 5. Text Sentiment (Max weight: 15%)
    # sentiment_score ranges from -1.0 (negative) to 1.0 (positive)
    if sentiment_score < -0.5:
        score += 15
        drivers.append("Highly negative feedback comments")
    elif sentiment_score < -0.1:
        score += 10
        drivers.append("Somewhat negative feedback comments")
    elif sentiment_score > 0.4:
        # High positive sentiment slightly reduces risk score
        score -= 5
        
    # Boundary correction
    score = max(0.0, min(100.0, score))
    
    # Determine risk category
    if score >= 70.0:
        level = "High"
    elif score >= 35.0:
        level = "Medium"
    else:
        level = "Low"
        
    if not drivers:
        drivers.append("No active risk flags detected")
        
    return round(score, 1), level, drivers

def batch_assess_risk(df: pd.DataFrame, sentiments: List[float] = None) -> pd.DataFrame:
    """
    Applies risk calculation to an entire dataframe.
    
    Returns dataframe with risk_score, risk_level, and risk_drivers columns appended.
    """
    if df.empty:
        df_copy = df.copy()
        df_copy["risk_score"] = []
        df_copy["risk_level"] = []
        df_copy["risk_drivers"] = []
        return df_copy
        
    if sentiments is None or len(sentiments) != len(df):
        sentiments = [0.0] * len(df)
        
    scores = []
    levels = []
    drivers_list = []
    
    for idx, row in df.iterrows():
        sentiment = sentiments[idx]
        sc, lvl, drv = calculate_employee_risk(row, sentiment)
        scores.append(sc)
        levels.append(lvl)
        drivers_list.append(", ".join(drv))
        
    df_copy = df.copy()
    df_copy["risk_score"] = scores
    df_copy["risk_level"] = levels
    df_copy["risk_drivers"] = drivers_list
    
    return df_copy
