import re
from typing import Dict, Any, List

# Positive and negative word lists for local rule-based sentiment assessment
POSITIVE_WORDS = {
    "great", "fantastic", "excellent", "amazing", "supportive", "friendly", 
    "satisfied", "happy", "love", "collaborative", "smooth", "perfect", 
    "challenge", "growth", "challenge", "challenging", "good", "solid", "learning"
}

NEGATIVE_WORDS = {
    "stuck", "heavy", "burnout", "micromanagement", "toxic", "unrealistic", 
    "undervalued", "outdated", "disconnected", "stagnant", "frustrated", 
    "stress", "pressure", "overwork", "micromanage", "criticized", "poor", 
    "bad", "unhappy", "worse", "disappointing", "lack"
}

CATEGORY_KEYWORDS = {
    "Compensation & Benefits": ["salary", "hike", "pay", "compensation", "benefit", "commission", "stipend"],
    "Career Growth": ["promotion", "grow", "growth", "career", "progression", "pathway", "stagnant", "advancement"],
    "Workplace Culture": ["culture", "team", "collaborative", "peers", "people", "bonding", "atmosphere", "friendly"],
    "Work-Life Balance": ["workload", "balance", "hours", "burnout", "life", "pressure", "stress", "late"],
    "Management & Leadership": ["management", "leadership", "manager", "micromanage", "executive", "communication", "direction"]
}

def analyze_sentiment(text: str, api_key: str = None, model_name: str = None) -> float:
    """
    Computes sentiment polarity from -1.0 (very negative) to 1.0 (very positive).
    If api_key is provided, this function acts as a hook/template for external LLM API sentiment calls.
    By default, it runs a local keyword matching algorithm.
    """
    if not isinstance(text, str) or not text.strip():
        return 0.0
        
    # Hook for external LLM execution if configured by user
    if api_key:
        # Template placeholder for OpenAI / Anthropic API call:
        # client = OpenAI(api_key=api_key)
        # response = client.chat.completions.create(...)
        pass
        
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)
    
    total = pos_count + neg_count
    if total == 0:
        return 0.0
        
    return (pos_count - neg_count) / total

def categorize_feedback(text: str) -> List[str]:
    """Categorizes the feedback text based on key themes."""
    if not isinstance(text, str) or not text.strip():
        return ["General"]
        
    text_lower = text.lower()
    categories = []
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                categories.append(category)
                break
                
    return categories if categories else ["General"]

def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    """Extracts prominent descriptive keywords from feedback comments (excluding trivial stopwords)."""
    if not isinstance(text, str) or not text.strip():
        return []
        
    stopwords = {
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", 
        "he", "him", "his", "she", "her", "it", "its", "they", "them", "their", "what", "which", 
        "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", 
        "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
        "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", 
        "with", "about", "against", "between", "into", "through", "during", "before", "after", 
        "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", 
        "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", 
        "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", 
        "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", 
        "should", "now", "feel", "get", "working", "also", "would", "could"
    }
    
    text_lower = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', text_lower) # only words with length >= 3
    filtered_words = [w for w in words if w not in stopwords]
    
    counts = {}
    for w in filtered_words:
        counts[w] = counts.get(w, 0) + 1
        
    sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [w[0] for w in sorted_words[:top_n]]

def get_action_recommendation(risk_drivers: List[str]) -> List[str]:
    """Generates actionable items for managers to address specific employee risk drivers."""
    recommendations = []
    
    for driver in risk_drivers:
        drv_lower = driver.lower()
        if "satisfaction" in drv_lower:
            recommendations.append("Schedule a 1-on-1 check-in to discuss job satisfaction and source of frustration.")
        if "work-life" in drv_lower or "workload" in drv_lower:
            recommendations.append("Conduct a workload audit. Consider delegating tasks or adjusting scope to ease stress.")
        if "promotion" in drv_lower or "stagnation" in drv_lower:
            recommendations.append("Outline a clear professional development roadmap. Discuss goals and timeline for next career steps.")
        if "salary" in drv_lower or "compensation" in drv_lower:
            recommendations.append("Initiate a formal compensation review relative to local market benchmark rates.")
        if "sentiment" in drv_lower or "negative" in drv_lower:
            recommendations.append("Perform a feedback review. Address specific complaints regarding team environment or processes.")
            
    if not recommendations:
        recommendations.append("Maintain regular contact. Continue offering professional development opportunities.")
        
    return recommendations
