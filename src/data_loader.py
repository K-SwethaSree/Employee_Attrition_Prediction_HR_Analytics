import pandas as pd
import os
import shutil

# Expected columns in our database
COLUMNS = [
    "employee_id", 
    "name", 
    "department", 
    "satisfaction_score", 
    "tenure_years", 
    "last_promotion_years", 
    "work_life_balance", 
    "salary_level", 
    "feedback_text", 
    "timestamp"
]

def get_data_dir() -> str:
    """Returns the path to the data directory, creating it if it doesn't exist."""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(current_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_feedback_filepath() -> str:
    """Returns the filepath of the active feedback.csv file."""
    return os.path.join(get_data_dir(), "feedback.csv")

def get_template_filepath() -> str:
    """Returns the filepath of the bootstrap template feedback_template.csv."""
    return os.path.join(get_data_dir(), "feedback_template.csv")

def load_feedback_data() -> pd.DataFrame:
    """
    Loads feedback data from feedback.csv.
    If feedback.csv doesn't exist:
      - If feedback_template.csv exists, copies it to feedback.csv and loads it.
      - Otherwise, creates an empty DataFrame with the default schema.
    """
    feedback_path = get_feedback_filepath()
    template_path = get_template_filepath()

    if not os.path.exists(feedback_path):
        if os.path.exists(template_path):
            try:
                shutil.copy(template_path, feedback_path)
            except Exception:
                # Fallback to direct loading of template
                return pd.read_csv(template_path)
        else:
            # Create a blank file with headers
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(feedback_path, index=False)
            return df
            
    try:
        df = pd.read_csv(feedback_path)
        # Ensure all columns exist
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = None
        return df
    except Exception:
        # If file is corrupted, return empty template dataframe
        return pd.DataFrame(columns=COLUMNS)

def save_feedback_data(df: pd.DataFrame) -> bool:
    """Saves the given DataFrame to feedback.csv."""
    try:
        feedback_path = get_feedback_filepath()
        # Keep columns aligned
        df_to_save = df[COLUMNS] if set(COLUMNS).issubset(df.columns) else df
        df_to_save.to_csv(feedback_path, index=False)
        return True
    except Exception:
        return False

def add_survey_response(
    employee_id: str,
    name: str,
    department: str,
    satisfaction_score: int,
    tenure_years: float,
    last_promotion_years: float,
    work_life_balance: int,
    salary_level: str,
    feedback_text: str,
    timestamp: str
) -> bool:
    """Appends a new feedback record to the database and saves it."""
    df = load_feedback_data()
    
    new_record = {
        "employee_id": employee_id,
        "name": name,
        "department": department,
        "satisfaction_score": satisfaction_score,
        "tenure_years": tenure_years,
        "last_promotion_years": last_promotion_years,
        "work_life_balance": work_life_balance,
        "salary_level": salary_level,
        "feedback_text": feedback_text,
        "timestamp": timestamp
    }
    
    # Append logic
    new_df = pd.DataFrame([new_record])
    df = pd.concat([df, new_df], ignore_index=True)
    return save_feedback_data(df)
